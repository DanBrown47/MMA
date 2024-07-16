from django.shortcuts import render

from rest_framework import generics

# Create your views here
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import EventType, Event, Fighter, Registration
from .serializers import EventTypeSerializer, EventSerializer, FighterSerializer,  RegistrationSerializer, MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class EventTypeViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer

    def list(self, request):
        event_types = self.queryset.all()
        serializer = self.serializer_class(event_types, many=True)
        return Response(serializer.data)

class EventViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.select_related('event_type')  # Optimize for event type data
    serializer_class = EventSerializer

    @action(detail=True, methods=['post'], permission_classes=[])  # Allow unauthenticated registration
    def register(self, request, pk=None):
        event = self.get_object(pk)
        if event.registrations.count() >= event.max_participants:
            return Response({'error': 'Event is full.'}, status=status.HTTP_400_BAD_REQUEST)

        fighter, created = Fighter.objects.get_or_create(name=request.data['name'])
        registration = Registration.objects.create(fighter=fighter, event=event)
        serializer = RegistrationSerializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FighterViewSet(viewsets.ModelViewSet):
    queryset = Fighter.objects.all()
    serializer_class = FighterSerializer

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.select_related('fighter', 'event')  # Optimize for fighter and event data
    serializer_class = RegistrationSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

#Register User
class RegisterView(viewsets.ModelViewSet):
    queryset = Fighter.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request): # Authenticate this manually in future
    user = request.user
    serializer = ProfileSerializer(user, many=False)
    return Response(serializer.data)


