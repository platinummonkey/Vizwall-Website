from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from vobject import iCalendar
from email.mime.text import MIMEText
import datetime

def mail_send(recipients, event, templateBase, calendar=False, calendarCancel=False):
  from_email = 'no-reply@vizlab.utsa.edu'
  subject_t = get_template(templateBase+'_subject.txt')
  plaintext_t = get_template(templateBase+'.txt')
  html_t = get_template(templateBase+'.html')
  d = Context({'event': event})
  subject_content = subject_t.render(d) 
  plaintext_content = plaintext_t.render(d)
  html_content = html_t.render(d)
  msg = EmailMultiAlternatives(subject_content, plaintext_content, from_email, recipients)
  msg.attach_alternative(html_content, "text/html")
  if calendar:
    cal = iCalendar()
    cal.add('method').value = 'PUBLISH' if not calendarCancel else 'CANCEL'
    vevent = cal.add('vevent')
    vevent.add('dtstart').value = event.event_date if not calendarCancel else 'CANCELLED'
    vevent.add('dtend').value = event.get_end_date() if not calendarCancel else 'CANCELLED'
    vevent.add('summary').value = event.event_title if not calendarCancel else 'CANCELLED'
    vevent.add('description').value = event.event_title if not calendarCancel else 'CANCELLED'
    calendarCancel: vevent.add('status').value = 'ACTIVE' if not calendarCancel else 'CANCELLED'
    vevent.add('uid').value = event.pk
    vevent.add('dtstamp').value = datetime.datetime.now() if not calendarCancel else 'CANCELLED'
    icalstream = cal.serialize()
    part = MIMEText(icalstream,'calendar')
    part.add_header('Filename','event.ics')
    part.add_header('Content-Disposition', 'attachment; filename=event.ics')
    msg.attach(part)
  msg.send()
