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
    message = ''
    if(request.method == 'POST'):
        name = request.POST.get('filter')
        area = request.POST.get('area')
        print('name : ' + name)
        print(area)
        type = request.POST.get('type')
        
        if name != '' and (type == 'filtered' or type is None):
            print('name')
            print('got filter, yayyyyyyyyyyy!!')
            properties = Property.objects.filter(property_name__icontains=name, is_available=True)
            if not properties:
                print('noooooooo')
                message = 'No results found with the property name ' + name
            
            else:
                message = 'Here are the properties with the property name ' + name
                
        elif area != '' and (type == 'filtered' or type is None):
            print('area')
            properties = Property.objects.filter(address__area__area__icontains=area, is_available=True)
            if not properties:
                print('noooooooo')
                message = 'No results found in the area ' + area

            else:
                message = 'Here are the properties in the the area ' + area

        elif type == 'all':
            properties = Property.objects.filter(is_available=True)
            if not properties:
                message = 'No Property Found'

        
        elif type == 'rent' or type == 'sale':
            properties = Property.objects.filter(is_available=True, tag=type)
            
            if not properties:
                message = 'No property available for ' + type
            
            else:
                message = 'Here are the properties available for ' + type
            
    
    purchases = Purchase.objects.filter(agent=agent)
    if message != '':
        messages.error(request, message)
    return render(request, 'agent_page.html', {'properties' : properties, 'agent' : agent, 'purchases' : purchases})

def failure(request):
    return render(request, 'failure.html')

def home(request):
    if request.user.is_authenticated:
        if request.user.is_agent:
            return redirect('/agent-dashboard/')
        else:
            return redirect('/office-dashboard/')
    else:
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
    if request.method == 'POST':

        form = PropertyForm(request.POST, request.FILES)
        form_owner = PersonForm(request.POST)
        city = City.objects.get(pk=1)
        area = request.POST.get('area')
        zipcode = request.POST.get('zipcode')
        description = request.POST.get('description')
        
        if form.is_valid() and form_owner.is_valid():
            print('is valid')
            flag = 0
            for a in Area.objects.all():
                if a.area == area and a.zipcode == zipcode:
                    flag = 1
                    break

            if(flag == 1):
                area = Area.objects.get(area=area)
            else:
                ar = Area(area=area, zipcode=zipcode, city=city)
                ar.save()
                area = ar
            ad = Address(area=area, description=description)
            ad.save()

            f = form.instance
            f2 = form_owner.instance
            f2.save()
            
            owner = Owner(owner=f2)
            owner.save()
            
            f.address = ad
            f.owner = owner
            
            f.save()
            
            return redirect('/property/')
            print('success')
        else:
            print('failure')
        print('fdsfs')
    
    else :
        form = PropertyForm()
        form_owner = PersonForm()

    return render(request, "property.html", {'form':form, 'form_owner':form_owner})

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

@office_required
def delete_property(request, property_id):
    print('came here u bitch')
    property = Property.objects.get(pk = property_id)
    property.delete()
    return redirect('/office-dashboard/')
        
def success(request):
    return render(request, 'success.html')

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().order_by('property_id')
    serializer_class = PropertySerializer


def intro(request):
    return render(request, 'Intro.html')