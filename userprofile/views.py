# djauth/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.urls import reverse
from .models import Profile
from .forms import UserForm, ProfileForm
from django.contrib.auth.decorators import login_required

def index(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None  # or create one here if you prefer

        context = {
            'user': request.user,
            'profile': profile
        }
        messages.success(request, "Welcome to the home page!")
        return render(request, 'index.html', context)
    
    return render(request, 'index.html')
def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if password != confirm_password:
            messages.warning(request, "Passwords don't match.")
            return redirect('signup')

        if len(password) < 8:
            messages.warning(request, "Password must be at least 8 characters.")
            return redirect('signup')

        if User.objects.filter(username=email).exists():
            messages.info(request, "Email already registered.")
            return redirect('signup')

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.save()

        # create empty profile
        Profile.objects.create(user=user)

        login(request, user)
        return redirect('profile')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated!")
            return redirect('index')

    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
