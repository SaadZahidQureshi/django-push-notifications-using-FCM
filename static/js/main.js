
Notification.requestPermission()

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/js/firebase-messaging-sw.js', {scope: '/static/js/'})
    .then((registration) => {
        console.log('Service Worker registered with scope:', registration.scope);

        // Initialize Firebase
        if (!firebase.apps.length) {
            firebase.initializeApp({
                // fcm configs here
            });
        }

        const messaging = firebase.messaging();
        messaging.useServiceWorker(registration);
        messaging.onMessage(function(payload){
            console.log(payload)
        })

        messaging.requestPermission()
        .then(() => {
            console.log('Notification permission granted.');
            return messaging.getToken({ vapidKey: 'your vapid key' });
        })
        .then((token) => {
            if (token) {
                console.log('FCM Token:', token);
                saveFcmToken(token);
            } else {
                console.log('No registration token available. Request permission to generate one.');
            }
        })
        .catch((err) => {
            console.log('Unable to get permission to notify.', err);
        });

    }).catch((err) => {
        console.log('Service Worker registration failed:', err);
    });
}



// Function to save FCM token (ensure this endpoint is correctly set up)
async function saveFcmToken(token) {
    let response = await fetch('/save-fcm-token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') 
        },
        body: JSON.stringify({ fcm_token: token })
    });
    console.log(response)
    if (response.ok){
        let re = await response.json();
        console.log(re)
    }
}

// Example function to get CSRF token from cookies
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}


async function send(){
    let response = await fetch('place-order/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') 
        },
        body: null
    });
    console.log(response)
    if (response.ok){
        let re = await response.json();
        console.log(re)
    }
}