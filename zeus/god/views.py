
import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client

from sendsms import api
from django.conf import settings
from .models import Host, Clients
from .forms import HostLogin, HostSignUp, ClientRegistration, Checkout
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout



# Function based view for home page
def home(request):
    return render(request, 'home.html', {})


# Function based view for Host Registration
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
            if user is not None:
                messages.success(request, 'Registration success')
                return redirect(reverse('hostSignup'))
    else:
        form = HostSignUp(None)

    context = {
        "form": form
    }

    return render(request, 'auth/hostSignup.html', context)


# Function based view for Host Login
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


# Function based view for Guest Registration
@login_required(login_url='hostLogin')
def clientRegister(request):
    if request.method == "POST":
        form = ClientRegistration(request.POST)
        print(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            altUser = Clients.objects.filter(email=email, phone=phone)
            print(altUser)
            if altUser.exists():
                user = Clients.objects.get(name=altUser[0])
                user.inMeeting = True
                user.checkInTime = timezone.now()
                user.checkOutTime = timezone.now()
                user.save()
            else:
                user = Clients(name=name, phone=phone, email=email)
                user.inMeeting=True
                user.checkInTime = timezone.now()
                user.checkOutTime = timezone.now()
                user.save()
            print(name, phone, email, user)
            print(user.checkInTime, Clients.objects.get(name=user.name).inMeeting)
            if user is not None:

                # # Sending Email to Host
                m = "Hey {host}, {guest} just checked-in for the meeting. {guest}'s email  is {email} and phone number is {phoneNum}".format(
                    host=request.user.username,
                    guest=user.name,
                    email=user.email,
                    phoneNum=user.phone
                )
                message = Mail(
                    from_email=os.environ.get('DEFAULT_FROM_EMAIL'),
                    to_emails=request.user.email,
                    subject='Check-In from new Guest',
                    html_content=m)

                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.send(message)
                print(response.status_code, response.body, response.headers)
                print('Email send')


                # SMS send to host
                smsContext = {
                    "host": request.user.username,
                    "guestName": user.name,
                    "guestEmail": user.email,
                    "guestPhone": phone
                }
                client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
                smsBody = render_to_string("snippets/sms.html", smsContext)
                smsPhone = "+{}{}".format(request.user.profile.phone.country_code,
                                          request.user.profile.phone.national_number)
                print(smsBody, smsPhone)
                try:
                    smsMessage = client.messages \
                        .create(
                            body=smsBody,
                            from_=os.environ.get('TWILIO_PHONE_NUMBER'),
                            to=smsPhone
                        )
                    print(smsMessage.sid)
                    print('SMS send')

                except:
                    print('SMS send failed')

                messages.success(request, 'Thanks for Checking-In. Enjoy the meeting.')
                print(user, user.checkInTime, user.checkOutTime)
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
            user = Clients.objects.get(email=email, phone=phone)
            if user is not None:
                messages.success(request, 'Thanks for attending the meeting')
                user.checkOutTime = timezone.now()
                user.inMeeting = False
                user.save()
                context = {
                    "guestName": user.name,
                    "guestEmail": user.email,
                    "guestPhone": phone,
                    "address": request.user.profile.address,
                    "guestCheckInTime": user.checkInTime,
                    "guestCheckOutTime": user.checkOutTime
                }
                # Sending Email to Guest
                message = Mail(
                    from_email=os.environ.get('DEFAULT_FROM_EMAIL'),
                    to_emails=email,
                    subject='Thanks for attending meeting',
                    html_content=render_to_string('snippets/email.html', context))

                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.send(message)
                print(response.status_code, response.body, response.headers)
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
