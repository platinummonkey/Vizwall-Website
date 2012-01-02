from django.db import models
from django.utils.safestring import mark_safe
import datetime

# Create your models here.
class PlanarPage(models.Model):
  title = models.CharField(max_length=200, help_text='Static Page Title')
  last_modified = models.DateTimeField(auto_now_add=True)
  content_main = models.TextField(help_text='Main page content - allows full HTML')
  content_right = models.TextField(blank=True,null=True,help_text='Right side content - allows full HTML')

  class Meta:
    ordering = ['title', '-last_modified']

  def __unicode__(self):
    return self.title

  def get_title(self):
    return mark_safe(self.title)

  def get_content_main(self):
    return mark_safe(self.content_main)

  def get_content_right(self):
    return mark_safe(self.content_right)

