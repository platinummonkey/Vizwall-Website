import django_filters
from vizwall.events.models import *
#from vizwall.events.forms import EventForm
import datetime, time

class EventFilterSet(django_filters.FilterSet):
  event_title = django_filters.filters.CharFilter(lookup_type="icontains")
  event_contact_dept = django_filters.filters.CharFilter(lookup_type="icontains")
  event_date = django_filters.filters.CustomDateTimeRangeFilter() #input_formats=dTimeFieldInputs)
  #event_date_start = django_filters.filters.DateFilter()
  #event_date_end = django_filters.filters.DateFilter()

  class Meta:
    model = Event
    fields = ['event_title', 'event_date', 'event_is_published', 'event_is_declined', 'event_duration', 'event_visitors', 'event_component_vizwall', 'event_component_3dtv', 'event_component_omni', 'event_component_hd2', 'event_component_smart', 'event_assistance', 'event_contact_dept', 'event_contact_exec']
    #form = EventForm # use already made form
    order_by = True # allow any field to be sorted by

  def __init__(self, *args, **kwargs):
    super(EventFilterSet, self).__init__(*args, **kwargs)
    for name, field in self.filters.iteritems():
      if isinstance(field, django_filters.filters.ChoiceFilter):
        # Add 'Any' entry to choice fields
        field.extra['choices'] = tuple([('', 'Any'), ] + list(field.extra['choices']))
    self.filters['event_date'].field.fields[0].input_formats = dTimeFieldInputs
    self.filters['event_date'].field.fields[1].input_formats = dTimeFieldInputs
