from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        messages.success(request, "Welcome to the home page!")
        return render(request, 'index.html', {'user': request.user})
    return render(request, 'index.html')

# Signup view
def signup_view(request):
    flag = 0

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        if password != confirm_password:
            messages.warning(request, "Password is not matching.")
            return redirect(reverse("signup"))

        if len(password) < 8:
            messages.warning(request, "Password must be atleast 8 characters.")
            return redirect(reverse("signup"))
        

        if flag == 0:
            try :
                if User.objects.get(username=email):
                    messages.info(request, "Email already reigster!")
                    return redirect(reverse("signup"))
            except Exception as Identifier:
                pass

            user = User.objects.create_user(email, email, password)
            user.first_name = name
            user.save()
            messages.success(request, "Account created successfully!!")
            return redirect('login')
        else:
            messages.error(request, "Please Enter valid password!!")
            return redirect(reverse("signup"))

    return render(request, 'signup.html')

# Sign in view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print(username, User.objects.all())
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            print("Invalid credentials")
            return redirect(reverse('login'))
    return render(request, 'login.html')

# logout view
def logout_view(request):
    logout(request)
    messages.success(request, "logout Successfull!!")
    return render(request, 'index.html')