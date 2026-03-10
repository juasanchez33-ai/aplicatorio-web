import { auth } from '/js/firebase-init.js';
import {
    onAuthStateChanged,
    signOut,
    sendPasswordResetEmail,
    reauthenticateWithCredential,
    EmailAuthProvider
} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
import { 
    PhoneAuthProvider,
    PhoneMultiFactorGenerator,
    multiFactor,
    RecaptchaVerifier,
    getMultiFactorResolver
} from './firebase-init.js';

let mainChart = null;
let dashboardState = {
    category: 'All',
    range: null,
    searchTerm: ''
};

// Global state
window.currentUser = null;
window.authCallbacks = [];

document.addEventListener('DOMContentLoaded', () => {
    initAuthListener();
    initCharts();
    fetchMarketData();
    setupRangeButtons();
    initPageSettings();
    initNotifications();
    initGlobalSearch();
});

// Notifications Management
window.initNotifications = () => {
    const existing = localStorage.getItem('fp_notifications');
    if (!existing) {
        localStorage.setItem('fp_notifications', JSON.stringify([]));
    }
    renderNotifications();
};

window.renderNotifications = () => {
    const notifications = JSON.parse(localStorage.getItem('fp_notifications') || '[]');
    const panel = document.getElementById('notifications-list');
    const badge = document.getElementById('notification-badge');

    if (!panel) return;

    const unreadCount = notifications.filter(n => !n.read).length;
    if (badge) {
        badge.style.display = unreadCount > 0 ? 'block' : 'none';
        badge.textContent = unreadCount;
    }

    if (notifications.length === 0) {
        panel.innerHTML = '<div class="p-8 text-center"><p class="text-xs text-slate-500">No hay notificaciones</p></div>';
        return;
    }

    panel.innerHTML = notifications.map(n => `
        <div onclick="window.markNotificationRead(${n.id})" 
             class="p-4 border-b border-white/5 hover:bg-white/5 cursor-pointer transition-colors relative ${n.read ? 'opacity-60' : ''}">
            ${!n.read ? '<span class="absolute right-4 top-4 w-1.5 h-1.5 bg-primary rounded-full"></span>' : ''}
            <p class="text-xs text-white font-medium">${n.title}</p>
            <p class="text-[10px] text-slate-500 mt-1">${n.message}</p>
            <p class="text-[9px] ${n.read ? 'text-slate-500' : 'text-primary'} mt-1 font-bold">${n.time}</p>
        </div>
    `).join('');
};

window.markNotificationRead = (id) => {
    const notifications = JSON.parse(localStorage.getItem('fp_notifications') || '[]');
    const updated = notifications.map(n => n.id === id ? { ...n, read: true } : n);
    localStorage.setItem('fp_notifications', JSON.stringify(updated));
    renderNotifications();
};

window.markAllNotificationsRead = () => {
    const notifications = JSON.parse(localStorage.getItem('fp_notifications') || '[]');
    const updated = notifications.map(n => ({ ...n, read: true }));
    localStorage.setItem('fp_notifications', JSON.stringify(updated));
    renderNotifications();
};

// Settings Management
const CURRENCY_RATES = { USD: 1, EUR: 0.92, COP: 3900, MXN: 17 };
const CURRENCY_SYMBOLS = { USD: '$', EUR: '€', COP: '$', MXN: '$' };

window.toggleSetting = (setting, value = null) => {
    let newState;
    if (value !== null) {
        newState = value;
    } else {
        const currentState = localStorage.getItem(`fp_setting_${setting}`) === 'true';
        newState = !currentState;
    }

    localStorage.setItem(`fp_setting_${setting}`, newState);
    applySettings();
    if (window.location.pathname === '/settings') updateSettingsUI();

    // Refresh data displays if currency or theme changes
    if (window.cachedMovements) processMovements(window.cachedMovements);
    if (window.cachedInvestments) processInvestments(window.cachedInvestments);
};

window.formatAmount = (amount) => {
    const currency = localStorage.getItem('fp_setting_currency') || 'USD';
    const rate = CURRENCY_RATES[currency] || 1;
    const symbol = CURRENCY_SYMBOLS[currency] || '$';
    const converted = amount * rate;

    return `${symbol}${converted.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
};

function initPageSettings() {
    applySettings();
    if (window.location.pathname === '/settings') updateSettingsUI();
}

function applySettings() {
    const darkMode = localStorage.getItem('fp_setting_darkMode') === 'true';
    if (darkMode) {
        document.documentElement.classList.add('dark-mode-active');
    } else {
        document.documentElement.classList.remove('dark-mode-active');
    }
}

function updateSettingsUI() {
    const darkMode = localStorage.getItem('fp_setting_darkMode') === 'true';
    const currency = localStorage.getItem('fp_setting_currency') || 'USD';
    const twoFactor = localStorage.getItem('fp_setting_twoFactor') === 'true';

    const dmToggle = document.getElementById('dark-mode-toggle');
    const dmThumb = document.getElementById('dark-mode-thumb');
    if (dmToggle && dmThumb) {
        dmToggle.className = `w-12 h-6 rounded-full relative cursor-pointer border transition-all ${darkMode ? 'bg-primary border-primary/50' : 'bg-slate-800 border-white/10'}`;
        dmThumb.className = `absolute top-1 w-4 h-4 bg-white rounded-full transition-all ${darkMode ? 'right-1' : 'left-1 bg-slate-400'}`;
    }

    const currSelect = document.getElementById('currency-select');
    if (currSelect) currSelect.value = currency;

    const tfaStatus = document.getElementById('two-factor-status');
    if (tfaStatus) {
        tfaStatus.textContent = twoFactor ? 'Activado' : 'Desactivado';
        tfaStatus.className = `text-[10px] px-2 py-1 rounded font-bold uppercase transition-all ${twoFactor ? 'bg-secondary/20 text-secondary' : 'bg-slate-800 text-slate-400'}`;
    }
}

window.onAuth = (callback) => {
    if (window.currentUser) {
        callback(window.currentUser);
    } else {
        window.authCallbacks.push(callback);
    }
};

function initAuthListener() {
    onAuthStateChanged(auth, (user) => {
        const isAuthPage = window.location.pathname === '/login' || window.location.pathname === '/register';

        if (user) {
            window.currentUser = user;
            localStorage.setItem('currentUser', JSON.stringify({ email: user.email, name: user.displayName }));

            updateUIForUser(user);
            startRESTListeners(user.email);

            while (window.authCallbacks.length > 0) {
                const cb = window.authCallbacks.shift();
                cb(user);
            }

            if (isAuthPage) {
                window.location.href = '/';
            }
        } else {
            window.currentUser = null;
            localStorage.removeItem('currentUser');

            window.cachedMovements = [];
            window.cachedInvestments = [];
            window.cachedPayments = [];
            window.cachedDebts = [];

            const balanceEl = document.querySelector('h2.text-5xl');
            if (balanceEl) balanceEl.textContent = '$0.00';

            ['movements-table-body', 'portfolio-table-body', 'payments-table-body', 'debts-table-body'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.innerHTML = '';
            });

            if (!isAuthPage) {
                window.location.href = '/login';
            }
        }
    });
}

function updateUIForUser(user) {
    const authContainer = document.getElementById('auth-ui-container');
    const loginBtn = document.getElementById('login-btn');

    if (authContainer && loginBtn) {
        loginBtn.style.display = 'none';

        const dropdownName = document.getElementById('dropdown-user-name');
        const dropdownEmail = document.getElementById('dropdown-user-email');
        if (dropdownName) dropdownName.textContent = user.displayName || 'Usuario';
        if (dropdownEmail) dropdownEmail.textContent = user.email;
    }

    const nameEl = document.getElementById('user-name');
    const initialsEl = document.getElementById('user-initials');
    const sidebarName = document.getElementById('sidebar-user-name');
    const sidebarInitials = document.getElementById('sidebar-initials');

    const displayName = user.displayName || 'Usuario';
    const initials = (user.displayName || user.email).split(/[ @.]/).map(n => n[0]).join('').toUpperCase().substring(0, 2);

    if (nameEl) nameEl.textContent = displayName;
    if (sidebarName) sidebarName.textContent = displayName;
    if (initialsEl) initialsEl.textContent = initials;
    if (sidebarInitials) sidebarInitials.textContent = initials;
}

window.cachedMovements = [];
window.cachedInvestments = [];
window.cachedPayments = [];

function initGlobalSearch() {
    const searchInput = document.getElementById('global-search');
    if (!searchInput) return;

    searchInput.addEventListener('input', (e) => {
        dashboardState.searchTerm = e.target.value.toLowerCase();
        refreshAllUI();
    });
}

function refreshAllUI() {
    if (window.cachedMovements) processMovements(window.cachedMovements);
    if (window.cachedInvestments) processInvestments(window.cachedInvestments);
    if (window.cachedPayments) processPayments(window.cachedPayments);
    
    if (window.location.pathname === '/investments' && window.updateInvestmentsUI) {
        window.updateInvestmentsUI(window.cachedInvestments, dashboardState.searchTerm);
    }
    if (window.location.pathname === '/debts' && window.updateDebtsUI) {
        window.updateDebtsUI(window.cachedDebts, dashboardState.searchTerm);
    }
}

async function startRESTListeners(email) {
    await fetchAllData(email);
    setInterval(() => fetchAllData(email), 30000);
}

async function fetchAllData(email) {
    try {
        const resMovements = await fetch(`/api/movements?email=${email}`);
        const dataMoves = await resMovements.json();
        if (dataMoves.status === 'success') {
            window.cachedMovements = dataMoves.data;
            processMovements(dataMoves.data);
            if (window.location.pathname === '/dashboard' || window.location.pathname === '/') {
                if (window.updateDashboardCharts) window.updateDashboardCharts(dataMoves.data);
            }
        }

        const resInvestments = await fetch(`/api/investments?email=${email}`);
        const dataInvestments = await resInvestments.json();
        if (dataInvestments.status === 'success') {
            window.cachedInvestments = dataInvestments.data;
            processInvestments(dataInvestments.data);
            if (window.location.pathname === '/portfolio' && window.updatePortfolioUI) {
                window.updatePortfolioUI(dataInvestments.data);
            }
        }

        const resPayments = await fetch(`/api/payments?email=${email}`);
        const dataPayments = await resPayments.json();
        if (dataPayments.status === 'success') {
            window.cachedPayments = dataPayments.data;
            processPayments(dataPayments.data);
            if (window.location.pathname === '/payments' && window.updatePaymentsUI) {
                window.updatePaymentsUI(dataPayments.data);
            }
        }
        const resDebts = await fetch(`/api/debts?email=${email}`);
        const dataDebts = await resDebts.json();
        if (dataDebts.status === 'success') {
            window.cachedDebts = dataDebts.data;
            if (window.location.pathname === '/debts' && window.updateDebtsUI) {
                window.updateDebtsUI(dataDebts.data);
            }
        }
    } catch (err) {
        console.error("Error fetching data:", err);
    }
}

function processMovements(movements) {
    let filtered = movements;
    if (dashboardState.searchTerm) {
        const s = dashboardState.searchTerm;
        filtered = filtered.filter(m =>
            (m.concept || '').toLowerCase().includes(s) ||
            (m.category || '').toLowerCase().includes(s)
        );
    }

    const totalIncome = filtered.filter(m => m.type === 'income').reduce((acc, m) => acc + m.amount, 0);
    const totalExpenses = filtered.filter(m => m.type === 'expense').reduce((acc, m) => acc + m.amount, 0);
    const balance = totalIncome - totalExpenses;

    const balanceEl = document.getElementById('dashboard-balance') || document.querySelector('h2.text-5xl');
    const incomeEl = document.getElementById('dashboard-income');
    const expenseEl = document.getElementById('dashboard-expenses');

    if (balanceEl) balanceEl.textContent = window.formatAmount(balance);
    if (incomeEl) incomeEl.textContent = window.formatAmount(totalIncome);
    if (expenseEl) expenseEl.textContent = window.formatAmount(totalExpenses);

    if (window.location.pathname === '/study') updateStudyStats(filtered);
}

function processInvestments(investments) {
    if (window.location.pathname === '/portfolio') {
        updatePortfolioUI(investments);
    }
}

function processPayments(payments) {
    if (window.location.pathname !== '/payments') return;

    const body = document.getElementById('payments-table-body');
    if (!body) return;

    if (payments.length === 0) {
        body.innerHTML = `<tr><td colspan="5" class="px-8 py-10 text-center text-slate-500 italic">No tienes pagos programados aún.</td></tr>`;
        return;
    }

    body.innerHTML = '';
    payments.forEach(p => {
        body.innerHTML += `
            <tr class="hover:bg-white/2 transition-colors">
                <td class="px-8 py-5">
                    <div class="flex items-center gap-3">
                        <p class="text-sm font-bold text-white">${p.service}</p>
                    </div>
                </td>
                <td class="px-8 py-5 text-sm text-slate-300 font-mono">${p.date}</td>
                <td class="px-8 py-5 text-sm text-white font-mono font-bold">${window.formatAmount(p.amount)}</td>
                <td class="px-8 py-5">
                    <span class="px-2 py-1 rounded-md bg-orange-500/10 text-orange-500 text-[10px] font-bold uppercase tracking-wider">${p.status}</span>
                </td>
                <td class="px-8 py-5 text-right">
                    <button class="p-2 hover:bg-white/5 rounded-lg text-secondary transition-all">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>
                    </button>
                </td>
            </tr>
        `;
    });
}

function updatePortfolioUI(investments) {
    const body = document.getElementById('portfolio-table-body');
    if (!body) return;

    if (investments.length === 0) {
        body.innerHTML = `<tr><td colspan="5" class="px-6 py-10 text-center text-slate-500 italic">Tu portafolio está vacío.</td></tr>`;
        return;
    }

    body.innerHTML = '';
    investments.forEach(item => {
        body.innerHTML += `
            <tr class="hover:bg-white/2 transition-colors">
                <td class="px-6 py-4">
                    <div class="flex items-center gap-3">
                        <p class="text-xs font-bold text-white">${item.symbol}</p>
                    </div>
                </td>
                <td class="px-6 py-4 text-white font-mono">${window.formatAmount(item.investment)}</td>
                <td class="px-6 py-4 text-white font-mono">${window.formatAmount(item.current)}</td>
                <td class="px-6 py-4 font-bold text-secondary">${item.pnl}%</td>
                <td class="px-6 py-4 text-right">
                    <button class="text-slate-500 hover:text-white transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="1"/><circle cx="12" cy="5" r="1"/><circle cx="12" cy="19" r="1"/></svg>
                    </button>
                </td>
            </tr>
        `;
    });
}

function updateStudyStats(movements) {
    const totalIncome = movements.filter(m => m.type === 'income').reduce((acc, m) => acc + m.amount, 0);
    const elements = {
        'study-income': totalIncome,
        'study-needs': totalIncome * 0.5,
        'study-wants': totalIncome * 0.3,
        'study-savings': totalIncome * 0.2
    };

    for (let id in elements) {
        const el = document.getElementById(id);
        if (el) el.textContent = window.formatAmount(elements[id]);
    }
}

function initCharts() {
    const chartOptions = {
        series: [{ name: 'Balance', data: [0, 0, 0, 0, 0, 0, 0] }],
        chart: {
            height: 350, type: 'area', toolbar: { show: false }, background: 'transparent', foreColor: '#94a3b8',
            animations: { enabled: true, easing: 'easeinout', speed: 800 }
        },
        colors: ['#00f0ff'],
        fill: { type: 'gradient', gradient: { shadeIntensity: 1, opacityFrom: 0.45, opacityTo: 0.05, stops: [20, 100] } },
        stroke: { curve: 'smooth', width: 3 },
        dataLabels: { enabled: false },
        grid: { borderColor: 'rgba(255, 255, 255, 0.05)', strokeDashArray: 4 },
        xaxis: { categories: ['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom'], axisBorder: { show: false }, axisTicks: { show: false } },
        yaxis: { labels: { formatter: (val) => `$${val.toFixed(0)}` } },
        tooltip: { theme: 'dark', x: { show: false } }
    };

    const chartEl = document.querySelector("#main-chart");
    if (chartEl) {
        mainChart = new ApexCharts(chartEl, chartOptions);
        mainChart.render();
    }
}

async function fetchMarketData() {
    try {
        const response = await fetch('/api/market-data');
        const result = await response.json();
        if (result.status === 'success') {
            const data = result.data;
            if (document.getElementById('btc-price')) {
                document.getElementById('btc-price').textContent = `$${data.btc.price.toLocaleString()}`;
                document.getElementById('eth-price').textContent = `$${data.eth.price.toLocaleString()}`;
            }
        }
    } catch (error) { console.error('Error market data:', error); }
}

function setupRangeButtons() {
    const buttons = document.querySelectorAll('.flex.gap-2 button');
    buttons.forEach(btn => {
        btn.onclick = () => {
            buttons.forEach(b => { b.classList.remove('bg-primary', 'text-black'); b.classList.add('text-slate-500'); });
            btn.classList.add('bg-primary', 'text-black');
            btn.classList.remove('text-slate-500');
        };
    });
}

// Auth Actions
async function logout() {
    try {
        await signOut(auth);
        window.location.href = '/login';
    } catch (error) { console.error('Logout error:', error); }
}

// MFA Implementation
window.enrollMFA = async (phoneNumber) => {
    try {
        const user = auth.currentUser;
        if (!user) throw new Error("No hay usuario autenticado.");

        if (window.recaptchaVerifier) window.recaptchaVerifier.clear();

        window.recaptchaVerifier = new RecaptchaVerifier(auth, 'recaptcha-container', {
            'size': 'invisible'
        });
        
        const session = await multiFactor(user).getSession();
        const verificationId = await (new PhoneAuthProvider(auth)).verifyPhoneNumber(
            { phoneNumber, session }, 
            window.recaptchaVerifier
        );
        return { status: 'success', verificationId };
    } catch (error) {
        console.error('MFA Enrollment error:', error);
        return { status: 'error', message: error.message };
    }
};

window.startMFA = async () => {
    const phoneNumber = prompt("Ingresa tu número de teléfono (formato internacional, ej: +57300...):");
    if (!phoneNumber) return;
    
    const res = await window.enrollMFA(phoneNumber);
    if (res.status === 'success') {
        const code = prompt("Ingresa el código que recibiste por SMS:");
        if (!code) return;
        const confirmResult = await window.confirmMFAEnrollment(res.verificationId, code);
        if (confirmResult.status === 'success') {
            alert("MFA habilitado correctamente.");
            location.reload();
        } else {
            alert("Error al confirmar: " + confirmResult.message);
        }
    } else {
        alert("Error al enrolar: " + res.message);
    }
};

window.confirmMFAEnrollment = async (verificationId, code, label = "Teléfono Personal") => {
    try {
        const user = auth.currentUser;
        const cred = PhoneAuthProvider.credential(verificationId, code);
        const multiFactorAssertion = PhoneMultiFactorGenerator.assertion(cred);
        await multiFactor(user).enroll(multiFactorAssertion, label);
        return { status: 'success' };
    } catch (error) {
        console.error('MFA Confirmation error:', error);
        return { status: 'error', message: error.message };
    }
};

window.unenrollMFA = async (factorId) => {
    try {
        const user = auth.currentUser;
        const enrolledFactors = multiFactor(user).enrolledFactors;
        const factorToUnenroll = factorId ? enrolledFactors.find(f => f.uid === factorId) : enrolledFactors[0];
        if (!factorToUnenroll) throw new Error("No se encontró ningún factor para desactivar.");
        await multiFactor(user).unenroll(factorToUnenroll);
        return { status: 'success' };
    } catch (error) {
        console.error('MFA Unenroll error:', error);
        return { status: 'error', message: error.message };
    }
};

async function resetPassword(email) {
    try {
        await sendPasswordResetEmail(auth, email);
        return { status: 'success', message: 'Correo de restablecimiento enviado.' };
    } catch (error) {
        return { status: 'error', message: error.message };
    }
}

// Global scope exposures
window.logout = logout;
window.resetPassword = resetPassword;
window.toggleProfileDropdown = (e) => {
    if (e) e.stopPropagation();
    const dropdown = document.getElementById('profile-dropdown');
    if (dropdown) {
        dropdown.classList.toggle('opacity-0');
        dropdown.classList.toggle('pointer-events-none');
        dropdown.classList.toggle('translate-y-2');
    }
};

// Movement/Investment Submit Override
window.firebaseAddData = async (type, data) => {
    if (!window.currentUser) return { status: 'error', message: 'No user logged in' };

    try {
        let endpoint = '/api/add-movement';
        let payload = { email: window.currentUser.email };

        if (type === 'invertir') {
            endpoint = '/api/add-investment';
            payload.investment = data;
        } else if (type === 'gasto' || type === 'ingreso' || type === 'movimiento') {
            endpoint = '/api/add-movement';
            payload.movement = data;
        } else if (type === 'pago') {
            endpoint = '/api/add-payment';
            payload.payment = data;
        } else if (type === 'deuda') {
            endpoint = '/api/add-debt';
            payload.debt = data;
        }

        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        if (result.status === 'success') {
            await fetchAllData(window.currentUser.email);
            return { status: 'success' };
        } else {
            return { status: 'error', message: result.message || 'Error saving data' };
        }
    } catch (error) {
        console.error('Error adding data:', error);
        return { status: 'error', message: error.message };
    }
};

window.exportInvestmentGuide = async () => {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    const user = window.currentUser;

    if (!user) return alert("Por favor, inicia sesión para exportar tu guía.");

    doc.setFillColor(4, 7, 13);
    doc.rect(0, 0, 210, 40, 'F');
    doc.setTextColor(0, 240, 255);
    doc.setFontSize(22);
    doc.text("FINANZAS PERSONALES - GUÍA DE INVERSIÓN", 20, 25);

    doc.setTextColor(150, 150, 150);
    doc.setFontSize(10);
    doc.text(`Generado para: ${user.displayName || user.email}`, 20, 35);
    doc.text(`Fecha: ${new Date().toLocaleDateString()}`, 150, 35);

    doc.setTextColor(0, 0, 0);
    doc.setFontSize(14);
    doc.text("1. Tu Estrategia de Ahorro Inteligente", 20, 55);
    doc.setFontSize(11);
    doc.text("Basado en el análisis de tus ingresos, tu meta de ahorro mensual (20%) debería ser:", 20, 65);

    const income = document.getElementById('study-income')?.textContent || "$0.00";
    const savings = document.getElementById('study-savings')?.textContent || "$0.00";

    doc.setFontSize(18);
    doc.setTextColor(57, 255, 20);
    doc.text(savings, 20, 75);

    doc.setTextColor(0, 0, 0);
    doc.setFontSize(10);
    doc.text(`Calculado sobre un ingreso total de ${income}`, 20, 82);

    doc.setFontSize(14);
    doc.text("2. Regla 50/30/20", 20, 100);
    doc.setFontSize(11);
    doc.text("- Necesidades (50%): " + (document.getElementById('study-needs')?.textContent || "$0.00"), 25, 110);
    doc.text("- Deseos (30%): " + (document.getElementById('study-wants')?.textContent || "$0.00"), 25, 118);
    doc.text("- Ahorro/Inversión (20%): " + (document.getElementById('study-savings')?.textContent || "$0.00"), 25, 126);

    doc.setFontSize(14);
    doc.text("3. Consejos de Inversión del Mes", 20, 145);
    doc.setFontSize(11);
    const splitText = doc.splitTextToSize(
        "Recuerda diversificar tus activos. No pongas todo tu capital en un solo sector. El interés compuesto trabaja mejor a largo plazo; la paciencia es tu mejor aliada en los mercados volátiles.",
        170
    );
    doc.text(splitText, 20, 155);

    doc.setFontSize(9);
    doc.setTextColor(150, 150, 150);
    doc.text("Finanzas Personales - Tu futuro financiero empieza aquí.", 20, 280);
    doc.text("www.finanzaspersonales.com", 160, 280);

    doc.save("Guia_Inversion_FinanzasPersonales.pdf");
};

const updateMFASettingsUI = () => {
    const container = document.getElementById('mfa-status-container');
    if (!container || !auth.currentUser) return;

    const user = auth.currentUser;
    const enrolledFactors = multiFactor(user).enrolledFactors;

    if (enrolledFactors && enrolledFactors.length > 0) {
        container.innerHTML = `
            <div class="flex items-center gap-4">
                <span class="text-[9px] px-2 py-1 bg-green-500/20 text-green-500 border border-green-500/30 rounded font-black uppercase">Activo</span>
                <button onclick="handleDisableMFA()"
                    class="text-[10px] px-4 py-2 bg-red-500/20 text-red-500 border border-red-500/30 rounded-lg font-black uppercase hover:bg-red-500 hover:text-white transition-all">
                    Desactivar
                </button>
            </div>
        `;
    } else {
        container.innerHTML = `
            <button onclick="startMFA()"
                class="text-[10px] px-4 py-2 bg-primary/20 text-primary border border-primary/30 rounded-lg font-black uppercase hover:bg-primary hover:text-black transition-all">
                Configurar SMS
            </button>
        `;
    }
};

window.handleDisableMFA = async () => {
    if (confirm("¿Estás seguro de que quieres desactivar la autenticación en dos pasos?")) {
        const res = await window.unenrollMFA();
        if (res.status === 'success') {
            alert("MFA desactivado correctamente.");
            location.reload();
        } else {
            alert("Error: " + res.message);
        }
    }
};

onAuthStateChanged(auth, (user) => {
    if (user && location.pathname === '/settings') {
        updateMFASettingsUI();
    }
});
筋
