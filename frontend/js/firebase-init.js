import { initializeApp, getApps, getApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { 
    getAuth, 
    GoogleAuthProvider,
    PhoneAuthProvider,
    PhoneMultiFactorGenerator,
    multiFactor,
    RecaptchaVerifier,
    getMultiFactorResolver
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
const auth = getAuth(app);
export { 
    auth, 
    db, 
    googleProvider,
    PhoneAuthProvider,
    PhoneMultiFactorGenerator,
    multiFactor,
    RecaptchaVerifier,
    getMultiFactorResolver
};
