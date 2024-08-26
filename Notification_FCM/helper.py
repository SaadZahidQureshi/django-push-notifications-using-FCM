import firebase_admin
from firebase_admin import messaging
from notificationsApp.models import FCMDevice, User, Notification

def send_notification_to_admin(order):
    try:
        # Retrieve admin FCM tokens
        admin_tokens = list(get_admin_fcm_tokens())
        
        response = None  # Initialize the response variable
        for token in admin_tokens:
            message = messaging.Message(
                notification=messaging.Notification(
                    title="New Order",
                    body=f"A new order with ID {order.id} has been placed.",
                ),
                token=token,
            )
            response = messaging.send(message)
            print('Successfully sent message to admin:', response)
            
        # Save the notification in the database
        for admin in User.objects.filter(role=User.Role.ADMIN):
            Notification.objects.create(
                recipient=admin,
                recipient_type=Notification.RECIPIENT_TYPE_CHOICES.ADMIN,
                title="New Order",
                message=f"A new order with ID {order.id} has been placed."
            )
        
        return response  # Return the last response (if needed)
    
    except Exception as e:
        print(e)


def send_notification_to_buyer(buyer_device_token, order):
    message = messaging.Message(
        notification=messaging.Notification(
            title="Order Completed",
            body=f"Your order with ID {order.id} has been completed.",
        ),
        token=buyer_device_token,
    )

    response = messaging.send(message)
    print('Successfully sent message to buyer:', response)
    
    
    # Save the notification in the database
    Notification.objects.create(
        recipient=order.user,
        recipient_type=Notification.RECIPIENT_TYPE_CHOICES.USER,
        title="Order Completed",
        message=f"Your order with ID {order.id} has been completed."
    )

    return response

# Helper Functions

def get_admin_fcm_tokens():
    # Retrieve all admin users with a specific role
    admin_users = User.objects.filter(role=User.Role.ADMIN)
    admin_tokens = FCMDevice.objects.filter(user__in=admin_users).values_list('fcm_token', flat=True)
    return admin_tokens

def get_buyer_fcm_token(buyer):
    # Retrieve buyer's FCM token from the FCMDevice model
    return FCMDevice.objects.filter(user=buyer).values_list('fcm_token', flat=True).first()
