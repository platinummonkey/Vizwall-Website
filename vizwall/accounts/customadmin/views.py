# Create your views here.

import datetime
import random
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required

# Email actions
from django.core.mail import send_mail
from vizwall.accounts.models import UserProfile

# Events stuff
from vizwall.events.models import Event
from vizwall.events.viewscalendar import formatEvents
from vizwall.events.forms import *

# debug
DEBUGSENDMAIL = False

@staff_member_required
def index(request):
  ''' Default events view that displays pending events and report generation '''
  user = request.user
  if user.profile.is_scheduler or user.is_superuser: # they can make changes to pending events
    return render_to_response('events/customadmin/index.html',{},context_instance=RequestContext(request))
  else: # they are not a scheduler and only get to see currently published events
    return render_to_response('events/customadmin/event_active_list.html',{},context_instance=RequestContext(request))


@staff_member_required
def activeEvents(request):
  return render_to_response('events/customadmin/event_active_list.html', {}, context_instance=RequestContext(request))

@staff_member_required
def editEvent(request, event_id):
  return render_to_response('events/customadmin/event_edit.html', {}, context_instance=RequestContext(request))

@staff_member_required
def deleteEvent(request, event_id):
  return render_to_response('events/customadmin/event_delete.html', {}, context_instance=RequestContext(request))

@staff_member_required
def deactivateEvent(request, event_id):
  return render_to_response('events/customadmin/event_deactivate.html', {}, context_instance=RequestContext(request))

@staff_member_required
def requestConfirm(request, event_id):
  return render_to_response('events/customadmin/event_confirm.html', {}, context_instance=RequestContext(request))



def displaySingleEvent(request, event_id):
  ''' Display a single event, template controls what is public and private'''
  try:
    event = Event.objects.get(pk=event_id)
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
          eventQuery = Event.objects.all().filter(event_date__year=year, event_date__month=month, event_date__day=day, event_is_published=True)
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
  events = Event.objects.all().filter(
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
      schedulers = UserProfile.objects.all().filter(is_scheduler=True,force_no_emails=False)
      recipients = []
      for s in schedulers:
        recipients.append(s.user.email)
      sender='no-reply@vizwall.utsa.edu'
      subject='New Request: %s %s' % (event.event_title, event.event_date)
      message='VizLab Scheduler,\n  There is a new event requested. Please review the request: <a href="http://vizlab.utsa.edu/admin/events/edit/%s/">http://vizlab.utsa.edu/admin/events/edit/%s/</a>\n\n%s\n%s\n%s\n\n --Automated Message' % (event.pk, event.pk, event.event_title, event.event_date, event.event_details)
      if DEBUGSENDMAIL: send_mail(subject, message, sender, recipients)
      # send mail confirmation to requester
      recipients = [event.event_contact_email]
      subject='VizLab Request: %s %s' % (event.event_title, event.event_date)
      message='%s,\n\n  Thank you for your request. Please be patient while your event is reviewed prior to approval.\n\n%s\n%s\n%s\n\n -VizLab Team\n\n--This is an automated message, replying to this message will be ignored.' % (event.event_contact_name, event.event_title, event.event_date, event.event_details)
      if DEBUGSENDMAIL: send_mail(subject, message, sender, recipients)
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
