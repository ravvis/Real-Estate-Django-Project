
from django.contrib import admin
from django.urls import path
from realestate import views

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('agentlogin/', views.agentlogin, name='agentlogin'),
    path('officelogin/', views.officelogin, name='officelogin'),
    path('logout/', views.logout_from, name='logout'),
    path('property/', views.prop_view, name='form'),

    path('success/', views.success, name='success'),
    path('failure/', views.failure, name='failure'),
    path('agent-dashboard/', views.agent_dashboard, name="agent_dashboard"),
]

# handler403 = 'realestate.views.error_view'