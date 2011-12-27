# Create your views here.

import datetime
import random
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404

# Email actions
from django.core.mail import send_mail
from vizwall.accounts.models import UserProfile

# Events stuff
from vizwall.events.models import Event
from vizwall.events.viewscalendar import formatEvents
from vizwall.events.forms import *

# Reports
from vizwall.events.customadmin.reports import EventFilterSet
from django.db.models import Avg, Sum, Count, Max, Min #, StdDev, Varience
import csv

# debug
DEBUGSENDMAIL = False

def is_scheduler(u):
  if u.is_authenticated():
    if u.profile.is_scheduler or u.is_superuser:
      return True
  return False


def getPendingEvents(request):
  user = request.user
  pendingEvents = None
  if user.profile.is_scheduler or user.is_superuser: #allowed to view and edit
    try:
      pendingEvents = Event.objects.all().filter(event_is_published=False, event_is_declined=False).order_by('event_req_date', 'event_title')
    except:
      pendingEvents = None
  return pendingEvents

def getActiveEvents():
  try:
    activeEvents = Event.objects.all().filter(event_is_published=True)
  except:
    activeEvents = None
  return activeEvents

def getDeclinedEvents(request):
  user = request.user
  declinedEvents = None
  if user.profile.is_scheduler or user.is_superuser: # allowed to view/edit
    try:
      declinedEvents = Event.objects.all().filter(event_is_declined=True)
    except:
      declinedEvents = None
  return declinedEvents


@staff_member_required
def index(request):
  ''' Default events view that displays pending events and report generation '''
  pendingEvents = getPendingEvents(request)[:5]
  activeEvents = getActiveEvents()[:5]
  declinedEvents = getDeclinedEvents(request)[:5]
  return render_to_response('events/customadmin/index.html',{'pendingevents': pendingEvents,'activeevents':activeEvents},context_instance=RequestContext(request))


# Page listings
@user_passes_test(is_scheduler)
def pendingEvents(request):
  ''' Shows events that are pending and need approval/editing '''
  user = request.user
  if user.profile.is_scheduler or user.is_superuser:
    pendingevents = getPendingEvents(request)
    return render_to_response('events/customadmin/event_list.html',{'mode': 'pending', 'pendingevents': pendingevents},context_instance=RequestContext(request))
  else: # they are not a scheduler and only get to see currently published events
    return HttpResponseRedirect('/admin/events/active/')

@user_passes_test(is_scheduler)
def declinedEvents(request):
  ''' Shows events that are pending and need approval/editing '''
  user = request.user
  if user.profile.is_scheduler or user.is_superuser:
    declinedevents = getDeclinedEvents(request)
    return render_to_response('events/customadmin/event_list.html',{'mode': 'declined', 'declinedevents': declinedevents},context_instance=RequestContext(request))
  else: # they are not a scheduler and only get to see currently published events
    return HttpResponseRedirect('/admin/events/active/')

@staff_member_required
def activeEvents(request):
  activeEvents = getActiveEvents()
  return render_to_response('events/customadmin/event_list.html', {'mode': 'active', 'activeevents': activeEvents}, context_instance=RequestContext(request))

# end page listings

# Un/Decline
@user_passes_test(is_scheduler)
def undoDecline(request, event_id):
  ''' Removed 'Declined' Status of event and allows it to show back up in pending events'''
  event = get_object_or_404(Event, pk=event_id)
  event.event_is_declined = False
  event.event_is_published = False
  event.save()
  return HttpResponseRedirect('/admin/events/declined/')


@user_passes_test(is_scheduler)
def declineEvent(request, event_id, redirectURL='/admin/events/requests/'):
  ''' Removed 'Declined' Status of event and allows it to show back up in pending events'''
  event = get_object_or_404(Event, pk=event_id)
  event.event_is_declined = True
  event.event_is_published = False
  event.save()
  return HttpResponseRedirect(redirectURL)

# Scheduler Permissions

@user_passes_test(is_scheduler)
def newEvent(request, redirectURL='/admin/events/requests/'):
  if request.method == 'POST':
    form = EventFormAdmin(request.POST)
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
                  event_details=fd['event_details'],
                  event_is_published=fd['event_is_published'],
                  event_is_declined=fd['event_is_declined'],
                  event_assigned_proctors=fd['event_assigned_proctors'])
        # conflicts are checked upon form validation method so no checking here!
        event.save()
        # don't send mail to schedulers! they already know!
        # send mail confirmation to requester
        recipients = [event.event_contact_email]
        subject='VizLab Request: %s %s' % (event.event_title, event.event_date)
        message='%s,\n\n  Thank you for your request. Please be patient while your event is reviewed prior to approval.\n\n%s\n%s\n%s\n\n -VizLab Team\n\n--This is an automated message, replying to this message will be ignored.' % (event.event_contact_name, event.event_title, event.event_date, event.event_details)
        if DEBUGSENDMAIL: send_mail(subject, message, sender, recipients)
      except:
        # Something bad happened, apologize and tell them to contact us.
        return render_to_response('events/customadmin/eventrequest.html', {'form': form}, context_instance=RequestContext(request))
      # eveything suceeded, lets redirect to pending events page
      return HttpResponseRedirect(redirectURL)
  else:
    # they need to fill the form out
    form = EventForm()
  return render_to_response('events/eventrequest.html', {'form': form}, context_instance=RequestContext(request))


@user_passes_test(is_scheduler)
def editEvent(request, event_id, redirectURL='/admin/events/requests/'):
  event = get_object_or_404(Event, pk=event_id)
  if request.method == 'POST': # form submitted
    form = EventFormAdmin(request.POST, instance=event) # repopulate form with edited data
    if form.is_valid(): # valid edits
      fd = form.cleaned_data
      event.event_last_modified = datetime.datetime.now()
      event.event_title = fd['event_title']
      event.event_date = fd['event_date']
      event.event_duration=fd['event_duration']
      event.event_audience=fd['event_audience']
      event.event_visitors=fd['event_visitors']
      event.event_component_vizwall=fd['event_component_vizwall']
      event.event_component_3dtv=fd['event_component_3dtv']
      event.event_component_omni=fd['event_component_omni']
      event.event_component_hd2=fd['event_component_hd2']
      event.event_component_smart=fd['event_component_smart']
      event.event_assistance=fd['event_assistance']
      event.event_contact_name=fd['event_contact_name']
      event.event_contact_dept=fd['event_contact_dept']
      event.event_contact_exec=fd['event_contact_exec']
      event.event_contact_phone=fd['event_contact_phone']
      event.event_contact_email=fd['event_contact_email']
      event.event_details=fd['event_details']
      event.event_is_published=fd['event_is_published']
      event.event_is_declined=fd['event_is_declined']
      event.event_assigned_proctors=fd['event_assigned_proctors']
      event.save()
      return HttpResponseRedirect(redirectURL)
  else:
    form = EventFormAdmin(instance=event)
  return render_to_response('events/customadmin/event_edit.html', {'form': form, 'event_id': event_id, 'req_date': event.event_req_date, 'last_mod_date': event.event_last_modified}, context_instance=RequestContext(request))

@user_passes_test(is_scheduler)
def deleteEvent(request, event_id, redirectURL='/admin/events/requests/'):
  ''' Delete Event object '''
  event = get_object_or_404(Event, pk=event_id)
  if request.method == 'POST': # form submitted
    if request.POST['confirm'] == u'Yes':
      event.delete() # deletes! no backups!
    return HttpResponseRedirect(redirectURL)
  return render_to_response('events/customadmin/confirm.html', {'mode': 'delete', 'event_id': event_id, 'event': event}, context_instance=RequestContext(request))

@user_passes_test(is_scheduler)
def deactivateEvent(request, event_id, redirectURL='/admin/events/requests/'):
  ''' Deactivate Event object '''
  event = get_object_or_404(Event, pk=event_id)
  if request.method == 'POST': # form submitted
    if request.POST['confirm'] == u'Yes':
      event.is_published=False
      event.is_declined=False
      event.save()
    return HttpResponseRedirect(redirectURL)
  return render_to_response('events/customadmin/confirm.html', {'mode': 'deactivate', 'event_id': event_id, 'event': event}, context_instance=RequestContext(request))


@user_passes_test(is_scheduler)
def requestConfirm(request, event_id, redirectURL='/admin/events/requests/'):
  ''' Publish Event object '''
  event = get_object_or_404(Event, pk=event_id)
  event.event_is_published = True
  event.event_is_declined = False
  event.save()
  return HttpResponseRedirect(redirectURL)



##### old shit

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


def requestConfirm(request): #TODO
  return render_to_response('events/event_confirm_submission.html', {})

def requestStatus(request, event_id): # TODO
  return render_to_response('events/event_status.html', {})

##### REPORTS #####
def getDownloadLink(request,type='csv'):
  dl = request.get_full_path().split('?')
  dl[0] = dl[0] + 'generate/%s/?' % type
  return ''.join(dl)


def getActiveOverallStats():
  f = EventFilterSet({'event_is_published':True,'event_is_decilned':False})
  numEvents = f.qs.count()
  duration_avg = int(f.qs.aggregate(Avg('event_duration')).values()[0])
  visitors_avg = int(f.qs.aggregate(Avg('event_visitors')).values()[0])
  numVizwall = f.qs.filter(event_component_vizwall=True).aggregate(Count('event_component_vizwall')).values()[0]
  num3dtv = f.qs.filter(event_component_3dtv=True).aggregate(Count('event_component_3dtv')).values()[0]
  numOmni = f.qs.filter(event_component_omni=True).aggregate(Count('event_component_omni')).values()[0]
  numHD2 = f.qs.filter(event_component_hd2=True).aggregate(Count('event_component_hd2')).values()[0]
  numSmart = f.qs.filter(event_component_smart=True).aggregate(Count('event_component_smart')).values()[0]
  return (('Total # Events', numEvents),
          ('Duration Average', duration_avg),
          ('Visitors Average', visitors_avg),
          ('Vis Wall Requests', numVizwall),
          ('3D TV Requests', num3dtv),
          ('Omni Requests', numOmni),
          ('HD2 Requests', numHD2),
          ('Smart Board Requests', numSmart))
  


@user_passes_test(is_scheduler)
def reportsIndex(request, download=None):
  f = EventFilterSet(request.GET or None)
  numEvents = f.qs.count()
  duration_avg = int(f.qs.aggregate(Avg('event_duration')).values()[0])
  visitors_avg = int(f.qs.aggregate(Avg('event_visitors')).values()[0])
  numVizwall = f.qs.filter(event_component_vizwall=True).aggregate(Count('event_component_vizwall')).values()[0]
  num3dtv = f.qs.filter(event_component_3dtv=True).aggregate(Count('event_component_3dtv')).values()[0]
  numOmni = f.qs.filter(event_component_omni=True).aggregate(Count('event_component_omni')).values()[0]
  numHD2 = f.qs.filter(event_component_hd2=True).aggregate(Count('event_component_hd2')).values()[0]
  numSmart = f.qs.filter(event_component_smart=True).aggregate(Count('event_component_smart')).values()[0]
  csvDownloadLink = getDownloadLink(request,'csv')
  
  if download == 'csv':
    # Generate CSV for download
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=report_generation_%s.csv' % datetime.datetime.now().strftime('%m%d%Y_%H%M')
    writer = csv.writer(response)
    writer.writerow(['# Events','Duration Average','Visitors Average',
                     '# Vis Wall Requests', '# 3D TV Requests', '# Omni Requests',
                     '# HD2 Requests', '# Smart Board Requests', 'CSV Link'])
    writer.writerow([numEvents,duration_avg,visitors_avg,numVizwall,num3dtv,numOmni,
                     numHD2,numSmart,'http://vizwall.utsa.edu'+csvDownloadLink])
    writer.writerow([]) # spacer
    writer.writerow(['Event Title','Published','Declined','Event Request Date',
                     'Published Date','Last Modified','Event Date','Duration',
                     'Visitors','Audience','Vis Wall','3D TV','Omni','HD2',
                     'Smart Board','Assistance','Contact Name','Contact Dept',
                     'Contact Exec','Contact Phone','Contact Email','Proctors',
                     'Event Details'])
    for e in f.qs:
      proctors = []
      for u in e.event_assigned_proctors.all():
        proctors.append(str(u.get_full_name()))
      if proctors:
        proctors = ';'.join(proctors)
      else:
        proctors = ''
      writer.writerow([str(e.event_title),str(e.event_pub_date),str(e.event_is_declined),
                       str(e.event_req_date),str(e.event_pub_date),str(e.event_last_modified),
                       str(e.event_date),str(e.event_duration),str(e.event_visitors),
                       str(e.event_audience),str(e.event_component_vizwall),
                       str(e.event_component_3dtv),str(e.event_component_omni),
                       str(e.event_component_hd2),str(e.event_component_smart),
                       str(e.event_assistance),str(e.event_contact_name),
                       str(e.event_contact_dept),str(e.event_contact_exec),
                       str(e.event_contact_phone),str(e.event_contact_email),
                       proctors,str(e.event_details)])
    return response
  # Else render display results page
  return render_to_response('events/customadmin/report_index.html', {'filter': f, 'count': numEvents, 'duration_avg': duration_avg, 'visitors_avg': visitors_avg, 'count_vizwall': numVizwall, 'count_3dtv': num3dtv, 'count_omni': numOmni, 'count_hd2': numHD2, 'count_smart': numSmart, 'csvDownloadLink': csvDownloadLink}, context_instance=RequestContext(request))
