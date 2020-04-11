
from django.contrib import admin
from django.urls import path, re_path
from realestate import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('agentlogin/', views.agentlogin, name='agentlogin'),
    path('officelogin/', views.officelogin, name='officelogin'),
    path('logout/', views.logout_from, name='logout'),
    path('property/', views.prop_view, name='form'),
    path('success/', views.success, name='success'),
    path('failure/', views.failure, name='failure'),
    path('agent-dashboard/', views.agent_dashboard, name="agent_dashboard"),

    re_path(r'^purchase/(?P<property_id>\d+)/$', views.client_view, name="purchase_client"),
    
] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler403 = 'realestate.views.error_view'