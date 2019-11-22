from django.shortcuts import render
from .forms import HostForm

# function based view for home
def home(request):
    return render(request, 'home.html',{})


# function based view for handling host login
def host_login(request):
    if request.method == "POST":
        form = HostForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return redirect(reverse('host:host_login'))

    else:
        form = HostForm(None)

    context = {
        "form": form
    }
    return render(request, 'auth/host_login.html', context)
