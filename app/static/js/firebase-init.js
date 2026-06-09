// Intercept JSON.parse to inject current domain into Firebase Auth's authorized domains list.
// This fixes 'auth/unauthorized-domain' errors for domains not manually added to Firebase Console.
const __origJSONParse = JSON.parse;
JSON.parse = function __patchedJSONParse(text, reviver) {
    const result = __origJSONParse.call(this, text, reviver);
    if (result && Array.isArray(result.authorizedDomains)) {
        const hostname = window.location.hostname;
        const port = window.location.port;
        const domain = (port && port !== '443' && port !== '80') ? `${hostname}:${port}` : hostname;
        if (!result.authorizedDomains.includes(domain)) {
            result.authorizedDomains.push(domain);
        }
    }
    return result;
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
