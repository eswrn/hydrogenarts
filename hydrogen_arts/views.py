from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from image_generator.logic import generate_image_from_prompt
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        if prompt:
            data, status = generate_image_from_prompt(prompt)
            if status == 200:
                return render(request, 'image_generator/generate.html', {'image_path': data.get('image_path')})
            else:
                return render(request, 'image_generator/generate.html', {'error': data.get('error')})

    return render(request, 'image_generator/generate.html')

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('generate')
    else:
        form = UserCreationForm()
    return render(request, 'hydrogen_arts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('generate')
    else:
        form = AuthenticationForm()
    return render(request, 'hydrogen_arts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
