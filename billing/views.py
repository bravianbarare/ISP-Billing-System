from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Plan, Transaction
from django.utils import timezone
from django.contrib import messages


def home(request):
    return render(request, 'billing/home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'billing/login.html', {'error': 'Invalid credentials'})
    return render(request, 'billing/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    plans = Plan.objects.all()
    return render(request, 'billing/dashboard.html', {'plans': plans})

@login_required
def purchase_plan(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    if request.method == 'POST':
        # Simulate payment confirmation
        Transaction.objects.create(
            user=request.user,
            plan=plan,
            amount_paid=plan.price,
            transaction_date=timezone.now()
        )
        return render(request, 'billing/success.html', {'plan': plan})
    return render(request, 'billing/purchase.html', {'plan': plan})

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'billing/history.html', {'transactions': transactions})

# register new user
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return redirect('register')

        # Create a new user
        user = User.objects.create_user(username=username, password=password, email=email)

        # Send a confirmation email
        send_mail(
            'Registration Successful',
            f'Hello {username},\n\nThank you for registering with ISP Billing System!',
            settings.EMAIL_HOST_USER,  # From email
            [email],  # To email
            fail_silently=False,
        )

        # Redirect to login page after successful registration
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('login')
    return render(request, 'billing/register.html')
