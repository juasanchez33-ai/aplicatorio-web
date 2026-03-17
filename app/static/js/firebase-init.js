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
    browserSessionPersistence
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

export { 
    auth, 
    GoogleAuthProvider,
    signInWithEmailAndPassword,
    signInWithPopup,
    onAuthStateChanged,
    signOut,
    sendPasswordResetEmail,
    updateProfile,
    createUserWithEmailAndPassword,
    EmailAuthProvider,
    reauthenticateWithCredential
};
