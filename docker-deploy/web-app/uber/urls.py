"""
URL configuration for uber project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.views.generic import TemplateView
from uber_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='main_page'),
    path('ride-request/', views.ride_request, name='ride_request'),
    path('ride-request/', views.ride_request, name='request_success'),
    path('sharer_request/', views.sharer_request, name='sharer_request'),
    path('valid_rides/', views.search_valid_rides, name='valid_rides'),
    
    path('sharer_join/<int:ride_id>/', views.sharer_join, name='sharer_join'),
    path('driver_join/<int:ride_id>/', views.driver_join, name='driver_join'),
    
    path('search_driver_rides/', views.search_driver_rides, name='search_driver_rides'),
    path('my_drives/', views.my_drives, name='my_drives'),
    path('my_rides/', views.my_rides, name='my_rides'),
    
    path('rides/ride_info/<int:ride_id>/', views.ride_info, name='ride_info'),
    path('profile/', views.profile_page, name='profile'),
    path('edit_profile/', views.edit_user_request, name='edit_profile'),
    path('edit_driver/', views.edit_driver_request, name='edit_driver'),
    
    
    path('register_user/', views.user_request, name='create_user_success'),
    path('create_driver/', views.driver_request, name='create_driver_success'),
    path('login/', views.Login, name='login_success'),
    path('logout/', views.logout_view, name='logout'),
    
    path('rides/owner_edit/<int:ride_id>/', views.owner_edit, name='owner_edit'),
    path('rides/driver_complete/<int:ride_id>/', views.driver_complete, name='driver_complete'),
    path('rides/sharer_edit/<int:sharer_id>/<int:ride_id>/', views.sharer_edit, name='sharer_edit')
]
