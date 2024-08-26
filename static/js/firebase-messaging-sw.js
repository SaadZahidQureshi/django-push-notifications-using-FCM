

self.addEventListener("notificationclick", (event) => {
    console.log("Click:", event.notification);
    event.notification.close();
    event.waitUntil(clients.matchAll({ type: "window" }).then((clientList) => {
        for (const client of clientList) {
            if (client.url.includes(self.location.origin) && "focus" in client) return client.focus();
        }
        if (clients.openWindow && Boolean(self.location.origin)) return clients.openWindow(self.location.origin);
    }).catch(err => {
        console.log("There was an error waitUntil:", err);
    }));
});


importScripts('https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.10.1/firebase-messaging.js');

// Initialize Firebase in the service worker
firebase.initializeApp({
  apiKey: "AIzaSyBv51-4hNiLPbReyBWeR3ncI7o98zZiIoY",
  authDomain: "underoneroof-a0b22.firebaseapp.com",
  projectId: "underoneroof-a0b22",
  storageBucket: "underoneroof-a0b22.appspot.com",
  messagingSenderId: "180332848840",
  appId: "1:180332848840:web:8a0214c135f87560cc27fd",
  measurementId: "G-RNP5F9N3NQ"
});

// Retrieve an instance of Firebase Messaging
const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);

  self.registration.showNotification(notificationTitle, notificationOptions);
});
