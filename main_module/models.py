from django.db import models
from django.contrib.auth.models import  AbstractBaseUser,BaseUserManager


# Create your models here.
class EventType(models.Model):
    TYPE_CHOICES = (
        ('GR grappling', 'Grappling'),
        ('NF normal_fighting', 'Normal Fighting'),
        ('BX boxing', 'Boxing'),
        ('MMA','MMA Match'),
        ('MMA','MMA Strike')
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return self.get_type_display()

class Event(models.Model):
    event_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    max_participants = models.PositiveIntegerField()
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    organizer_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.event_type} - {self.date}"
class FighterManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with email, password, and admin privileges."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
class Fighter(AbstractBaseUser):    
    name = models.CharField(max_length=255,unique=False, blank=False, null=True)
    middle_name = models.CharField(max_length=255,unique=False, blank=True, null=True)
    last_name = models.CharField(max_length=255,unique=False, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=False, null=False, default=0)
    weight_category = models.CharField(max_length=200, unique=False, blank=False, null=True)
    weight_code = models.CharField(max_length=30, unique=False, blank=False, null=True)
    height = models.IntegerField(blank=False, null=False, default=0)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    state=models.CharField(max_length=255 ,blank=True,null=True)
    sex = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')))
    email = models.EmailField(unique=True)
    number=models.IntegerField(blank=True,null=True)
    password = models.CharField(max_length=255)
    password2 = models.CharField(max_length=255)
    main_event = models.CharField(max_length=200, blank=True, null=True)
    coach_name=models.CharField(max_length=255, blank=True, null=True)
    club_name = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='fighter_photos/', blank=True, null=True)
    id_card = models.ImageField(upload_to='fighter_id_cards/', blank=True, null=True)
    win=models.IntegerField(blank=True,null=True)
    loss=models.IntegerField(blank=True,null=True)
    no_contest=models.IntegerField(blank=True,null=True)
    player_lock=models.BooleanField(default=False)
    player_disqualify=models.BooleanField(default=False)
    unique_id=models.CharField(max_length=10,blank=False,null=True,editable=False)
    is_fighter_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return True

    # Remove the username field inherited from AbstractUser
    objects = FighterManager()
    
    def __str__(self):
        return self.email
    def generate_unique_id(self):
        # if not self.name or not self.middle_name or not self.last_name:
        #     raise ValueError("All name parts (name, middle_name, last_name) must be provided to generate unique ID.")
    
        first_initial = self.name[0].upper() if self.name else '-'
        middle_initial = self.middle_name[0].upper() if self.middle_name else '-'
        last_initial = self.last_name[0].upper() if self.last_name else '-'

        initials = f"{first_initial}{middle_initial}{last_initial}"
    
        total_fighters = Fighter.objects.count()
        unique_number = 1001 + total_fighters  # Incremented based on the number of existing fighters
    
        return f"{initials}{unique_number}"
    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = self.generate_unique_id()
        super().save(*args, **kwargs)

class Registration(models.Model):
    fighter = models.ForeignKey(Fighter, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fighter.name} - {self.event.event_type} on {self.event.date}"
