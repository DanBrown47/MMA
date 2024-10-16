# from django.contrib import admin
# from .models import EventType, Event, Fighter, Registration


# admin.site.register(EventType)
# admin.site.register(Event)
# admin.site.register(Fighter)
# admin.site.register(Registration)
from django.contrib import admin
from .models import EventType, Event, Fighter, Registration,RegistrationEvent

class FighterAdmin(admin.ModelAdmin):
    model = Fighter
    list_display = ('email', 'name', 'age')
    search_fields = ('email', 'name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'age', 'weight', 'height', 'date_of_birth', 'address', 'sex', 'club_name', 'photo', 'id_card','is_fighter_active')}),
    )
class RegistrationEventAdmin(admin.ModelAdmin):
    # Optional: customize the list display to show specific fields in the admin list view
    list_display = ('eventid', 'event_name', 'fighterid', 'fighter_name')

admin.site.register(EventType)
admin.site.register(Event)
admin.site.register(Fighter, FighterAdmin)
admin.site.register(Registration)
