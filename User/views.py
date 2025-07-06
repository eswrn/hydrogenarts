from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import PromptLog
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('generate')
    return render(request, 'user/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('generate')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'user/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def prompt_log_view(request):
    logs = PromptLog.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user/prompt_logs.html', {'logs': logs})
