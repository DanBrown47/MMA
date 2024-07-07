
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'event-types', views.EventTypeViewSet)
router.register(r'events', views.EventViewSet)
router.register(r'fighters', views.FighterViewSet)
router.register(r'registrations', views.RegistrationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]