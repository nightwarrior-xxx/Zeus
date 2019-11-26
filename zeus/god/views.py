from django.shortcuts import render, redirect, reverse
from .forms import HostSignup, HostLogin
from django.contrib.auth import login, authenticate
from django.contrib import messages


# function based view for home
def home(request):
    return render(request, 'home.html', {})


# function based view for handling host login
def hostSignup(request):
    if request.user.is_authenticated:
        username = request.user.username
        return redirect(reverse('home'))

    if request.method == "POST":
        form = HostSignup(request.POST)
        print(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save() 
            messages.info(request, 'Thanks for signing up')
            return redirect(reverse('hostLogin'))
        else:
            messages.error(request, 'Fill all the fields correctly')
            return redirect(reverse('hostSignup'))

    else:
        form = HostSignup()

    context = {
        "form": form
    }

    return render(request, "auth/hostSignup.html", context)



# function based view for handling client login
def hostLogin(request):
    if request.method == "POST":
        form = HostLogin(request.POST)
        print(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password1)
            print(user)
            if user is not None:
                login(request, user)
                print('Logged in')
            else:
                return redirect(reverse('hostLogin'))
        else:
            messages.error(request, 'Invalid details')
            return redirect(reverse('hostLogin'))
    else:
        form = HostLogin(None)

    context = {
        "form": form
    }
    return render(request, 'auth/hostLogin.html', context)
