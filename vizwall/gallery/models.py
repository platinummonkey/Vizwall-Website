from django.db import models
from django.utils.safestring import mark_safe
import datetime

# Create your models here.
class Photo(models.Model):
  alt_text = models.CharField(blank=True, max_length=256, help_text='Alternative Text')
  image = models.ImageField(upload_to='/media/gallery/')
  rank = models.PositiveIntegerField(default=10)
  pub_date = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['rank','-pub_date']

  def __unicode__(self):
    return 'Rank %s: %s - %s' % (self.rank, self.image, self.alt_text)

  def get_html(self):
    return '<img alt="%s" src="%s" />' % (self.alt_text, self.image)
  
class PhotoGallery(models.Model):
  title = models.CharField(max_length=256)
  pictures = models.ManyToManyField(Photo)

  class Meta:
    ordering = ['title']
  
