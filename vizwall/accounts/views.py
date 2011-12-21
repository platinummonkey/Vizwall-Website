# Create your views here.

import datetime
import random
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.contrib.auth.models import User # django-builtin
from vizwall.accounts.models import UserProfile # our custom profile additions
from django.contrib.auth import authenticate, login, logout

def index(request):
  return HttpResponseRedirect('/')

def viewProfile(request):
  return HttpResponseRedirect('/')

def logout_view(request):
  logout(request)
  return HttpResponseRedirect('/')


