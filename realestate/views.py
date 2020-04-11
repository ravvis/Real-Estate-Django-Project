from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from .decorators import *

def error_view(request):
    return render(request, '404.html')

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
         
@agent_required
def agent_dashboard(request): 

    agent = {}   
    if request.user.is_authenticated:
        u = request.user
        agent = Agent.objects.get(user=u);
        print(agent.agent.email)
    properties = {}
    properties = Property.objects.filter(is_available=True)

    return render(request, 'agent_page.html', {'properties' : properties, 'agent' : agent})

def failure(request):
    return render(request, 'failure.html')

def home(request):
    return render(request, 'home.html')

def logout_from(request):
    logout(request)
    return redirect('/')

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

def prop_view(request):
    context = {}
    if request.method == 'POST':

        form = PropertyForm(request.POST, request.FILES)
        
        if form.is_valid():
            print('is valid')
            form.save(commit=True)
            return redirect('/property/')
            print('success')
        else:
            print('failure')
        print('fdsfs')
    
    else :
        form = PropertyForm()

    return render(request, "property.html", {'form':form})



def client_view(request, property_id):

    property = Property.objects.filter(pk=property_id)
    
    if property.exists() and property[0].is_available == True:    
        p = property[0]
        context = {}
    
        if request.method == 'POST':    
            form = PersonForm(request.POST)
            print(form.errors)
    
            if form.is_valid():    
                print('form is valid')
                form.save(commit=True)
                f = form.instance
                client = Client(client=f)
                client.save()
                property = Property.objects.get(pk=property_id)
                u = request.user
                agent = Agent.objects.get(user=u);
                purchase = Purchase(client = client, property=property, agent=agent)
                purchase.save()
                message = 'The property has been success fully updated!!'
                return redirect('/agent-dashboard/')
    
            else:
                return render(request, "client_info.html", {'form' : form})

        else:
            form = PersonForm()

        return render(request, "client_info.html", {'form':form})
    else:
        return render(request, 'already_purchased.html')


        
def success(request):
    return render(request, 'success.html')



