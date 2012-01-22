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
  subject_content = subject_t.render(d).rstrip() # need to strip off newline (SMTP error otherwise)
  plaintext_content = plaintext_t.render(d)
  html_content = html_t.render(d)
  msg = EmailMultiAlternatives(subject_content, plaintext_content, from_email, recipients)
  msg.attach_alternative(html_content, "text/html")
  if calendar:
    cal = iCalendar()
    if not calendarCancel:
      cal.add('method').value = 'PUBLISH'
      vevent = cal.add('vevent')
      vevent.add('dtstart').value = event.event_date
      vevent.add('dtend').value = event.get_end_date()
      vevent.add('summary').value = event.event_title
      vevent.add('description').value = event.event_title
      vevent.add('status').value = 'ACTIVE'
      vevent.add('uid').value = str(event.pk)
      vevent.add('dtstamp').value = datetime.datetime.now()

    else:
      cal.add('method').value = 'CANCEL'
      vevent = cal.add('vevent')
      vevent.add('dtstart').value = 'CANCELLED'
      vevent.add('dtend').value = 'CANCELLED'
      vevent.add('summary').value = 'CANCELLED'
      vevent.add('description').value = 'CANCELLED'
      vevent.add('status').value = 'CANCELLED'
      vevent.add('uid').value = str(event.pk)
      vevent.add('dtstamp').value = 'CANCELLED'

    icalstream = cal.serialize()
    part = MIMEText(icalstream,'calendar')
    part.add_header('Filename','event.ics')
    part.add_header('Content-Disposition', 'attachment; filename=event.ics')
    msg.attach(part)
  msg.send()
