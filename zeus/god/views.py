from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import HostSignUp, HostLogin, ClientRegistration, Client
from .models import Host, Client
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone


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


@login_required(redirect_field_name='hostLogin')
def hostCloseMeeting(request):
    logout(request)
    return redirect(reverse('home'))


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
            user.save()
            if user is not None:
                messages.success(request, 'Thanks')
                print(user, user.checkInTime, user.checkOutTime)
                return redirect(reverse('god:client'))
        
        else:
            messages.error(request, 'Please try again')
            return redirect(reverse('god:client'))

    else:
        form = ClientRegistration(None)

    context = {
        "form": form
    }

    return render(request, 'auth/clientRegistration.html', context)


def ClientCheckout(request):
    if request.method == "POST":
        form = ClientCheckout(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')

            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            user = Client.objects.filter(name=name, email=email, phone=phone)[0]
            if user is not None:
                messages.success(request,'Thanks for attending the meeting')
                user.CheckOutTime = timezone.now()
                user.save()
                return redirect(reverse('god:Client'))
            else:
                messages.error(request, 'Please enter details correctly')
                return redirect(reverse('god:ClientCheckout'))

    else:
        form = ClientCheckout(None)

    context = {
        "form": form
    }

    return render(request, "auth/ClientCheckout.html", context)
