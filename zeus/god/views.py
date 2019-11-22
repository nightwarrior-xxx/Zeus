from django.shortcuts import render


# function based view for home
def home(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    
    return render(request, 'home.html', {})


# function based view for handling host login
def host_login(request):
    return render(request)

