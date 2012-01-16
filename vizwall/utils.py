# collection of common utilities

from hashlib import md5
import datetime
from os.path import splitext
from cStringIO import StringIO
import Image
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.utils.text import get_valid_filename
import urlparse, os

class CustomFileSystemStorage(FileSystemStorage):
  ''' Fix to Django's FileSystemStorage mechanism - image.url not correct '''
  def __init__(self,location,base_url,*args, **kwargs):
    super(CustomFileSystemStorage, self).__init__(*args, **kwargs)
    self.location = location
    self.base_url = base_url

  def get_valid_filename(self, name):
    ''' builting filename mechanism broken too '''
    try:
      fname = name.split(self.location)[1]
    except:
      fname = name.split('/')[-1]
    return fname

  def delete(self, name):
    ''' builtin delete function doesn't work either - workaround '''
    if name:
      fullpath = urlparse.urljoin(self.location, name)
      if os.path.exists(fullpath):
        os.remove(fullpath)

  def url(self, name, *args, **kwargs):
    ''' builtin url function needed workaround '''
    name = self.get_valid_filename(name)
    return urlparse.urljoin(self.base_url, name).replace('\\', '/')

def handle_uploaded_picture(i, maxSize, thumbSize=None, path=''):
  ''' Resizes and crops images, also generates thumbnail if thumbSize given '''
  if i:
    basename = md5(i.name+str(datetime.datetime.now())).hexdigest()
    filename_image = basename + '.jpg'
    filename_thumb = basename + '_thumb.jpg'
    resizedContentFile = crop_resize_image(i, maxSize)
    thumbContentFile = None
    if thumbSize:
      i.seek(0)
      thumbContentFile = crop_resize_image(i, thumbSize)
    return ((filename_image, filename_thumb), (resizedContentFile, thumbContentFile))
  else:
    return ((None, None), (None, None))

def crop_resize_image(i, dst_dim):
  ''' actual image resizing and crop '''
  imagefile = StringIO(i.read())
  imageImage = Image.open(imagefile)
  src_dim = imageImage.size # (width, height)
  src_ratio = float(src_dim[0])/float(src_dim[1])
  dst_ratio = float(dst_dim[0])/float(dst_dim[1])
  if dst_ratio < src_ratio:
    crop_dim = (src_dim[1] * dst_ratio, src_dim[1])
    offset_dim = (float(src_dim[0] - crop_dim[0])/2, 0)
  else:
    crop_dim = (src_dim[0], src_dim[0]/dst_ratio)
    offset_dim = (0, float(src_dim[1] - crop_dim[1])/3)
  crop_box = ( offset_dim[0], offset_dim[1],
               offset_dim[0]+int(crop_dim[0]),
               offset_dim[1]+int(crop_dim[1]) )
  imageImage = imageImage.crop(crop_box)
  newimageImage = imageImage.resize(dst_dim, Image.ANTIALIAS)
  newimagefile = StringIO()
  newimageImage.save(newimagefile, 'JPEG')
  imageContentFile = ContentFile(newimageImage.tostring('jpeg', newimageImage.mode))
  return imageContentFile

