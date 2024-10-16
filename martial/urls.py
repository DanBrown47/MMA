"""martial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from main_module import views
from main_module import serializers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('main_module.urls')),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),  # Login using JWT
    path('dashboard/', views.dashboard_view, name='dashboard'),  # Dashboard view after login
    path('login/dashboard/', views.dashboard_view, name='login_dashboard'),  # New URL pattern for login/dashboard
    path('dashboard/events/', views.event_list, name='event_list'),
    path('dashboard/events/<int:event_id>/', views.event_detail, name='event_detail'),
]
