# Create your views here.

import datetime
import random
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.contrib.auth.models import User # django-builtin
from vizwall.accounts.models import UserProfile # our custom profile additions
from django.contrib.auth import authenticate, login, logout

def vizwallTeam(request):
  (STAFF,FACULTY) = ([],[])
  staff = UserProfile.objects.all().filter(is_vizlab_staff=True, is_leadership_team=False, user__is_active=True).order_by('staff_position','rank_order','formal_name')
  for s in staff:
    STAFF.append((s.user,s))
  faculty = UserProfile.objects.all().filter(is_leadership_team=True, user__is_active=True).order_by('staff_position','rank_order', 'formal_name')
  for f in faculty:
    FACULTY.append((f.user,f))
  return render_to_response('accounts/team.html', {'staff': STAFF, 'faculty': FACULTY}, context_instance=RequestContext(request))

def login_view(request):
  username = request.POST['username']
  password = request.POST['password']
  user = authenticate(username=username, password=password)
  if user is not None:
    if user.is_active:
      login(request, user)
      return HttpResponseRedirect('/admin/')
    else:
      # account is disabled
      return render_to_response('accounts/login.html',{errors:'disabled'})
  else:
    # invalid login
    return render_to_response('accounts/login.html', {errors:'invalid'})

def logout_view(request):
  logout(request)
  return HttpResponseRedirect('/')
