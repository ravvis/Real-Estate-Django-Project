
from django.contrib import admin
from django.urls import path
from realestate import views

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('agentlogin/', views.agentlogin, name='agentlogin'),
    path('officelogin/', views.officelogin, name='officelogin'),
    path('logout/', views.logout_from, name='logout'),
]
