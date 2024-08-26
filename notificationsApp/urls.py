from django.urls import path
from .views import index, save_fcm_token, success, login, place_order, mark_order_completed, send_notification

urlpatterns = [
    path("", index, name="index"),
    path("success/", success, name="success"),
    path("login/", login, name="login"),
    
    path("place-order/", place_order, name="place_order"),
    path("mark-order-completed/<pk>/", mark_order_completed, name="mark_order_completed"),
    path("save-fcm-token/", save_fcm_token, name="save_fcm_token"),
    
    path('send-notification/', send_notification, name='send_notification'),
]
