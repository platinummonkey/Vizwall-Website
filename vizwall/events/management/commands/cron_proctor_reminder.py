from django.core.management.base import NoArgsCommand
from vizwall.events.models import Event
from vizwall.mailer import mail_send
import datetime

class Command(NoArgsCommand):
  args = '<No arguments for this command>'
  help = 'Sends reminders to proctors about an event they have been assigned to that day'

  def handle_noargs(self, **options):
    n = datetime.datetime.now()
    t = n + datetime.timedelta(days=1)
    events = Event.objects.all().filter(
          event_date__gte=datetime.date(n.year, n.month, n.day),
          event_date__lte=datetime.date(t.year, t.month, t.day),
          event_is_published=True, event_is_declined=False)
    if events:
      for event in events:
        ps = event.get_assigned_proctors_can_email()
        if ps:
          proctors = [u.email for u in ps]
          mail_send(ps, event, 'mail/proctor_reminder')
          #self.stdout.write(str(event)+': '+repr(proctors))

