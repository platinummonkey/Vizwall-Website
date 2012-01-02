#index

# not sure if this is necessary
######### -*- coding: utf-8 -*-

import datetime
import random
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.contrib.admin.views.decorators import staff_member_required

# News feed
from vizwall.news.views import getRecentNews

# Event Feed
from vizwall.events.views import getUpcomingEvents
from vizwall.events.customadmin.views import getActiveOverallStats, getPendingEvents

page_size = 20 # maximum # of events to show on page (we'll do mini synyopsis and they can click per event) 

def viewRedirect(request, event_id):
  ''' Redirect to /events/detail/<event_id>/ '''
  return HttpResponseRedirect('/event/detail/%s/' % event_id)

@staff_member_required
def adminhome(request):
#  return HttpResponseRedirect('/')
  ''' Admin Home'''
  stats = getActiveOverallStats() # grabs generic event stats
  news = getRecentNews(10) # Get 10 latest entries
  upcomingEvents = getUpcomingEvents(10) # Get 10 upcoming events
  pendingEvents = getPendingEvents(request)
  if pendingEvents: pendingEvents = pendingEvents[:10] # Get 10 upcoming events
  return render_to_response('admin-menu.html', {'stats': stats, 
          'news': news, 'events': upcomingEvents,
          'pendingevents': pendingEvents},
          context_instance=RequestContext(request))

# TEMPORARY

def eventrequest(request={}):
  ''' Event Request'''
  return render_to_response('eventrequest.html', {}, context_instance=RequestContext(request)) 

def eventdetail(request={}):
  ''' Event Detail'''
  return render_to_response('eventdetail.html', {}, context_instance=RequestContext(request)) 

def adminmenu(request={}):
  ''' Event Listing'''
  return render_to_response('admin-menu.html', {}, context_instance=RequestContext(request)) 

def adminaccounts(request={}):
  ''' Event Listing'''
  return render_to_response('admin-accounts.html', {}, context_instance=RequestContext(request)) 

def adminaccountsdetail(request={}):
  ''' Event Listing'''
  return render_to_response('admin-accounts-detail.html', {}, context_instance=RequestContext(request)) 

def adminnews(request={}):
  ''' Event Listing'''
  return render_to_response('admin-news.html', {}, context_instance=RequestContext(request)) 
  
def adminnewsdetail(request={}):
  ''' Event Listing'''
  return render_to_response('admin-news-detail.html', {}, context_instance=RequestContext(request)) 

def adminpages(request={}):
  ''' Event Listing'''
  return render_to_response('admin-pages.html', {}, context_instance=RequestContext(request)) 
  
def adminpagesdetail(request={}):
  ''' Event Listing'''
  return render_to_response('admin-pages-detail.html', {}, context_instance=RequestContext(request)) 

def admineventrequest(request={}):
  ''' Event Listing'''
  return render_to_response('admin-event-request.html', {}, context_instance=RequestContext(request)) 




def home(request={}, page=0):
  ''' Home'''
  news = getRecentNews(5) # Get 5 latest entries
  events = getUpcomingEvents(4) # Get 4 upcoming events
  return render_to_response('index.html', {'news': news, 'events': events}, context_instance=RequestContext(request))

def news(request={}, page=0):
  ''' VizLab in the News'''
  return render_to_response('news.html', {}, context_instance=RequestContext(request)) 

def login(request={}, page=0):
  ''' Login page '''
  return render_to_response('login.html', {}, context_instance=RequestContext(request)) 
  
def contact(request={}):
  ''' Contact'''
  return render_to_response('contact.html', {}, context_instance=RequestContext(request))

def galvizwall(request={}):
  ''' VizWall Gallery'''
  return render_to_response('gal-vizwall.html', {}, context_instance=RequestContext(request))

def galhaptic(request={}):
  ''' Haptic Device Gallery'''
  return render_to_response('gal-haptic.html', {}, context_instance=RequestContext(request))

