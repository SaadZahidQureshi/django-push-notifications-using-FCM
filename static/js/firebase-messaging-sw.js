

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
  // fcm configs
 
});

// Retrieve an instance of Firebase Messaging
const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);

  self.registration.showNotification(notificationTitle, notificationOptions);
});
