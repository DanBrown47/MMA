# from django.shortcuts import render

# from rest_framework import generics
# from rest_framework.parsers import MultiPartParser, FormParser


# # Create your views here
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from .models import EventType, Event, Fighter, Registration
# from .serializers import EventTypeSerializer, EventSerializer, FighterSerializer,  RegistrationSerializer, MyTokenObtainPairSerializer, RegisterSerializer
# from rest_framework_simplejwt.authentication import JWTAuthentication

# class EventTypeViewSet(viewsets.ModelViewSet):
#     authentication_classes = []
#     permission_classes = []
#     queryset = EventType.objects.all()
#     serializer_class = EventTypeSerializer

#     def list(self, request):
#         event_types = self.queryset.all()
#         serializer = self.serializer_class(event_types, many=True)
#         return Response(serializer.data)

# class EventViewSet(viewsets.ModelViewSet):
#     authentication_classes = []
#     permission_classes = []
#     queryset = Event.objects.filter(is_active=True).select_related('event_type')  # Optimize for event type data
#     serializer_class = EventSerializer

#     @action(detail=True, methods=['post'], permission_classes=[])  # Allow unauthenticated registration
#     def register(self, request, pk=None):
#         event = self.get_object(pk)
#         if event.registrations.count() >= event.max_participants:
#             return Response({'error': 'Event is full.'}, status=status.HTTP_400_BAD_REQUEST)

#         fighter = Fighter.objects.get(name=request.data['name'])
#         registration = Registration.objects.create(fighter=fighter, event=event)
#         serializer = RegistrationSerializer(registration)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class FighterViewSet(viewsets.ModelViewSet):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     queryset = Fighter.objects.all()
#     serializer_class = FighterSerializer

# class RegistrationViewSet(viewsets.ModelViewSet):
#     queryset = Registration.objects.select_related('fighter', 'event')  # Optimize for fighter and event data
#     serializer_class = RegistrationSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

#     def perform_create(self, serializer):
#         user = self.request.user
#         serializer.save(fighter=user)

# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer

# #Register User
# class RegisterView(viewsets.ModelViewSet):
#     queryset = Fighter.objects.all()
#     serializer_class = RegisterSerializer
#     parser_classes = (MultiPartParser, FormParser)  # Add parsers to handle file uploads

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def getProfile(request): # Authenticate this manually in future
#     user = request.user
#     serializer = ProfileSerializer(user, many=False)
#     return Response(serializer.data)


from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import EventType, Event, Fighter, Registration
from .serializers import (
    EventTypeSerializer, EventSerializer, FighterSerializer, 
    RegistrationSerializer, MyTokenObtainPairSerializer, RegisterSerializer
)

# ViewSet for EventType model
class EventTypeViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer

    def list(self, request):
        event_types = self.queryset.all()
        serializer = self.serializer_class(event_types, many=True)
        return Response(serializer.data)

# ViewSet for Event model
class EventViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Event.objects.filter(is_active=True).select_related('event_type')  # Optimize query
    serializer_class = EventSerializer

    @action(detail=True, methods=['post'], permission_classes=[])
    def register(self, request, pk=None):
        event = self.get_object()
        if event.registrations.count() >= event.max_participants:
            return Response({'error': 'Event is full.'}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure that the fighter exists before registering
        try:
            fighter = Fighter.objects.get(email=request.data['email'])  # Identify fighter by email
        except Fighter.DoesNotExist:
            return Response({'error': 'Fighter not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Create registration for the event
        registration = Registration.objects.create(fighter=fighter, event=event)
        serializer = RegistrationSerializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# ViewSet for Fighter model
class FighterViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Fighter.objects.all()
    serializer_class = FighterSerializer

# ViewSet for Registration model
class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.select_related('fighter', 'event')  # Optimize queries
    serializer_class = RegistrationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Ensure that the registration is linked to the authenticated fighter
        user = self.request.user
        serializer.save(fighter=user)

# JWT Token view
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# User registration view
class RegisterView(viewsets.ModelViewSet):
    queryset = Fighter.objects.all()
    serializer_class = RegisterSerializer
    parser_classes = (MultiPartParser, FormParser)  # Support for file uploads

    def create(self, request, *args, **kwargs):
        # Validate and create a new fighter account
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):
    user = request.user
    serializer = FighterSerializer(user, many=False)
    return Response(serializer.data)
