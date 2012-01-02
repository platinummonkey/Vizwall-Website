from django.forms import ModelForm
from django.forms.widgets import Textarea
from vizwall.planarpages.models import PlanarPage

class PlanarPageFormAdmin(ModelForm):
  '''PlanarPage form - for superusers only'''
  class Meta:
    model=PlanarPage
    exclude=('last_modified')
    widgets = {
           'title': Textarea(attrs={'cols':90, 'rows':1}),
           'content_main': Textarea(attrs={'cols':90, 'rows':20}),
           'content_right': Textarea(attrs={'cols':90, 'rows':20}),
           }

