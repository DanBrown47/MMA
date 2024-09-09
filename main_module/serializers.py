from rest_framework import serializers
from .models import EventType, Event, Fighter, Registration
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    event_type = EventTypeSerializer(read_only=True)
    
    class Meta:
        model = Event
        fields = '__all__'

class FighterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fighter
        fields = '__all__'  # Adjust fields as needed
        read_only_fields = ('email',)

class RegistrationSerializer(serializers.ModelSerializer): # For event registration
    fighter = FighterSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    event_id = serializers.IntegerField(write_only=True) 
    

    class Meta:
        model = Registration
        fields = ['fighter', 'event', 'event_id']

    def create(self, validated_data):
        event_id = validated_data.pop('event_id')  # Extract event_id from the data
        if event_id is None:
            raise serializers.ValidationError({'event_id': 'This field is required.'})
        event = Event.objects.get(id=event_id)  # Get the Event instance
        registration = Registration.objects.create(event=event, **validated_data)
        return registration

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        # token['username'] = user.username
        token['email'] = user.email

        return token


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, read_only=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Fighter.objects.all())]
    )

    class Meta:
        model = Fighter
        fields = ('name', 'email', 'username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = Fighter.objects.create(
            email=validated_data['email'],
            username=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user