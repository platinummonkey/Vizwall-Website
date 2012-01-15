from django.db import models
from vizwall.settings import UPLOAD_ROOT, NEWS_UPLOAD_URL
import datetime

from vizwall.utils import CustomFileSystemStorage as CFSS

upload_storage = CFSS(location=UPLOAD_ROOT, base_url=NEWS_UPLOAD_URL)

# Create your models here.
class News(models.Model):
  title = models.CharField(max_length=200, help_text='A short descriptive title')
  pub_date = models.DateTimeField(auto_now_add=True)
  article = models.TextField(help_text='The news article text itself.')
  image = models.ImageField(upload_to='news/', default='news/default_picture.jpg', help_text='Select an image to upload', storage=upload_storage)
  #image_thumb = ImageSpec([resize.Fit(width=80, height=80, upscale=True)], image_field='image', format='JPEG', options={'quality': 85}, storage=upload_storage, autoconvert=True, pre_cache=True, cache_to='/news')
  #image_thumb = models.ImageField(upload_to='/media/news/thumbs', default='/media/site_images/news_thumb.jpg', help_text='Thumbnail image should be 80px x 80px')
  outside_link = models.URLField(verify_exists=False, blank=True, null=True, help_text='An outside link to the original article if available')
  is_published = models.BooleanField(default=False, help_text='Publish this news item?')
  
  class Meta:
    # orders by descending pub_date and ascending (alphabetical) title
    ordering = ['-pub_date', 'title']

  def __unicode__(self):
    return self.title
