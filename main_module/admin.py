from django.contrib import admin
from .models import Fighter, Registration,  Event
# Register your models here.

admin.site.register(Fighter)
admin.site.register(Registration)
admin.site.register(Event)