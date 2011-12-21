from django.db import models
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField


STAFF_TITLE_CHOICES = (
  # THESE MUST BE IN ORDER BY NUMBER IN ORDER FOR get_staff_position to work!
  # if they are not staff then ignore
  (0, 'Not Staff'),
  (1, 'VizLab Director'),
  (2, 'VizLab Co-Director'),
  (3, 'Haptic Device Coordinator'),
  (4, 'VizLab Coordinator'),
  (5, 'VizLab IT Project Manager'),
  (6, 'VizLab System Administrator'),
  (7, 'Graduate Research Assistant'),
  (8, 'VizLab Web Specialist'),
  (9, 'UnderGraduate Assistant'),
)

NAME_FORMALITIES_PREFIX = (
  # These are prefixes to create a formal name. ie. Dr. John Doe
  ('none', 'Mr/Ms/Mrs/etc..'), # no prefix
  ('Dr.', 'Dr.'),
  ('Ph.D.', 'Ph.D.'),
  ('P.E.', 'P.E.'),
)

# Create your models here.
class UserProfile(models.Model):
  user = models.ForeignKey(User, unique=True, related_name='profile')
  last_update_profile = models.DateTimeField(auto_now_add=True, editable=False)
  staff_position = models.IntegerField(choices=STAFF_TITLE_CHOICES, default=STAFF_TITLE_CHOICES[0][0])
  staff_faculty_position = models.CharField(max_length=500, blank=True, null=True)
  formal_name = models.CharField(max_length=50, choices=NAME_FORMALITIES_PREFIX, default='none')
  picture = models.ImageField(upload_to='/media/profiles/avatars', default='/media/site_images/userprofile.jpg')
  is_leadership_team = models.BooleanField(default=False)
  is_vizlab_staff = models.BooleanField(default=False)
  faculty_webpage = models.URLField(default='', blank=True)
  phone = PhoneNumberField(blank=True, default='', null=True)
  rank_order = models.IntegerField(default=100)
  demo_presenter = models.BooleanField(default=False)
  is_scheduler = models.BooleanField(default=False)
  extra_get_event_emails = models.BooleanField(default=False)
  force_no_emails = models.BooleanField(default=False)

  def __unicode__(self):
    return self.get_formal_name()

  def get_staff_position(self):
    d = self.tuple2dict(STAFF_TITLE_CHOICES)
    return d[self.staff_position]

  def get_formal_name(self):
    if self.formal_name == u'none':
      return self.user.get_full_name()
    else:
      return '%s %s' % (self.formal_name, self.user.get_full_name())
  
  def tuple2dict(self, choices):
    d = {}
    for choice in choices:
      d[choice[0]] = choice[1]
    return d

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
