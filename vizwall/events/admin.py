from vizwall.events.models import Event
from django.contrib import admin

class EventAdmin(admin.ModelAdmin):
  fields = ['event_date', 'event_title']

# enable admin control over news - so simple!
admin.site.register(Event, EventAdmin)
