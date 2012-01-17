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
  picture = ImageField(required=False)
  faculty_position = ChoiceField(choices=STAFF_TITLE_CHOICES)
  faculty_webpage = URLField(verify_exists=True, max_length=512, required=False)
  is_staff = BooleanField(required=False, initial=False)
  is_superuser = BooleanField(required=False, initial=False)
  is_leadership_team = BooleanField(required=False, initial=False)
  is_vizlab_staff = BooleanField(required=False, initial=False)
  is_demo_presenter = BooleanField(required=False, initial=False)
  is_scheduler = BooleanField(required=False, initial=False)
  is_event_emails_only = BooleanField(required=False, initial=False)
  is_force_no_emails = BooleanField(required=False, initial=False)
  staff_position_number = IntegerField(required=False, initial=10)
  rank_order = IntegerField(required=False, initial=10)
  reset_password = BooleanField(required=False, initial=False)
  is_active = BooleanField(required=False, initial=True)
  
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
    fd = self.cleaned_data
    user = User.objects.get(pk=user_id)
    userprofile = user.get_profile()
    (user.username, user.email, user.first_name, user.last_name) = (fd['username'], fd['email'], fd['firstname'], fd['lastname'])
    user.is_staff = True if fd['is_staff'] else False
    user.is_superuser = True if fd['is_superuser'] else False
    user.save()
    userprofile.is_leadership_team = True if fd['is_leadership_team'] else False
    userprofile.is_vizlab_staff = True if fd['is_vizlab_staff'] else False
    userprofile.demo_presenter = True if fd['is_demo_presenter'] else False
    userprofile.is_scheduler = True if fd['is_scheduler'] else False
    userprofile.extra_get_event_emails = True if fd['is_event_emails_only'] else False
    userprofile.force_no_emails = True if fd['is_force_no_emails'] else False
    if fd['formal_prefix']: userprofile.formal_name = fd['formal_prefix']
    if fd['faculty_webpage']: userprofile.faculty_webpage = fd['faculty_webpage']
    if fd['staff_position_number']: userprofile.staff_position = fd['staff_position_number']
    if fd['faculty_position']: userprofile.staff_faculty_position = fd['faculty_position']
    if fd['rank_order']: userprofile.rank_order = fd['rank_order']
    userprofile.save()
    if fd['is_active'] == False: self.deactivate(user)
    return (user, userprofile)

  def do_reset_password(self, user_id):
    password = User.objects.make_random_password(length=15)
    user = User.objects.get(user_id)
    user.set_password(password)
    user.save()
    return password

# Contact Form
from captcha.fields import CaptchaField
from django.contrib.localflavor.us.forms import USPhoneNumberField
from vizwall.settings import CONTACT_FORM_EMAIL
class ContactSubmission():
  def __init__(self, subject, message, name, phone, email):
    self.subject = subject
    self.message = message
    self.name = name
    self.phone = phone
    self.email = email

class ContactForm(Form):
  subject = CharField(max_length=100)
  message = CharField(max_length=2000, widget=Textarea(attrs={'cols':35, 'rows': 5}))
  name = CharField(max_length=200)
  phone = USPhoneNumberField(help_text='123-456-7890 only please!')
  email = EmailField()
  cc_myself = BooleanField(required=False)
  captcha = CaptchaField()

  def save(self):
    cs = ContactSubmission(self.subject, self.message, self.name, self.phone, self.email)
    mail_send([CONTACT_FORM_EMAIL], cs, 'mail/contact_form')
    if self.cc_myself:
      mail_send([self.email], cs, 'mail/contact_form')
    return cs
