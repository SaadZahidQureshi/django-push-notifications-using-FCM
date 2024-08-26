from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.


# Create your models here.
class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    
    class Role(models.TextChoices):
        USER = 'user', ('User')
        ADMIN = 'admin', ('Admin')
        
    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = ['first_name']
    username = None
    email = models.EmailField(unique=True)
    role=models.CharField(max_length=50, choices=Role.choices, default=Role.USER.value)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    objects = CustomUserManager()


class FCMDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="devices")
    fcm_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.fcm_token}"
    

class Order(models.Model):
    
    class Status(models.TextChoices):
        PLACED = 'placed', ('Placed')
        COMPLETED = 'completed', ('Completed')

    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PLACED.value)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.email}"
    


class Notification(models.Model):

    class RECIPIENT_TYPE_CHOICES(models.TextChoices):
        USER = 'user', ('User')
        ADMIN = 'admin', ('Admin')

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    recipient_type = models.CharField(max_length=10, choices=RECIPIENT_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.email}: {self.title}"

    class Meta:
        ordering = ['-created_at']  # Orders by most recent notifications first