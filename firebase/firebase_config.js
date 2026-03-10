// Firebase Configuration for Proyecto_Finanzas_80
// Replace with your actual project credentials

const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "proyecto-finanzas-80.firebaseapp.com",
  projectId: "proyecto-finanzas-80",
  storageBucket: "proyecto-finanzas-80.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID",
  measurementId: "YOUR_MEASUREMENT_ID"
};

// Initialize Firebase
const app = firebase.initializeApp(firebaseConfig);
const db = firebase.firestore(app);
const auth = firebase.auth(app);

export { db, auth };
