
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import RegisterView,MyTokenObtainPairView, dashboard_view, logout_view

router = DefaultRouter()
# router.register(r'event-types', views.EventTypeViewSet, basename='event_type')

router.register(r'events', views.EventViewSet, basename='event')
router.register(r'fighters', views.FighterViewSet, basename='fighter') 
router.register(r'event_registrations', views.RegistrationViewSet, basename='event_registration')
router.register(r'register', views.RegisterView, basename='register')

urlpatterns = [
    path('', include(router.urls)),
    # Custom Views
    path('login/', MyTokenObtainPairView.as_view(), name='login'),  # Login using JWT
    path('dashboard/', dashboard_view, name='dashboard'),  # Dashboard view after login
    path('logout/', logout_view, name='logout'),  # Logout functionality
    path('login/dashboard/', views.dashboard_view, name='login_dashboard'),
    path('dashboard/events/', views.event_list, name='event_list'),
    path('dashboard/events/<int:event_id>/', views.event_detail, name='event_detail'),

    # Include other necessary authentication URLs if needed
    path('api-auth/', include('rest_framework.urls')),  # DRF's built-in authentication views (optional)
    
]