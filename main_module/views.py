
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
from django.http import JsonResponse

from .models import EventType, Event, Fighter, Registration
from .serializers import (
    EventTypeSerializer, EventSerializer, FighterSerializer, 
    RegistrationSerializer, MyTokenObtainPairSerializer, RegisterSerializer)
# events

# Fetch list of active events
def event_list(request):
    events = Event.objects.filter(is_active=True).values(
        'id', 'event_name', 'description', 'event_type__type', 
        'date', 'time', 'location', 'max_participants', 'fees', 'organizer_name'
    )
    return JsonResponse(list(events), safe=False)
# Fetch details of a specific event
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event_data = {
        'id': event.id,
        'event_name': event.event_name,
        'description': event.description,
        'event_type': event.event_type.type,
        'date': event.date,
        'time': event.time,
        'location': event.location,
        'max_participants': event.max_participants,
        'fees': event.fees,
        'organizer_name': event.organizer_name,
    }
    return JsonResponse(event_data)


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

# Dashboard view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_view(request): 
    email = request.user.email
    # Serialize the user data
    fighter_instance = Fighter.objects.get(email=email)
    serializer = FighterSerializer(fighter_instance, many=False) 
    return Response({'profile': serializer.data}, status=status.HTTP_200_OK)

# Logout view
def logout_view(request):
    logout(request)
    return redirect('/login/')  # Redirect to login after logout
