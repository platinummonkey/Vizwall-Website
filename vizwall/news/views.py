# Create your views here.

import datetime
import random
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from vizwall.news.models import News
#from vizwall.news.forms import *

def index(request, page=0):
  news = News.objects.all().filter(is_published=True)
  return render_to_response('news/index.html', {'news': news}, context_instance=RequestContext(request))

def newsDetail(request, news_id):
  ''' Display News article '''
  try:
    news = News.objects.get(pk=news_id)
  except:
    return render_to_response('news/not_found.html', {'news_id': news_id},context_instance=RequestContext(request))
  if news.is_published or request.user.profile.is_scheduler or request.user.is_superuser:
    return render_to_response('news/details.html', {'news': news}, context_instance=RequestContext(request))
  else:
    return render_to_response('news/not_found.html', {'news_id': news_id},context_instance=RequestContext(request))

def getRecentNews(numArticles):
  news = News.objects.all().filter(is_published=True)[:numArticles]
  return news
