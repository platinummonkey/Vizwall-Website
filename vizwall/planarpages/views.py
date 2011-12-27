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
    


