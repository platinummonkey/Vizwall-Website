from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField
from django.contrib.auth.models import User
from vizwall.accounts.models import UserProfile
import datetime

AUDIENCE_CHOICES = (
  (5, u'0-5'),
  (10, u'5-10'),
  (20, u'10-20'),
  (30, u'20-30'),
)

DURATION_CHOICES = (
  (30, u'30 min'),
  (60, u'1 hour'),
  (120, u'2 hours'),
  (180, u'3 hours'),
  (240, u'4 hours'),
  (300, u'5 hours'),
  (480, u'Full Day'), 
)

CONTACT_EXEC_CHOICES = (
  (1, u'President'),
  (2, u'Provost'),
  (3, u'Business Affairs'),
  (4, u'Community Service'),
  (5, u'Research'),
  (6, u'Student Affairs'),
  (7, u'University Advancement'),
)

COMPONENT_CHOICES = (
  ('vizwall', 'Vis Wall'),
  ('3dtv', '3D TV'),
  ('omni', 'Omni Haptic'),
  ('hd2', 'HD2 Haptic'),
  ('smart', 'Smart Board'),
)


# datetime input formats
dTimeFieldInputs = [
'%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
'%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
'%Y-%m-%d',              # '2006-10-25'
'%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
'%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
'%m/%d/%Y',              # '10/25/2006'
'%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
'%m/%d/%y %H:%M',        # '10/25/06 14:30'
'%m/%d/%y',              # '10/25/06'
'%m/%d/%Y %I:%M %p',     # '10/25/2006 8:00 AM'
'%m/%d/%Y %I:%M:%S %p'   # '10/25/2006 8:00:00 AM'
'%m-%d-%Y %I:%M %p',     # '10-25-2006 8:00 AM'
'%m-%d-%Y %I:%M:%S %p',  # '10-25-2006 8:00:00 AM'
]


# Create your models here.
class Event(models.Model):
  ''' Event model which contains event data and modification data '''
  event_title = models.CharField(max_length=200, help_text='Short Descriptive Title')
  event_req_date = models.DateTimeField(auto_now_add=True, editable=False)
  event_last_modified = models.DateTimeField(auto_now=True, editable=False)
  event_duration = models.PositiveIntegerField(max_length=6, choices=DURATION_CHOICES, default=60, help_text='Choose the amount of time you will need')
  event_date = models.DateTimeField(help_text='Please use the date selector and check the calendar for available times!')
  event_audience = models.CharField(max_length=256, help_text='Describe the demographic of the attendees')
  event_visitors = models.PositiveIntegerField(max_length=4, choices=AUDIENCE_CHOICES, default=10, help_text='How many people are expected?')
  event_component_vizwall = models.BooleanField(default=False)
  event_component_3dtv = models.BooleanField(default=False)
  event_component_omni = models.BooleanField(default=False)
  event_component_hd2 = models.BooleanField(default=False)
  event_component_smart = models.BooleanField(default=False)
  event_assistance = models.BooleanField(default=True, blank=True, help_text='Will assistance be required?')
  event_contact_name = models.CharField(max_length=200, help_text='Who is responsible for the event?')
  event_contact_dept = models.CharField(max_length=200, blank=True, null=True, help_text='Which department is responsible for the event?')
  event_contact_exec = models.PositiveIntegerField(max_length=4, choices=CONTACT_EXEC_CHOICES, help_text='Which executive area does the organizing department report to?')
  event_contact_phone = PhoneNumberField(help_text='123-456-7890 only please!')
  event_contact_email = models.EmailField(max_length=100, help_text='john.doe@utsa.edu')
  event_details = models.TextField(max_length=2000,help_text='Please desribe your event and the focus of the event.')
  event_pub_date = models.DateTimeField(auto_now_add=True, editable=False)
  event_is_published = models.BooleanField(default=False)
  event_assigned_proctors = models.ManyToManyField(User, through='Proctor')
  event_is_declined = models.BooleanField(default=False)
  
  class Meta:
    # orders by descending pub_date and ascending (alphabetical) title
    ordering = ['-event_date', 'event_title']

  def __unicode__(self):
    return '%s - %s' % (self.event_date.strftime('%m/%d/%Y %H:%M'), self.event_title)

  def get_duration(self):
    d = self.tuple2dict(DURATION_CHOICES)
    return d[self.event_duration]

  def get_end_date(self):
    dur = self.event_duration
    return self.event_date+datetime.timedelta(minutes=int(dur))

  def get_audience(self):
    try:
      d = self.tuple2dict(AUDIENCE_CHOICES)
      return d[self.event_audience]
    except:
      return None

  def get_contact_exec(self):
    try:
      d = self.tuple2dict(CONTACT_EXEC_CHOICES)
      return d[self.event_contact_exec]
    except:
      return None

  def get_cs_components(self):
    comp = []
    if self.event_component_vizwall: comp.append('VizWall')
    if self.event_component_3dtv: comp.append('3D TV')
    if self.event_component_omni: comp.append('Omni')
    if self.event_component_hd2: comp.append('HD2')
    if self.event_component_smart: comp.append('Smartboard')
    if comp:
      return ', '.join(comp)
    return None

  def assign_proctors_byID(self, proctorList):
    ''' Clears old proctors then assigns new proctors based on [User.pk] '''
    self.event_assigned_proctors.clear()
    assignedList = []
    for p in proctorList:
      try:
        user = User.objects.get(pk=p)
        newProctor = Proctor.objects.create(event=self, user=user)
        assignedList.append(user)
      except:
        continue
    return assignedList

  def assign_proctors(self, proctorList):
    ''' Clears old proctors then assigns new proctors based on [UserProfile] '''
    self.event_assigned_proctors.clear()
    assignedList = []
    for p in proctorList:
      try:
        user = p.user # p is a UserProfile object
        newProctor = Proctor.objects.create(event=self, user=user)
        assignedList.append(user)
      except:
        continue
    return assignedList

  def get_assigned_proctors_can_email(self):
    ps = self.get_assigned_proctors()
    proctors = []
    if ps:
      for p in ps:
        if not p.user.profile.force_no_emails:
          proctors.append(p.user)
      return proctors
    return None

  def get_assigned_proctors(self):
    ''' Get assigned proctors: [User] '''
    ps = self.proctor_set.all()
    proctors = []
    if ps:
      for p in ps:
        proctors.append(p.user)
      return proctors
    return None

  def get_unassigned_proctors(self):
    ''' Get unassigned proctors to the event: [User]'''
    unassigned = []
    proctors = [p.user for p in self.proctor_set.all()]
    presenters = UserProfile.objects.all().filter(demo_presenter=True)
    for p in presenters:
      if p.user not in proctors:
        unassigned.append(p.user)
    return unassigned

  def tuple2dict(self, choices):
    d = {}
    for choice in choices:
      d[choice[0]] = choice[1]
    return d

class Proctor(models.Model):
  ''' This is an intermediate model in order to assign proctors to events'''
  event = models.ForeignKey(Event)
  user = models.ForeignKey(User)
  date_assigned = models.DateTimeField(auto_now_add=True, editable=False)
