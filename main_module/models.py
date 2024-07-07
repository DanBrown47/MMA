from django.db import models

# Create your models here.
class EventType(models.Model):
    TYPE_CHOICES = (
        ('GR grappling', 'Grappling'),
        ('NF normal_fighting', 'Normal Fighting'),
        ('BX boxing', 'Boxing'),
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return self.get_type_display()

class Event(models.Model):
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    max_participants = models.PositiveIntegerField()
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    organizer_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.event_type} - {self.date}"

class Fighter(models.Model):
    name = models.CharField(max_length=255)
    # Add other relevant fighter information (weight class, experience, etc.)

    def __str__(self):
        return self.name

class Registration(models.Model):
    fighter = models.ForeignKey(Fighter, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fighter.name} - {self.event.event_type} on {self.event.date}"
