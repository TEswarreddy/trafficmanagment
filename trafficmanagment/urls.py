"""
URL configuration for trafficmanagment project.

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
from .import views
from users  import views as usviews
from admins import views as adviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.basefunction,name='basefunction'),


    #user views
    path('userloginsignup/', usviews.userloginsignup, name='userloginsignup'),
    path('signup/', usviews.signup, name='signup'),
    path('login/', usviews.login, name='login'),
    path('dashboard/', usviews.dashboard, name='dashboard'), 
    path('logout/', usviews.logout, name='logout'),
    path("run_simulation/", usviews.run_simulation, name="run_simulation"),
    path('run_gesture_simulation/', usviews.run_gesture_simulation, name='run_gesture_simulation'),
    path("emergency/", usviews.emergency, name="emergency"),




    #admin views
    path('admin_login/',adviews.admin_login,name='admin_login'),
    path("admin_login_check/", adviews.admin_login_check, name="admin_login_check"),
    path("admin-dashboard/", adviews.admin_dashboard, name="admin_dashboard"),
    path("admin-logout/", adviews.admin_logout, name="admin_logout"),
    

    
    path('activate-user/<int:user_id>/', adviews.activate_user, name='activate_user'),
    path('block-user/<int:user_id>/', adviews.block_user, name='block_user'),
    path('delete-user/<int:user_id>/', adviews.delete_user, name='delete_user'),
    path('view-user/<int:user_id>/', adviews.view_user_details, name='view_user_details'),
]
