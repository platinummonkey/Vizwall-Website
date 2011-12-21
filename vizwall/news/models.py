from django.db import models
import datetime

# Create your models here.
class News(models.Model):
  title = models.CharField(max_length=200, help_text='A short descriptive title')
  pub_date = models.DateTimeField(auto_now_add=True)
  article = models.TextField(help_text='The news article text itself.')
  image = models.ImageField(upload_to='/media/news', default='/media/site_images/news_image.jpg', help_text='Select an image to upload')
  image_thumb = models.ImageField(upload_to='/media/news/thumbs', default='/media/site_images/news_thumb.jpg', help_text='Thumbnail image should be 80px x 80px')
  outside_link = models.URLField(verify_exists=False, blank=True, null=True, help_text='An outside link to the original article if available')
  is_published = models.BooleanField(default=False, help_text='Publish this news item?')
  
  class Meta:
    # orders by descending pub_date and ascending (alphabetical) title
    ordering = ['-pub_date', 'title']

  def __unicode__(self):
    return self.title
