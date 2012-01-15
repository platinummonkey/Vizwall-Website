from django.forms import *
from django.forms.widgets import *
from django.forms.extras.widgets import *
from vizwall.news.models import News
from vizwall.events.models import dTimeFieldInputs
import datetime

class NewsFormAdmin(ModelForm):
  '''News form, for admin view only'''
  class Meta:
    model = News
    #fields = ()
    exclude=('pub_date', 'image_formatted', 'image_thumb')
    widgets = {
        'article': Textarea(attrs={'cols':50, 'rows': 10}),
        'is_published': CheckboxInput(),
        }

  def clean_pub_date(self):
    self.cleaned_data['pub_date'] = datetime.datetime.now()
    return self.cleaned_data['pub_date']
