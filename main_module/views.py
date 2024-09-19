# from django.shortcuts import get_object_or_404
# from rest_framework import generics, viewsets, status
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.decorators import action, api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.authentication import JWTAuthentication

# from .models import EventType, Event, Fighter, Registration
# from .serializers import (
#     EventTypeSerializer, EventSerializer, FighterSerializer, 
#     RegistrationSerializer, MyTokenObtainPairSerializer, RegisterSerializer
# )

# # ViewSet for EventType model
# class EventTypeViewSet(viewsets.ModelViewSet):
#     authentication_classes = []
#     permission_classes = []
#     queryset = EventType.objects.all()
#     serializer_class = EventTypeSerializer

#     def list(self, request):
#         event_types = self.queryset.all()
#         serializer = self.serializer_class(event_types, many=True)
#         return Response(serializer.data)

# # ViewSet for Event model
# class EventViewSet(viewsets.ModelViewSet):
#     authentication_classes = []
#     permission_classes = []
#     queryset = Event.objects.filter(is_active=True).select_related('event_type')  # Optimize query
#     serializer_class = EventSerializer

#     @action(detail=True, methods=['post'], permission_classes=[])
#     def register(self, request, pk=None):
#         event = self.get_object()
#         if event.registrations.count() >= event.max_participants:
#             return Response({'error': 'Event is full.'}, status=status.HTTP_400_BAD_REQUEST)

#         # Ensure that the fighter exists before registering
#         try:
#             fighter = Fighter.objects.get(email=request.data['email'])  # Identify fighter by email
#         except Fighter.DoesNotExist:
#             return Response({'error': 'Fighter not found.'}, status=status.HTTP_404_NOT_FOUND)

#         # Create registration for the event
#         registration = Registration.objects.create(fighter=fighter, event=event)
#         serializer = RegistrationSerializer(registration)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# # ViewSet for Fighter model
# class FighterViewSet(viewsets.ModelViewSet):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     queryset = Fighter.objects.all()
#     serializer_class = FighterSerializer

# # ViewSet for Registration model
# class RegistrationViewSet(viewsets.ModelViewSet):
#     queryset = Registration.objects.select_related('fighter', 'event')  # Optimize queries
#     serializer_class = RegistrationSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         # Ensure that the registration is linked to the authenticated fighter
#         user = self.request.user
#         serializer.save(fighter=user)

# # JWT Token view
# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer

# # User registration view
# class RegisterView(viewsets.ModelViewSet):
#     queryset = Fighter.objects.all()
#     serializer_class = RegisterSerializer
#     parser_classes = (MultiPartParser, FormParser)  # Support for file uploads

#     def create(self, request, *args, **kwargs):
#         # Validate and create a new fighter account
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def getProfile(request):
#     user = request.user
#     serializer = FighterSerializer(user, many=False)
#     return Response(serializer.data)
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import generics, viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

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
        fighter_email = request.data.get('email')
        if not fighter_email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        fighter = Fighter.objects.filter(email=fighter_email).first()
        if not fighter:
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
        email = request.data.get('email')
        if Fighter.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate and create a new fighter account
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# Profile view
@api_view(['GET'])
@permission_classes([IsAuthenticated])

def getProfile(request):
    user = request.user
    serializer = FighterSerializer(user, many=False)
    return Response(serializer.data)

# Dashboard view
@login_required
def dashboard_view(request):
    # if not request.user.is_authenticated:
    #     return redirect('/login/')  # Redirect to login if not authenticated
    # print("Dashboard view accessed") 
    user = request.user

    # Serialize the user data
    serializer = FighterSerializer(user, many=False) 
    return render(request, 'dashboard.html', {'profile': serializer.data})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('/login/')  # Redirect to login after logout
