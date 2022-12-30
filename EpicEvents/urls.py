"""EpicEvents URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_nested import routers
#from accounts import views
from accounts.views import UserViewset, ClientViewset
from contracts.views import ContractViewset
from events.views import EventViewset




router = routers.DefaultRouter()

user_router = routers.SimpleRouter()
user_router.register('users', UserViewset, basename='users')
clients_router = routers.SimpleRouter()
clients_router.register(r'clients', ClientViewset, basename='clients')
contracts_router = routers.SimpleRouter()
contracts_router.register(r'contracts', ContractViewset, basename='contracts')

events_router = routers.SimpleRouter()
events_router.register(r'events', EventViewset, basename='events')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('', include('rest_framework.urls')),
    
    path('', include(user_router.urls)),
    path('', include(clients_router.urls)),
    path('', include(contracts_router.urls)),
    path('', include(events_router.urls)),
]
urlpatterns += router.urls