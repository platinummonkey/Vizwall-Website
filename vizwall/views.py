#index

# not sure if this is necessary
######### -*- coding: utf-8 -*-

import datetime
import random
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

# News feed
from vizwall.news.views import getRecentNews
from vizwall.news.models import News

# Event Feed
from vizwall.events.views import getUpcomingEvents
from vizwall.events.models import Event

page_size = 20 # maximum # of events to show on page (we'll do mini synyopsis and they can click per event) 

def viewRedirect(request, event_id):
  ''' Redirect to /events/detail/<event_id>/ '''
  return HttpResponseRedirect('/event/detail/%s/' % event_id)

def calendar(request={}):
  ''' Main View of events, sorts data out for display'''
  return render_to_response('calendar.html', {}, context_instance=RequestContext(request))  

def events(request={}):
  ''' Main View of events, sorts data out for display'''
  return render_to_response('eventrequest.html', {}, context_instance=RequestContext(request))  


def adminhome(request):
#  return HttpResponseRedirect('/')
  ''' Admin Home'''
  return render_to_response('admin-menu.html', {}, context_instance=RequestContext(request)) 

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






def faq(request={}):
  ''' FAQ'''
  return render_to_response('faq.html', {}, context_instance=RequestContext(request))
  
def overview(request={}):
  ''' Overview'''
  return render_to_response('docs.html', {}, context_instance=RequestContext(request))
  
def team(request={}):
  ''' VizLab Team'''
  return render_to_response('team.html', {}, context_instance=RequestContext(request))  
  
def facilities(request={}):
  ''' Facilities'''
  return render_to_response('facilities.html', {}, context_instance=RequestContext(request))
  
def research(request={}):
  ''' Research'''
  return render_to_response('research.html', {}, context_instance=RequestContext(request))

def galvizwall(request={}):
  ''' VizWall Gallery'''
  return render_to_response('gal-vizwall.html', {}, context_instance=RequestContext(request))

def galhaptic(request={}):
  ''' Haptic Device Gallery'''
  return render_to_response('gal-haptic.html', {}, context_instance=RequestContext(request))

