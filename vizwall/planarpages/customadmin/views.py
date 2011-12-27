# Create your views here.

import datetime
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from vizwall.planarpages.models import PlanarPage
from vizwall.planarpages.forms import PlanarPageFormAdmin

def is_superuser(u):
  if u.is_authenticated():
    if u.is_superuser:
      return True
  return False

@user_passes_test(is_superuser)
def index(request):
  flatpages = PlanarPage.objects.all()
  return render_to_response('planarpages/customadmin/index.html',{'flatpages':flatpages},context_instance=RequestContext(request))

@user_passes_test(is_superuser)
def editPage(request, page_id):
  flatpage = get_object_or_404(PlanarPage, pk=page_id)
  if request.method == 'POST':
    form = PlanarPageFormAdmin(request.POST)
    if form.is_valid():
      fd = form.cleaned_data
      try:
        flatpage.title=fd['title']
        flatpage.last_modified=datetime.datetime.now()
        flatpage.content_main=fd['content_main']
        flatpage.content_right=fd['content_right']
        flatpage.save()
      except:
        return render_to_response('planarpages/customadmin/edit.html',{'page_id':page_id, 'form':form,'flatpage':flatpage},context_instance=RequestContext(request))
  else:
    form = PlanarPageFormAdmin(instance=flatpage)
  return render_to_response('planarpages/customadmin/edit.html',{'page_id':page_id, 'form':form,'flatpage':flatpage},context_instance=RequestContext(request))

