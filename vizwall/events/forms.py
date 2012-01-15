from django.forms import *
from django.forms.widgets import *
from django.forms.extras.widgets import *
from vizwall.events.models import Event, COMPONENT_CHOICES, dTimeFieldInputs
import datetime
from vizwall.accounts.models import UserProfile

class EventForm(ModelForm):
  '''Event form, customized to show normal Anonymous view'''
  event_date = DateTimeField(required=True, initial=None, input_formats=dTimeFieldInputs, help_text='Please use the date selector and check the calendar for available times!')
  class Meta:
    model = Event
    #fields = ()
    exclude=('event_last_modified', 'event_req_date',
             'event_pub_date', 'event_is_published', 'event_assigned_proctors',
             'event_is_declined')
    widgets = {
        'event_detail': Textarea(attrs={'cols':35, 'rows': 5}),
        'event_components_vizwall': CheckboxInput(),
        'event_components_3dtv': CheckboxInput(),
        'event_components_omni': CheckboxInput(),
        'event_components_hd2': CheckboxInput(),
        'event_components_smart': CheckboxInput(),
        }

  def clean_event_component_vizwall(self):
    if self.cleaned_data['event_component_vizwall']:
      return True
    return False

  def clean_event_component_omni(self):
    if self.cleaned_data['event_component_omni']:
      return True
    return False

  def clean_event_component_3dtv(self):
    if self.cleaned_data['event_component_3dtv']:
      return True
    return False

  def clean_event_component_hd2(self):
    if self.cleaned_data['event_component_hd2']:
      return True
    return False

  def clean_event_component_smart(self):
    if self.cleaned_data['event_component_smart']:
      return True
    return False
 
  def clean_event_date(self):
    ''' Checks requested date against any current events for conflicts
      raises an error if another published event exists, else passes validation'''
    reqDate = self.cleaned_data['event_date']
    reqDuration = self.cleaned_data['event_duration']
    conflict = self.checkConflict(reqDate, reqDuration)
    if conflict:
      raise forms.ValidationError("This event Conflicts with another event: \"%s\" between %s-%s" % ('\n'+conflict.event_title, conflict.event_date.strftime('%H:%M'), conflict.get_end_date().strftime('%H:%M')))
    # always return the cleaned data, whether it was changed or not
    return reqDate

  def inRange(self,begin,duration,eventStart,eventDuration):
    ''' Checks if date ranges overlap - pads 1 minute off end times'''
    end = begin + datetime.timedelta(minutes=duration-1)
    eventEnd = eventStart + datetime.timedelta(minutes=int(eventDuration)-1)
    #print begin, end
    #print eventStart, eventEnd
    isInRange = begin <= eventStart <= end or begin <= eventEnd <= end
    return isInRange
  
  def checkConflict(self, reqDate, reqDuration):
    '''checks current scheduled and published events if there is a conflict '''
    tom = reqDate+datetime.timedelta(days=2) # make sure full day tomorrow is included
    daysEvents = Event.objects.all().filter(
            event_date__gte=datetime.date(reqDate.year,reqDate.month,reqDate.day),
            event_date__lte=datetime.date(tom.year,tom.month,tom.day),
            event_is_published=True)
    for event in daysEvents:
      if self.inRange(event.event_date, event.event_duration, reqDate, reqDuration):
        # conflict exists, return with conflicting event (~bool True)
        return event
    # no conflicts, valid event time, return with nothing (~bool False)
    return False

class EventFormAdmin(EventForm):
  class Meta:
    model=Event
    exclude=('event_pub_date', 'event_req_date', 'event_last_modified', 'event_assigned_proctors')
    widgets = {
        'event_detail': Textarea(attrs={'cols':35, 'rows':5}),
        'event_components_vizwall': CheckboxInput(),
        'event_components_3dtv': CheckboxInput(),
        'event_components_omni': CheckboxInput(),
        'event_components_hd2': CheckboxInput(),
        'event_components_smart': CheckboxInput(),
        'event_is_published': CheckboxInput(),
        'event_is_declined': CheckboxInput(),
        }

  # representing the manytomany related field in Event
  proctors = MultipleChoiceField()
