# Create your views here.

import datetime
import random
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404

# Email actions
from django.core.mail import send_mail
# debug
DEBUGSENDMAIL = False

# User and profile
from django.contrib.auth.models import User
#from vizwall.accounts.models import UserProfile
from vizwall.accounts.forms import UserFormAdmin
from vizwall.accounts.customadmin.reports import UserFilterSet

def getInactiveUsersCount():
  return User.objects.all().filter(is_active=False).count()

@staff_member_required
def index(request):
  ufs = UserFilterSet(request.GET or {'order_by': 'username', 'is_active': True})
  numUsers = ufs.qs.count()
  numInactive = getInactiveUsersCount()
  return render_to_response('accounts/customadmin/index.html',
          {'filter': ufs, 'user_count': numUsers,
            'inact_user_count': numInactive},
          context_instance=RequestContext(request))

def emailPassword(email, password):
  subject = 'Password Reset'
  message = 'Your password has been reset: %s\n\nPlease login now and change this: http://vislab.utsa.edu/login/' % password
  send_mail(subject, message, 'no-reply@vislab.utsa.edu', email)

def createUser(request, redirectURL='/admin/accounts/'):
  if request.method == 'POST':
    form = UserFormAdmin(request.POST)
    if form.is_valid():
      (user, password) = form.save()
      emailPassword(user.email, password)
      return HttpResponseRedirect(redirectURL)
  else:
    form = UserFormAdmin()
  return render_to_response('accounts/customadmin/create.html', {'form': form}, context_instance=RequestContext(request))

def editUser(request, user_id, redirectURL='/admin/accounts/'):
  user = get_object_or_404(User, pk=user_id)
  userprofile = user.get_profile()
  if request.method == 'POST':
    form = UserFormAdmin(request.POST)
    if form.is_valid():
      form.update_user(user_id)
      if form.cleaned_data['reset_password'] == True and form.cleaned_data['is_active'] == True:
        password = form.do_reset_password()
        email = form.cleaned_data['email']
        emailPassword(email, password)
      return HttpResponseRedirect(redirectURL)
  else:
    data = {'username': user.username,
            'email': user.email,
            'firstname': user.first_name,
            'lastname': user.last_name,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'is_leadership_team': userprofile.is_leadership_team,
            'is_vizlab_staff': userprofile.is_vizlab_staff,
            'is_demo_presenter': userprofile.demo_presenter,
            'is_scheduler': userprofile.is_scheduler,
            'is_event_emails_only': userprofile.extra_get_event_emails,
            'is_force_no_emails': userprofile.force_no_emails,
            'formal_prefix': userprofile.formal_name,
            'faculty_webpage': userprofile.faculty_webpage,
            'staff_position_number': userprofile.staff_position,
            'faculty_position': userprofile.staff_faculty_position,
            'rank_order': userprofile.rank_order,
            'reset_password': False}
    form = UserFormAdmin(data)
    return render_to_response('accounts/customadmin/edit.html', {'form': form, 'user_id': user_id, 'redirectURL': redirectURL}, context_instance=RequestContext(request))

def activateUser(request, user_id, redirectURL='/admin/accounts/'):
  user = get_object_or_404(User, pk=user_id)
  user.is_active = True
  password = User.objects.make_random_password(length=15)
  user.set_password(password)
  userprofile = user.get_profile()
  userprofile.last_update_profile = datetime.datetime.now()
  userprofile.save()
  user.save()
  emailPassword(user.email, password)
  return HttpResponseRedirect(redirectURL)

def deactivateUser(request, user_id, redirectURL='/admin/accounts/'):
  user = get_object_or_404(User, pk=user_id)
  if request.method == 'POST':
    if request.POST['confirm'] == u'Yes':
      user.is_active = False
      user.set_unusable_password()
      userprofile = user.get_profile()
      userprofile.last_update_profile = datetime.datetime.now()
      userprofile.save()
      user.save()
    return HttpResponseRedirect(redirectURL)
  return render_to_response('accounts/customadmin/confirm.html', {'mode': 'deactivate', 'user_id': user_id, 'user': user}, context_instance=RequestContext(request))

def deleteUser(request, user_id, redirectURL='/admin/accounts/'):
  user = get_object_or_404(User, pk=user_id)
  if request.method == 'POST':
    if request.POST['confirm'] == u'Yes':
      userprofile = user.get_profile()
      userprofile.delete()
      user.delete()
    return HttpResponseRedirect(redirectURL)
  return render_to_response('accounts/customadmin/confirm.html', {'mode': 'delete', 'user_id': user_id, 'user': user}, context_instance=RequestContext(request))

