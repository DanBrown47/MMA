
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

    # Include other necessary authentication URLs if needed
    path('api-auth/', include('rest_framework.urls')),  # DRF's built-in authentication views (optional)
]