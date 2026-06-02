from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import LoginHistory


# ======================================
# Welcome Page
# ======================================

def welcome(request):

    return render(request, 'welcome.html')


# ======================================
# Login Page
# ======================================

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(

            request,

            username=username,

            password=password

        )

        # Valid User

        if user is not None:

            login(request, user)

            # Save Login History

            LoginHistory.objects.create(

                user=user

            )

            messages.success(request, f"Welcome back, {user.username}!")

            # Admin User

            if user.is_superuser:

                return redirect('/admin/')

            # Normal User

            return redirect('/dashboard/')

        # Invalid User

        else:

            messages.error(request, "Invalid username or password")

            return render(

                request,

                'login.html',

                {

                    'error': 'Invalid username or password'

                }

            )

    return render(request, 'login.html')


# ======================================
# Signup Page
# ======================================

def signup_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        email = request.POST.get('email')

        password = request.POST.get('password')

        confirm_password = request.POST.get('confirm_password')

        # Password Check

        if password != confirm_password:

            messages.error(request, "Passwords do not match")

            return render(

                request,

                'signup.html',

                {

                    'error': 'Passwords do not match'

                }

            )

        # Username Check

        if User.objects.filter(

            username=username

        ).exists():

            messages.error(request, "Username already exists")

            return render(

                request,

                'signup.html',

                {

                    'error': 'Username already exists'

                }

            )

        # Create User

        User.objects.create_user(

            username=username,

            email=email,

            password=password

        )

        messages.success(request, "Account created successfully. Please log in.")

        return redirect('/login/')

    return render(request, 'signup.html')


# ======================================
# Logout Page
# ======================================

def logout_view(request):

    logout(request)

    messages.success(request, "You have been logged out.")

    return redirect('/dashboard/')
