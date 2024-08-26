from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from firebase_admin import messaging

from Notification_FCM.helper import send_notification_to_admin, send_notification_to_buyer, get_buyer_fcm_token
from .models import FCMDevice, User, Order

# Create your views here.


def index(request):
    return render(request, "index.html")

def success(request):
    return render(request, "success.html")

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')  
        else:
            print(form.errors)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
        
# ------------------------------------------------------

@csrf_exempt
@login_required
def place_order(request):
    if request.method == 'POST':
        # Your existing order placement logic here
        order = Order.objects.create(
            user=request.user, subtotal=180, tax=20, total=200, status=Order.Status.PLACED
        )
        # Send notification to admin
        response = send_notification_to_admin(order)
        return JsonResponse({'status': True, 'message': 'sent'})

    return JsonResponse({'status': 'Failed', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
@login_required
def mark_order_completed(request, pk):
    if request.method == 'POST':
        order = Order.objects.get(id=pk)
        order.status = Order.Status.COMPLETED
        order.save()

        # Send notification to buyer
        buyer_token = get_buyer_fcm_token(order.user)
        if buyer_token:
            responce = send_notification_to_buyer(buyer_token, order)

        print(responce)
        return redirect('success')

    return JsonResponse({'status': 'Failed', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
@login_required
def save_fcm_token(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        fcm_token = data.get('fcm_token')

        if not fcm_token:
            return JsonResponse({'status': 'Failed', 'message': 'FCM token missing'}, status=400)

        # Save token in the FCMDevice model
        FCMDevice.objects.update_or_create(user=request.user, defaults={'fcm_token': fcm_token})

        return JsonResponse({'status': 'Token saved'})

    return JsonResponse({'status': 'Failed', 'message': 'Invalid request method'}, status=405)




# ------------------------------------------------------
@csrf_exempt
def send_notification(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token = data.get('token')
        # message_title = data.get('title', 'Default Title')
        # message_body = data.get('body', 'Default Body')

        message_title = "New Notification"
        message_body = "this is just body of notification"
    
        if not token:
            return JsonResponse({'error': 'No token provided'}, status=400)

        message = messaging.Message(
            notification=messaging.Notification(
                title=message_title,
                body=message_body,
            ),
            token=token,
        )

        try:
            response = messaging.send(message)
            return JsonResponse({'message': 'Notification sent', 'response': response})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)