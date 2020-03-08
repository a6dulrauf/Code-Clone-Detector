
# Create your views here.

from django.shortcuts import render, redirect
from CodeClone.forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def signup_user(request):
    form = UserForm
    if request.method == 'POST':
        form_view = form(request.POST)
        if form_view.is_valid():
            user = form_view.save(commit=False)
            # normalize data
            username = form_view.cleaned_data['username']
            email = form_view.cleaned_data['email']
            password = form_view.cleaned_data['password']
            confirmPassword = form_view.cleaned_data['confirmPassword']

            if not User.objects.filter(email=email).exists():
                if password == confirmPassword:
                    user.set_password(password)
                    user.save()
                else:
                    form_view.add_error("confirmPassword", "Passwords Donot Matched !")
                    return render(request, "Accounts/registration_form.html", {'form': form_view})
            else:
                form_view.add_error("email", "Email already exists !")
                return render(request, "Accounts/registration_form.html", {'form': form_view})

            # authentication
            user = authenticate(username=username, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session['username'] = user.username
                    return render(request, 'CodeClone/dashboard.html')
        return render(request, "Accounts/registration_form.html", {'form': form_view})

    form_view = form(None)
    return render(request, "Accounts/registration_form.html", {'form': form_view})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['login_username']
        password = request.POST['login_password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['username'] = user.username
                return redirect("project-features")
        else:
            messages.error(request, 'Invalid Credentials !')

    return render(request, "Accounts/login_form.html")

def logout_user(request):
    logout(request)
    return redirect('index')

