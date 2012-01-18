from django.core.management.base import NoArgsCommand
from vizwall.news.models import News
import datetime

class Command(NoArgsCommand):
  args = '<No arguments for this command>'
  help = 'Sends reminders to proctors about an event they have been assigned to that day'

  def handle_noargs(self, **options):
    while True:
      title = raw_input('Title: ')
      pub_date = raw_input('Published Date: ')
      if not pub_date:
        pub_date = datetime.datetime.now()
      else:
        pub_date = datetime.datetime.strptime(pub_date, '%m/%d/%Y %H:%M')
      article = raw_input('Article: ')
      outside_link = raw_input('Outside link: ')
      saveit = raw_input('Save it? [y/N]: ')
      if not saveit.lower() == 'y':
        self.stdout.write("== Not Saved! ==\n\n")
      else:
        n = News(title=title, pub_date=pub_date, article=article, outside_link=outside_link, is_published=True)
        n.pub_date = pub_date
        n.save()
        self.stdout.write("=======News article saved========\n\n")
      another = raw_input('Create a new one? [y/N]: ')
      if not another.lower() == 'y':
        break
