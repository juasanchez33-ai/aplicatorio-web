// Intercept fetch to inject current domain into Firebase Auth's authorized domains list.
// Firebase Auth SDK v10 uses FetchProvider which resolves self.fetch dynamically.
// This fixes 'auth/unauthorized-domain' for any domain without Firebase Console changes.
const __origFetch = window.fetch;
window.fetch = function __patchedFetch(input, init) {
    return __origFetch.call(window, input, init).then(async response => {
        const url = (typeof input === 'string' ? input : input?.url) || '';
        if (url.includes('/v1/projects') && response.ok) {
            try {
                const cloned = response.clone();
                const data = await cloned.json();
                if (data.authorizedDomains && Array.isArray(data.authorizedDomains)) {
                    const hostname = window.location.hostname;
                    const port = window.location.port;
                    const domain = (port && port !== '443' && port !== '80') ? `${hostname}:${port}` : hostname;
                    if (!data.authorizedDomains.includes(domain)) {
                        data.authorizedDomains.push(domain);
                    }
                    return new Response(JSON.stringify(data), {
                        status: response.status,
                        statusText: response.statusText,
                        headers: response.headers
                    });
                }
            } catch (e) {
                // Ignore parsing errors — let the original response through
            }
        }
        return response;
    });
};

import { initializeApp, getApps, getApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { 
    getAuth, 
    GoogleAuthProvider,
    signInWithEmailAndPassword,
    signInWithPopup,
    onAuthStateChanged,
    signOut,
    sendPasswordResetEmail,
    updateProfile,
    createUserWithEmailAndPassword,
    EmailAuthProvider,
    reauthenticateWithCredential,
    setPersistence,
    browserSessionPersistence,
    updateEmail,
    deleteUser
} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";

const firebaseConfig = {
    apiKey: "AIzaSyDWbZ9lFdPKJ5xE8sJR7jAsm0x7bOaOcO4",
    authDomain: "financepro-dac5d.firebaseapp.com",
    projectId: "financepro-dac5d",
    storageBucket: "financepro-dac5d.firebasestorage.app",
    messagingSenderId: "1071490211566",
    appId: "1:68074149213:web:fec86553c8e58642f444b4",
    measurementId: "G-RS98EW7GEC"
};

// Initialize Firebase with singleton pattern
const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApp();
// Initialize Firebase Auth, set language and persistence
const auth = getAuth(app);
auth.languageCode = 'es';
setPersistence(auth, browserSessionPersistence);

const db = getFirestore(app);

export { 
    auth, 
    db,
    GoogleAuthProvider,
    signInWithEmailAndPassword,
    signInWithPopup,
    onAuthStateChanged,
    signOut,
    sendPasswordResetEmail,
    updateProfile,
    createUserWithEmailAndPassword,
    EmailAuthProvider,
    reauthenticateWithCredential,
    updateEmail,
    deleteUser
};
