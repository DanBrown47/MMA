
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import RegisterView

router = DefaultRouter()
# router.register(r'event-types', views.EventTypeViewSet, basename='event_type')

router.register(r'events', views.EventViewSet, basename='event')
router.register(r'fighters', views.FighterViewSet, basename='fighter') 
router.register(r'event_registrations', views.RegistrationViewSet, basename='event_registration')
router.register(r'register', views.RegisterView, basename='register')

urlpatterns = [
    path('', include(router.urls)),
    
]