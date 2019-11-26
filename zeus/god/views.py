from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import HostSignUp
from .models import Host
from django.contrib.auth.models import User


def home(request):
    return render(request, 'home.html', {})


def hostSignup(request):
    if request.method == "POST":
        form = HostSignUp(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            user = User.objects.create_user(
                username=username, email=email, password=password)
            extendedUser = Host(user=user, email=email,
                                phone=phone, address=address)
            extendedUser.save()
            print('Registration done')
            messages.success(request, 'Registration success')
            return redirect(reverse('hostSignup'))
        else:
            messages.error(request, 'Please register again')
    else:
        form = HostSignUp(None)

    context = {
        "form": form
    }

    return render(request, 'auth/hostSignup.html', context)
