from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from .decorators import *
from django.contrib import messages
from rest_framework import viewsets
from .serializers import PropertySerializer


def error_view(request):
    return render(request, '404.html')

def login_(request):
    if(request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_authenticated and user.is_agent:
                x = 24
                while x < 39:
                    person = Person.objects.get(pk=x)
                    owner = Owner(owner=person)
                    owner.save()
                    x = x + 1
                return redirect('/agent-dashboard/')

            elif user.is_authenticated and user.is_office:
                return redirect('/office-dashboard/')

        else:
            message = 'Invalid username or password'
            messages.error(request, message)
            return redirect('/login/')

    return render(request, 'registration/login.html')
         
@agent_required
def agent_dashboard(request): 

    agent = {}   
    if request.user.is_authenticated:
        u = request.user
        agent = Agent.objects.get(user=u);
        print(agent.agent.email)
    properties = {}
    properties = Property.objects.filter(is_available=True)
    
    purchases = Purchase.objects.filter(agent=agent)
    return render(request, 'agent_page.html', {'properties' : properties, 'agent' : agent, 'purchases' : purchases})

def failure(request):
    return render(request, 'failure.html')

def home(request):
    return redirect('/login/')

def logout_from(request):
    logout(request)
    return redirect('/')

def officelogin(request):
    if(request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_office:
            login(request, user)
            if user.is_authenticated and user.is_office:
                return redirect('/office-dashboard/')

        else:
            message = 'Invalid username or password'
            messages.error(request, message)
            return redirect('/officelogin/')

    return render(request, 'registration/officelogin.html')

@office_required
def office_dashboard(request):
    agents = Agent.objects.all()
    purchases = Purchase.objects.all()
    properties = Property.objects.all()
    areas = Area.objects.all()
    return render(request, 'office_page.html', {'agents' : agents, 'purchases' : purchases, 'properties' : properties, 'areas' : areas})

@office_required
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

@office_required
def agent_register(request):
    context = {}
    if request.method == 'POST':
        form1 = PersonForm(request.POST)
        form2 = UserForm(request.POST)

        if form1.is_valid() and form2.is_valid():
            form1.save(commit=True)
            f1 = form1.instance
            f = form2.instance
            f.is_agent = True
            f.save()

            f2 = User.objects.get(username=f.username)
            agent = Agent(agent=f1, user=f2)
            agent.save()
            return redirect('/office-dashboard/')
        else:
            return redirect('/failure/')
    else:
        form1 = PersonForm()
        form2 = UserForm()
    return render(request, 'agent-register.html', {'form1' : form1, 'form2' : form2}) 


@agent_required
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
                message = 'The property - ' + property.property_name + ' has been success fully updated!!'
                messages.success(request, message)
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

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().order_by('property_id')
    serializer_class = PropertySerializer

