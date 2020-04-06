from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from realestate.models import User

def agentlogin(request):
    if(request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_authenticated and user.is_agent:
                return redirect('/')

        else:
            return redirect('/')

    return render(request, 'registration/agent_login.html')

def officelogin(request):
    if(request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_authenticated and user.is_office:
                return redirect('/')

        else:
            return redirect('/home/')

    return render(request, 'registration/officelogin.html')

def home(request):
    return render(request, 'home.html')

def logout_from(request):
    logout(request)
    return redirect('/')