from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Plan, Transaction
from django.utils import timezone

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
