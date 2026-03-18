import {
    auth,
    onAuthStateChanged,
    signOut,
    sendPasswordResetEmail,
    reauthenticateWithCredential,
    EmailAuthProvider
} from '/static/js/firebase-init.js';

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
    setupSecurityListeners();
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
        const isAuthPage = window.location.pathname === '/login' || window.location.pathname === '/register' || window.location.pathname === '/';

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
                const isVerified = sessionStorage.getItem('fp_security_verified') === 'true';
                if (!isVerified) {
                    window.checkAndPromptSecurityOTP(user).then(isLocked => {
                        if (!isLocked && window.location.pathname !== '/dashboard') {
                            window.location.href = '/dashboard';
                        }
                    });
                } else if (window.location.pathname !== '/dashboard') {
                    window.location.href = '/dashboard';
                }
            } else {
                window.checkAndPromptSecurityOTP(user);
            }
            
            if (window.location.pathname === '/settings') {
                updateMFASettingsUI();
            }
            
            // MFA Activation Prompt Logic (Post-Login)
            if (window.location.pathname === '/' || window.location.pathname === '/dashboard') {
                setTimeout(() => window.checkAndPromptMFA(user), 500);
            }

        } else {
            window.currentUser = null;
            localStorage.removeItem('currentUser');
            sessionStorage.removeItem('fp_security_verified');
            
            if (document.getElementById('auth-loading-overlay')) {
                document.getElementById('auth-loading-overlay').classList.add('opacity-0');
                setTimeout(() => document.getElementById('auth-loading-overlay').classList.add('hidden'), 300);
            }
            if (document.getElementById('login-main-content')) {
                document.getElementById('login-main-content').classList.remove('hidden');
                // Removed opacity-0 just in case there's an animation class
            }

            window.cachedMovements = [];
            window.cachedPayments = [];
            window.cachedDebts = [];

            const balanceEl = document.querySelector('h2.text-5xl');
            if (balanceEl) balanceEl.textContent = '$0.00';

            ['movements-table-body', 'payments-table-body', 'debts-table-body'].forEach(id => {
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
    if (window.cachedPayments) processPayments(window.cachedPayments);
    
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
window.logout = async function() {
    try {
        console.log("Iniciando cierre de sesión profundo...");
        
        // 1. Clear ALL relevant local storage keys
        const keysToClear = [
            'currentUser', 
            'fp_currentUser', 
            'fp_user_email', 
            'fp_notifications',
            'mfaVerificationId'
        ];
        keysToClear.forEach(key => localStorage.removeItem(key));
        
        // Clear session specific security status
        sessionStorage.removeItem('fp_security_verified');
        sessionStorage.clear(); // Clear all session storage for safety
        
        // 2. Sign out from Firebase if possible
        if (auth.currentUser) {
            await signOut(auth);
            console.log("Sesión de Firebase cerrada de forma segura.");
        }
    } catch (error) { 
        console.error('Error durante el cierre de sesión:', error);
    } finally {
        // 3. ALWAYS redirect to login as a final step
        window.location.href = '/login';
    }
};

// --- CUSTOM SECURITY ACTIVATION (Replacing legacy MFA) ---
window.startMFA = async () => {
    const user = window.currentUser || auth.currentUser;
    if (!user) return alert("Debes iniciar sesión primero.");

    if (confirm("¿Deseas activar la seguridad por correo electrónico? Recibirás un código para validar tus inicios de sesión.")) {
        try {
            const response = await fetch('/api/profile', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: user.email, two_factor_enabled: true })
            });
            const res = await response.json();
            if (res.status === 'success') {
                alert("¡Seguridad activada con éxito! Por favor, inicia sesión nuevamente.");
                if (window.logout) {
                    window.logout();
                } else {
                    signOut(auth).then(() => { window.location.href = '/login'; });
                }
            } else {
                alert("Error: " + res.message);
            }
        } catch (err) {
            alert("Error de conexión al activar seguridad.");
        }
    }
};

window.unenrollMFA = async () => {
    const user = window.currentUser || auth.currentUser;
    if (!user) return { status: 'error', message: 'No hay usuario' };
    
    try {
        // Sync with backend (Set two_factor_enabled to false)
        const response = await fetch('/api/profile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: user.email, two_factor_enabled: false })
        });
        const result = await response.json();
        return result;
    } catch (err) {
        return { status: 'error', message: err.message };
    }
};

// Legacy placeholders cleaned up
window.enrollMFA = async () => { console.log("Legacy enrollment skipped"); };
window.submitMFAPhone = async () => {};
window.submitMFACode = async () => {};
window.confirmMFAEnrollment = async () => {};

async function resetPassword(email) {
    try {
        await sendPasswordResetEmail(auth, email);
        return { status: 'success', message: 'Correo de restablecimiento enviado.' };
    } catch (error) {
        return { status: 'error', message: error.message };
    }
}

// Global scope exposures
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

        if (type === 'gasto' || type === 'ingreso' || type === 'movimiento') {
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



window.handlePasswordReset = async () => {
    const user = auth.currentUser;
    if (!user) return alert("Debes estar conectado para realizar esta acción.");
    
    if (confirm(`¿Enviar un correo de restablecimiento a ${user.email}?`)) {
        const res = await window.resetPassword(user.email);
        if (res.status === 'success') {
            alert("Correo enviado. Revisa tu bandeja de entrada.");
        } else {
            alert("Error: " + res.message);
        }
    }
};

const updateMFASettingsUI = async () => {
    const container = document.getElementById('mfa-status-container');
    if (!container) return;

    const user = window.currentUser || auth.currentUser;
    if (!user) {
        container.innerHTML = `<p class="text-[10px] text-slate-600 font-bold uppercase">Sesión no detectada</p>`;
        return;
    }

    try {
        const response = await fetch(`/api/profile?email=${user.email}`);
        const result = await response.json();
        const isEnabled = result.status === 'success' && result.data.two_factor_enabled;

        if (isEnabled) {
            container.innerHTML = `
                <div class="flex items-center gap-4 animate-fade-in">
                    <span class="text-[9px] px-2.5 py-1 bg-primary/10 text-primary border border-primary/20 rounded font-black uppercase tracking-widest shadow-[0_0_15px_rgba(0,240,255,0.1)]">Protegido</span>
                    <button onclick="handleDisableMFA()"
                        class="text-[9px] px-4 py-2 bg-red-500/10 text-red-500 border border-red-500/20 rounded-lg font-black uppercase tracking-widest hover:bg-red-500 hover:text-white transition-all">
                        Desactivar
                    </button>
                </div>
            `;
        } else {
            container.innerHTML = `
                <button onclick="startMFA()"
                    class="text-[9px] px-6 py-2 bg-primary/20 text-primary border border-primary/30 rounded-lg font-black uppercase tracking-widest hover:bg-primary hover:text-black transition-all shadow-lg hover:shadow-primary/20 animate-pulse">
                    Configurar Seguridad
                </button>
            `;
        }
    } catch (err) {
        container.innerHTML = `<p class="text-[9px] text-red-500 opacity-50">Error al cargar estado</p>`;
    }
};

window.handleDisableMFA = async () => {
    if (confirm("¿Estás seguro de que quieres desactivar la autenticación en dos pasos? Esto reducirá la seguridad de tu cuenta.")) {
        const res = await window.unenrollMFA();
        if (res.status === 'success') {
            alert("MFA desactivado correctamente.");
            location.reload();
        } else {
            alert("Error: " + res.message);
        }
    }
};

// Redundant listener removed. Auth state is handled in initAuthListener.

// --- GLOBAL MFA FLOW (Post-Login Activation) ---
window.checkAndPromptMFA = async (user) => {
    console.log("checkAndPromptMFA: Iniciando validación...");
    const path = window.location.pathname;
    // Only prompt on Dashboard/Home
    if (path !== '/' && path !== '/dashboard') {
        return;
    }
    
    // Check storage for skip
    const skipped = sessionStorage.getItem('fp_mfa_prompt_skipped');
    // Clear old localStorage flag if it exists so we don't accidentally hide it forever
    localStorage.removeItem('fp_mfa_prompt_skipped');
    
    if (skipped === 'true' && !window.location.search.includes('force_2fa')) return;

    try {
        const response = await fetch(`/api/profile?email=${user.email}`);
        const result = await response.json();
        
        if (result.status === 'success' && !result.data.two_factor_enabled) {
            const prompt = document.getElementById('mfa-activation-prompt');
            if (prompt) {
                prompt.classList.remove('hidden');
                
                const confirmBtn = document.getElementById('activate-mfa-confirm-btn');
                const skipBtn = document.getElementById('activate-mfa-skip-btn');

                confirmBtn.onclick = async () => {
                    if (confirmBtn.disabled) return;
                    confirmBtn.disabled = true;
                    const originalText = confirmBtn.innerText;
                    confirmBtn.innerText = "Activando...";
                    
                    try {
                        const response = await fetch('/api/profile', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ email: user.email, two_factor_enabled: true })
                        });
                        const res = await response.json();
                        if (res.status === 'success') {
                            confirmBtn.innerText = "Protegido. Cerrando sesión...";
                            setTimeout(() => {
                                if (window.logout) {
                                    window.logout();
                                } else {
                                    window.location.href = '/login';
                                }
                            }, 1200);
                            return; // Do not re-enable the button
                        } else {
                            alert("Error al activar MFA: " + (res.message || "Desconocido"));
                        }
                    } catch (error) {
                        alert("Error de red: " + error.message);
                    }
                    
                    confirmBtn.disabled = false;
                    confirmBtn.innerText = originalText;
                };

                skipBtn.onclick = () => {
                    prompt.classList.add('hidden');
                    sessionStorage.setItem('fp_mfa_prompt_skipped', 'true');
                };
            }
        }
    } catch (err) {
        console.error("Error setting up security:", err);
    }
};

// --- CUSTOM SECURITY SYSTEM (OTP) ---
window.submitSecurityOTP = async () => {
    const input = document.getElementById('security-otp-input');
    const errorEl = document.getElementById('security-otp-error');
    const code = input.value.trim();
    
    if (!code || code.length < 6) return;

    const btn = document.getElementById('security-otp-confirm-btn');
    if (btn.disabled) return;
    
    btn.disabled = true;
    const originalText = btn.innerText;
    btn.innerText = "Verificando...";
    errorEl.classList.add('hidden');

    try {
        const emailInput = document.getElementById('security-otp-email');
        const email = emailInput ? emailInput.value.trim() : null;
        
        if (!email) throw new Error("Email no detectado");
        
        const response = await fetch('/api/security/verify-otp', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, code: code })
        });
        const result = await response.json();

        if (result.status === 'success') {
            sessionStorage.setItem('fp_security_verified', 'true');
            const modal = document.getElementById('global-security-otp-modal');
            if (modal) modal.classList.add('hidden');
            
            window.location.href = '/';
        } else {
            errorEl.classList.remove('hidden');
            errorEl.querySelector('p').textContent = result.message || "Código incorrecto";
        }
    } catch (err) {
        console.error("Error en verify-otp:", err);
        alert("Error de conexión al verificar el código.");
    } finally {
        btn.disabled = false;
        btn.innerText = originalText;
    }
};

window.resendSecurityOTP = async () => {
    const emailInput = document.getElementById('security-otp-email');
    const email = emailInput ? emailInput.value.trim() : null;
    const btn = document.getElementById('security-otp-send-btn');
    
    if (!email) return alert("Por favor, ingresa un correo electrónico.");
    if (btn.disabled) return;

    btn.disabled = true;
    const originalText = btn.innerText;
    btn.innerText = "...";

    try {
        const response = await fetch('/api/security/send-otp', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email })
        });
        const result = await response.json();
        if (result.status === 'success') {
            alert("Código enviado con éxito.");
        } else {
            alert("Error: " + result.message);
        }
    } catch (err) {
        alert("Error al enviar el código.");
    } finally {
        btn.disabled = false;
        btn.innerText = originalText;
    }
};

function setupSecurityListeners() {
    document.addEventListener('click', (e) => {
        const sendBtn = e.target.closest('#security-otp-send-btn');
        const confirmBtn = e.target.closest('#security-otp-confirm-btn');
        
        if (sendBtn) {
            e.preventDefault();
            window.resendSecurityOTP();
        }
        if (confirmBtn) {
            e.preventDefault();
            window.submitSecurityOTP();
        }
    });
}

window.checkAndPromptSecurityOTP = async (user) => {
    // Si ya verificamos en esta sesión, no molestar
    if (sessionStorage.getItem('fp_security_verified') === 'true') return false;

    try {
        const response = await fetch(`/api/profile?email=${user.email}`);
        const result = await response.json();
        
        // Si el usuario tiene habilitado el 2FA en nuestro backend
        if (result.status === 'success' && result.data.two_factor_enabled) {
            console.log("Seguridad detectada. Mostrando modal y solicitando OTP automáticamente...");
            
            // Mostrar modal
            const modal = document.getElementById('global-security-otp-modal');
            const emailInput = document.getElementById('security-otp-email');
            
            if (modal) {
                // Pre-llenar con el correo de la cuenta
                if (emailInput && !emailInput.value) {
                    const storedEmail = localStorage.getItem('fp_user_email');
                    emailInput.value = user.email || storedEmail || "";
                }
                modal.classList.remove('hidden');
                
                // Disparar envío de OTP automáticamente
                try {
                    const otpRes = await fetch('/api/security/send-otp', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ email: user.email })
                    });
                    const otpData = await otpRes.json();
                    if(otpData.status === 'success') {
                        // Avisar al usuario discretamente
                        const toast = document.createElement('div');
                        toast.className = "fixed top-5 left-1/2 -translate-x-1/2 bg-primary/20 border border-primary text-primary px-6 py-3 rounded-full text-xs font-black uppercase tracking-widest animate-fade-in z-[300]";
                        toast.innerText = "Código enviado a tu correo";
                        document.body.appendChild(toast);
                        setTimeout(() => toast.remove(), 4000);
                    }
                } catch(e) {
                    console.error("No se pudo auto-enviar el OTP", e);
                }
                
            } else {
                console.error("No se encontró el modal de seguridad global");
            }
            return true; // Indica que se activó el bloqueo
        }
    } catch (err) {
        console.error("Error al verificar estado de seguridad:", err);
    }
    return false;
};
