from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import HostSignUp, HostLogin, ClientRegistration, Checkout
from .models import Host, Client
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings


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


def hostLogin(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))

    if request.method == "POST":
        form = HostLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print('Logged In')
                return redirect(reverse('god:client'))
            else:
                messages.error(request, 'Invalid username and password')
                return redirect(reverse('hostLogin'))
        else:
            messages.error(request, 'Please fill the form correctly')
            return redirect(reverse('hostLogin'))
    else:
        form = HostLogin(None)

    context = {
        "form": form
    }

    return render(request, "auth/hostLogin.html", context)


@login_required(login_url='hostLogin')
def hostCloseMeeting(request):
    logout(request)
    return redirect(reverse('home'))


@login_required(login_url='hostLogin')
def clientRegister(request):
    if request.method == "POST":
        form = ClientRegistration(request.POST)
        print(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            user = Client(name=name, phone=phone, email=email)
            print(name, phone, email, user)
            user.checkInTime = timezone.now()
            user.inMeeting = True
            user.save()
            if user is not None:
                messages.success(request, 'Thanks')
                print(user, user.checkInTime, user.checkOutTime)
                return redirect(reverse('god:client'))

        else:
            messages.error(
                request, 'Please try again. Values entered are wrong')
            return redirect(reverse('god:client'))

    else:
        form = ClientRegistration(None)

    context = {
        "form": form
    }

    return render(request, 'auth/clientRegistration.html', context)


@login_required
def ClientCheckout(request):
    if request.method == "POST":
        form = Checkout(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')

            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            user = Client.objects.get(email=email, phone=phone)
            if user is not None:
                messages.success(request, 'Thanks for attending the meeting')
                user.CheckOutTime = timezone.now()
                user.inMeeting = False
                user.save()
                return redirect(reverse('god:client'))
            else:
                messages.error(request, 'Please enter details correctly')
                return redirect(reverse('god:ClientCheckout'))

    else:
        form = Checkout(None)

    context = {
        "form": form
    }

    return render(request, "auth/ClientCheckout.html", context)
