from vizwall.planarpages.models import PlanarPage

def newPage(title,content_main,content_right):
  ''' currently an admin method only available via the shell '''
  flatpage = PlanarPage(title=title,content_main=content_main,content_right=content_right)
  flatpage.save()
  return flatpage
