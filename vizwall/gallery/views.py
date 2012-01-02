# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response

from vizwall.gallery.models import PhotoGallery

def haptic(request, pk_id):
  gallery = PhotoGallery.objects.get(pk=pk_id)
  return render_to_response('gallery/gallery.html',{'title': 'Haptic', 'gallery': gallery}, context_instance=RequestContext(request))

def vizwall(request, pk_id):
  gallery = PhotoGallery.objects.get(pk=pk_id)
  return render_to_response('gallery/gallery.html',{'title': 'Vis Wall', 'gallery': gallery}, context_instance=RequestContext(request))
