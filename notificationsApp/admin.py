from django.contrib import admin
from .models import User, FCMDevice, Order, Notification

# Register your models here.

admin.site.register(User)
admin.site.register(FCMDevice)
admin.site.register(Order)
admin.site.register(Notification)