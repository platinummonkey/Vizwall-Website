# Create your views here.

import datetime
import random
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

# Email actions
from vizwall.accounts.models import UserProfile
from vizwall.utils import mass_email
from vizwall.settings import REQUESTER_NEW_REQUEST, SCHED_NEW_REQUEST

# Events stuff
from vizwall.events.models import Event
from vizwall.events.viewscalendar import formatEvents
from vizwall.events.forms import *

# debug
DEBUGSENDMAIL = True

def index(request):
  ''' REDIRECT to calendar view '''
  return HttpResponseRedirect('/calendar/') 

def displaySingleEvent(request, event_id):
  ''' Display a single event, template controls what is public and private'''
  try:
    event = Event.objects.get(pk=event_id)
    if event.event_is_declined or not event.event_is_published:
      return render_to_response('events/events_forbidden.html', {})
  except Event.DoesNotExist:
    raise Http404
  return render_to_response('events/event_details.html', {'event': event})

def displayDaysEvents(request, y, m, d):
  ''' Displays a single day's events '''
  try:
    (year, month, day) = int(y), int(m), int(d)
    if year in range(d.year-5, d.year+5): # within +/- 5 years - can always change this, but this seemed reasonable.
      if month in range(1,13): # need 13, range doesn't include final value!
        if day in range(1,32):
          eventQuery = Event.objects.all().filter(event_date__year=year, event_date__month=month, event_date__day=day, event_is_published=True, event_is_declined=False)
          events = formatEvents(eventQuery)
  except:
    raise Http404
  return render_to_response('events/event_day_list.html', {'events': events})

def getUpcomingEvents(maxEvents):
  ''' Gets the upcoming events and returns a total of MaxEvents in a dict'''
  #now = datetime.datetime(2011,11,1,0,0,0)
  now = datetime.datetime.now()
  nMonth = now.month+1
  if nMonth > 12:
    (nMonth, nYear) = (1, now.year+1)
  else:
     nYear = now.year
  events = Event.objects.all().filter(event_is_published=True,
                 event_is_declined=False,
                 event_date__gte=datetime.date(now.year, now.month, now.day),
                 event_date__lte=datetime.date(nYear, nMonth, now.day)).order_by('event_date')[:maxEvents]
  return events

def requestEvent(request):
  if request.method == 'POST': # if form has been submitted...
   form = EventForm(request.POST)
   if form.is_valid():
    # form passed validation, and objects in form.cleaned_data dict.
    fd = form.cleaned_data
    try:
      event = Event(event_title=fd['event_title'], event_date=fd['event_date'],
                event_duration=fd['event_duration'],
                event_audience=fd['event_audience'],
                event_visitors=fd['event_visitors'],
                event_component_vizwall=fd['event_component_vizwall'],
                event_component_3dtv=fd['event_component_3dtv'],
                event_component_omni=fd['event_component_omni'],
                event_component_hd2=fd['event_component_hd2'],
                event_component_smart=fd['event_component_smart'],
                event_assistance=fd['event_assistance'],
                event_contact_name=fd['event_contact_name'],
                event_contact_dept=fd['event_contact_dept'],
                event_contact_exec=fd['event_contact_exec'],
                event_contact_phone=fd['event_contact_phone'],
                event_contact_email=fd['event_contact_email'],
                event_details=fd['event_details'])
      # conflicts are checked upon form validation method so no checking here!
      event.save()
      # send mail to schedulers about new event
      schedulers = [u.user.email for u in UserProfile.objects.all().filter(is_scheduler=True,force_no_emails=False)]
      subject=SCHED_NEW_REQUEST[0] % (event.event_title, event.event_date)
      message=SCHED_NEW_REQUEST[1] % (event.pk, event.pk, event.event_title, event.event_date, event.event_details)
      mass_email(subject, message, recipients=schedulers)
      # send mail confirmation to requester
      recipients = [event.event_contact_email]
      subject=REQUESTER_NEW_REQUEST[0] % (event.event_title, event.event_date)
      message=REQUESTER_NEW_REQUEST[1] % (event.event_contact_name, event.event_title, event.event_date, event.event_details)
      mass_email(subject, message, recipients=recipients)
    except:
      # Something bad happened, apologize and tell them to contact us.
      return render_to_response('events/eventrequest.html', {'form': form}, context_instance=RequestContext(request))
    # eveything suceeded, lets redirect for confirmation!
    return HttpResponseRedirect('/events/request/confirm/')
  else:
    # they need to fill the form out
    form = EventForm()
  return render_to_response('events/eventrequest.html', {'form': form}, context_instance=RequestContext(request))

def requestConfirm(request): #TODO
  return render_to_response('events/event_confirm_submission.html', {})

def requestStatus(request, event_id): # TODO
  return render_to_response('events/event_status.html', {})
