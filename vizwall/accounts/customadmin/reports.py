import django_filters
from django.contrib.auth.models import User
from vizwall.events.models import dTimeFieldInputs

class UserFilterSet(django_filters.FilterSet):
  username = django_filters.filters.CharFilter(lookup_type="icontains")
  first_name = django_filters.filters.CharFilter(lookup_type="icontains")
  last_name = django_filters.filters.CharFilter(lookup_type="icontains")
  last_login = django_filters.filters.CustomDateTimeRangeFilter()

  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'last_login', 'profile__demo_presenter', 'profile__extra_get_event_emails', 'profile__force_no_emails', 'profile__is_leadership_team', 'profile__is_vizlab_staff', 'profile__is_scheduler', 'profile__staff_position']
    #form = EventForm # use already made form
    order_by = True # allow any field to be sorted by

  def __init__(self, *args, **kwargs):
    super(UserFilterSet, self).__init__(*args, **kwargs)
    for name, field in self.filters.iteritems():
      if isinstance(field, django_filters.filters.ChoiceFilter):
        # Add 'Any' entry to choice fields
        field.extra['choices'] = tuple([('', 'Any'), ] + list(field.extra['choices']))
    self.filters['last_login'].field.fields[0].input_formats = dTimeFieldInputs
    self.filters['last_login'].field.fields[1].input_formats = dTimeFieldInputs
