# Create your views here.

import datetime
import random
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required

# uploaded picture handling
from vizwall.utils import handle_uploaded_picture
MAX_IMG_SIZE = (100, 100) # (width, height)
THUMB_IMG_SIZE = (50, 50)

# Email actions
from django.core.mail import send_mail
from vizwall.accounts.models import UserProfile

# News stuff
from vizwall.news.models import News
from vizwall.news.forms import *

# debug
DEBUGSENDMAIL = False

@staff_member_required
def index(request):
  ''' Default news view that displays pending and active news items '''
  news = News.objects.all()
  pagenum = None
  if request.GET and request.GET.has_key('page'):
    pagenum = request.GET['page']
  return render_to_response('news/customadmin/index.html',{'news': news, 'pagenum': pagenum},context_instance=RequestContext(request))

def newNews(request):
  ''' Create news article '''
  if request.method == 'POST': # form submitted
    form = NewsFormAdmin(request.POST, request.FILES)
    if form.is_valid():
      fd = form.cleaned_data
      news = News(title=fd['title'], article=fd['article'],
              outside_link=fd['outside_link'])
      news.save()
      if request.FILES.get('picture', False):
        (filename, content) = handle_uploaded_picture(request.FILES['picture'], MAX_IMG_SIZE, THUMB_IMG_SIZE)
        news.image.save(filename[0], content[0])
        news.image_thumb.save(filename[1], content[1])
      news.is_published=True
      news.save()
      return HttpResponseRedirect('/admin/news/')
  else: # form not submitted, create populated form for editing
      form = NewsFormAdmin()
  return render_to_response('news/customadmin/create.html', {'form': form}, context_instance=RequestContext(request))

@staff_member_required
def editNews(request, news_id):
  ''' Edit a news article '''
  try:
    news = News.objects.get(pk=news_id)
    if request.method == 'POST': # form submitted
      form = NewsFormAdmin(request.POST, request.FILES, instance=news) # repopulate form with edited data
      if form.is_valid(): # valid edits
        #form.save() # save and redirect back to the news page
        news.pub_date = datetime.datetime.now()
        news.title = form.cleaned_data['title']
        news.article = form.cleaned_data['article']
        if request.FILES.get('picture', False):
          (filename, content) = handle_uploaded_picture(request.FILES['picture'], MAX_IMG_SIZE, THUMB_IMG_SIZE)
          news.image.delete()
          news.image.save(filename[0], content[0])
          news.image_thumb.delete()
          news.image_thumb.save(filename[1], content[1])
        news.outside_link = form.cleaned_data['outside_link'] if form.cleaned_data['outside_link'] else None
        news.is_published = True if form.cleaned_data['is_published'] else False
        news.save()
        return HttpResponseRedirect('/admin/news/')
    else: # form not submitted, create populated form for editing
      form = NewsFormAdmin(instance=news)
  except News.DoesNotExist:
    raise Http404
  except:
    raise Http404
  return render_to_response('news/customadmin/edit.html', {'form': form, 'news_id': news_id, 'ndate': news.pub_date}, context_instance=RequestContext(request))

@staff_member_required
def deleteNews(request, news_id):
  ''' Delete News object '''
  try:
    news = News.objects.get(pk=news_id)
    if request.method == 'POST': # form submitted
      if request.POST['confirm'] == u'Yes':
        news.picture.delete()
        news.picture_thumb.delete()
        news.delete() # deletes! no backups!
        if request.GET and request.GET.has_key('page'):
          pagenum = request.GET['page']
          return HttpResponseRedirect('/admin/news/?page=%s' % pagenum)
      return HttpResponseRedirect('/admin/news/')
  except News.DoesNotExist:
    raise Http404
  except:
    raise Http404
  return render_to_response('news/customadmin/confirm.html', {'news_id': news_id, 'news': news}, context_instance=RequestContext(request))
  

@staff_member_required
def publishNews(request, news_id):
  ''' Publish news object '''
  try:
    news = News.objects.get(pk=news_id)
    news.is_published = True
    news.pub_date = datetime.datetime.now()
    news.save()
  except News.DoesNotExist:
    raise Http404
  except:
    raise Http404
  if request.GET and request.GET.has_key('page'):
    pagenum = request.GET['page']
    return HttpResponseRedirect('/admin/news/?page=%s' % pagenum)
  return HttpResponseRedirect('/admin/news/')

@staff_member_required
def unpublishNews(request, news_id):
  ''' Publish news object '''
  try:
    news = News.objects.get(pk=news_id)
    news.is_published = False
    news.save()
  except News.DoesNotExist:
    raise Http404
  except:
    raise Http404
  if request.GET and request.GET.has_key('page'):
    pagenum = request.GET['page']
    return HttpResponseRedirect('/admin/news/?page=%s' % pagenum)
  return HttpResponseRedirect('/admin/news/')


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
