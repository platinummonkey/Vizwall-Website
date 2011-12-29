from django.forms import *
from django.forms.widgets import *
from django.forms.extras.widgets import *
from vizwall.accounts.models import STAFF_TITLE_CHOICES, NAME_FORMALITIES_PREFIX, UserProfile
from django.contrib.auth.models import User
import datetime

class UserFormAdmin(Form):
  '''User form, for admin view only'''
  username = CharField(max_length=100)
  firstname = CharField(max_length=256)
  lastname = CharField(max_length=256)
  formal_prefix = ChoiceField(choices=NAME_FORMALITIES_PREFIX)
  email = EmailField(max_length=256)
  image = ImageField(required=False)
  faculty_position = ChoiceField(choices=STAFF_TITLE_CHOICES)
  faculty_webpage = URLField(verify_exists=True, max_length=512, required=False)
  is_staff = BooleanField(required=True, initial=False)
  is_superuser = BooleanField(required=True, initial=False)
  is_leadership_team = BooleanField(required=True, initial=False)
  is_vizlab_staff = BooleanField(required=True, initial=False)
  is_demo_presenter = BooleanField(required=True, initial=False)
  is_scheduler = BooleanField(required=True, initial=False)
  is_event_emails_only = BooleanField(required=True, initial=False)
  is_force_no_emails = BooleanField(required=True, initial=False)
  staff_position_number = IntegerField(required=True, initial=10)
  rank_order = IntegerField(required=True, initial=10)
  reset_password = BooleanField(required=False, initial=False)
  is_active = BooleanField(required=False, initial=True)
  
  def clean_username(self):
    try:
      User.objects.get(username=self.username)
      return False
    except:
      return self.username

  def clean_email(self):
    try:
      User.objects.get(email=self.email)
      return False
    except:
      return self.email

  def save(self):
    password = User.objects.make_random_password(length=15)
    newuser = User.objects.create_user(self.username, self.email, password)
    newuser.first_name = self.firstname
    newuser.last_name = self.lastname
    if self.is_staff: newuser.is_staff = True
    if self.is_superuser: newuser.is_superuser = True
    newuser.save()
    newuserprofile = newuser.get_profile()
    if self.is_leadership_team: newuserprofile.is_leadership_team = True
    if self.is_vizlab_staff: newuserprofile.is_vizlab_staff = True
    if self.is_demo_presenter: newuserprofile.demo_presenter = True
    if self.is_scheduler: newuserprofile.is_scheduler = True
    if self.is_event_emails_only: newuserprofile.extra_get_event_emails = True
    if self.is_force_no_emails: newuserprofile.force_no_emails = True
    newuserprofile.formal_name = self.formal_prefix
    newuserprofile.faculty_webpage = self.faculty_webpage
    newuserprofile.staff_position = self.staff_position_number
    newuserprofile.staff_faculty_position = self.faculty_position 
    newuserprofile.rank_order = self.rank_order
    newuserprofile.save()
    if self.is_active == False: self.deactivate(newuser)
    return (user, password)

  def deactivate(self, user):
    user.is_active = False
    user.set_unusable_password()
    user.save()
    
  def update_user(self, user_id):
    user = User.objects.get(pk=user_id)
    userprofile = user.get_profile()
    (user.username, user.email, user.first_name, user.last_name) = (self.username, self.email, self.firstname, self.lastname)
    if self.is_staff: user.is_staff = True
    if self.is_superuser: user.is_superuser = True
    user.save()
    if self.is_leadership_team: userprofile.is_leadership_team = True
    if self.is_vizlab_staff: newuserprofile.is_vizlab_staff = True
    if self.is_demo_presenter: newuserprofile.demo_presenter = True
    if self.is_scheduler: newuserprofile.is_scheduler = True
    if self.is_event_emails_only: newuserprofile.extra_get_event_emails = True
    if self.is_force_no_emails: newuserprofile.force_no_emails = True
    newuserprofile.formal_name = self.formal_prefix
    newuserprofile.faculty_webpage = self.faculty_webpage
    newuserprofile.staff_position = self.staff_position_number
    newuserprofile.staff_faculty_position = self.faculty_position
    newuserprofile.rank_order = self.rank_order
    newuserprofile.save()
    if self.is_active == False: self.deactivate(user)

  def do_reset_password(self, user_id):
    password = User.objects.make_random_password(length=15)
    user = User.objects.get(user_id)
    user.set_password(password)
    user.save()
    return password
