# Create your views here.

from django.template import RequestContext
from django.shortcuts import render_to_response

from vizwall.planarpages.models import PlanarPage

def displayPage(request, pk_id, right=False):
  fp = PlanarPage.objects.get(pk=pk_id)
  if right:
    return render_to_response('planarpages/withrightcontent.html',{'flatpage':fp},context_instance=RequestContext(request))
  else:
    return render_to_response('planarpages/content.html',{'flatpage':fp},context_instance=RequestContext(request))
    
def error_403(request):
  fp = PlanarPage.objects.get(pk=7) # I know that 7 is the right one
  return render_to_response('planarpages/content.html',{'flatpage':fp},context_instance=RequestContext(request))

def error_404(request):
  fp = PlanarPage.objects.get(pk=5) # I know that 5 is the right one
  return render_to_response('planarpages/content.html',{'flatpage':fp},context_instance=RequestContext(request))

def error_500(request):
  fp = PlanarPage.objects.get(pk=6) # I know that 6 is the right one
  return render_to_response('planarpages/content.html',{'flatpage':fp},context_instance=RequestContext(request))
