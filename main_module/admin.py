from django.contrib import admin
from .models import EventType, Event, Fighter, Registration

admin.site.register(EventType)
admin.site.register(Event)
admin.site.register(Fighter)
admin.site.register(Registration)