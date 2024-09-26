from rest_framework import serializers
from .models import EventType, Event, Fighter, Registration
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    event_type = EventTypeSerializer(read_only=True)
    
    class Meta:
        model = Event
        fields = '__all__'

class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fighter
        fields = ['name','middle_name','last_name', 'age', 'weight', 'weight_category', 'height', 'date_of_birth', 'address', 'state','sex', 'email','number', 'weight_code','player_lock','player_disqualify','coach_name','club_name', 'photo', 'id_card', 'main_event','unique_id','is_fighter_active']

class FighterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fighter
        fields = ['name','middle_name','last_name', 'age', 'weight', 'weight_category','height', 'date_of_birth', 'address', 'state','sex', 'email','number', 'weight_code','player_lock','player_disqualify', 'password' ,'password2','coach_name','club_name', 'photo', 'id_card', 'main_event','unique_id','is_fighter_active']  # Specify fields explicitly
        read_only_fields = ['email', 'main_event']
    def validate(self, attrs):
        if not attrs.get('name') or not attrs.get('middle_name') or not attrs.get('last_name'):
            raise serializers.ValidationError("All name parts must be provided to generate a unique ID.")
        return attrs

class RegistrationSerializer(serializers.ModelSerializer):
    fighter = FighterSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    event_id = serializers.IntegerField(write_only=True)  # Added to handle event registration by ID

    class Meta:
        model = Registration
        fields = ['fighter', 'event', 'event_id']

    def create(self, validated_data):
        event_id = validated_data.pop('event_id')  # Extract event_id from the data
        event = Event.objects.get(id=event_id)  # Get the Event instance
        registration = Registration.objects.create(event=event, **validated_data)
        return registration

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['isAdmin'] = user.is_staff
        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Fighter.objects.all())]
    )

    class Meta:
        model = Fighter
        fields = ['name', 'middle_name','last_name','age', 'weight', 'weight_category', 'weight_code','height', 'date_of_birth', 'address', 'state','sex', 'email','number', 'password' ,'password2','coach_name','club_name', 'photo', 'id_card', 'main_event','unique_id','is_fighter_active']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = Fighter.objects.create(
            name=validated_data['name'],
            middle_name=validated_data['middle_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            number=validated_data['number'],
            age=validated_data['age'],
            weight=validated_data['weight'],
            weight_category=validated_data['weight_category'],
            weight_code=validated_data['weight_code'],
            height=validated_data['height'],
            date_of_birth=validated_data.get('date_of_birth', None),
            address=validated_data.get('address', None),
            state=validated_data['state'],
            sex=validated_data['sex'],
            main_event=validated_data['main_event'],
            club_name=validated_data.get('club_name', None),
            coach_name=validated_data.get('coach_name'),
            photo=validated_data.get('photo', None),
            id_card=validated_data.get('id_card', None),
            is_fighter_active=validated_data('is_fighter_active')
        ),

        user.set_password(validated_data['password'])
        user.save()

        return user
