
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm,CustomPasswordResetForm 
from expenseapp.models import ProfileUpdate
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from .forms import CustomPasswordResetForm




def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already in use.')
                return redirect('register')
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email or Password Are Invalid!')
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def FORGOTPASSWORD(request):
    return render(request,"forgotpassword.html")


User = get_user_model()





def custom_password_reset(request):
    return render(request, "custom_password_reset.html")


def profileupdate(request):
    return render(request, "profile_update.html")



        