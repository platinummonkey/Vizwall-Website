from django.core.management.base import NoArgsCommand
from vizwall.events.models import Event
import datetime

class Command(NoArgsCommand):
  args = '<No arguments for this command>'
  help = 'Sends reminders to proctors about an event they have been assigned to that day'

  def handle_noargs(self, **options):
    while True:
      title = raw_input('Title: ')
      edate = raw_input('Event Date: ')
      if not edate:
        edate = datetime.datetime.now()
      else:
        edate = datetime.datetime.strptime(edate, '%m/%d/%Y %H:%M')
      duration = raw_input('Duration in minutes: ')
      if not duration:
        duration = 60
      else:
        try:
          duration = int(duration)
        except:
          duration = 60
      audience = raw_input('Description of Audience: ')
      c_name = raw_input('Contact Name: ')
      c_phone = raw_input('Contact Phone: ')
      if not c_phone: c_phone = '210-458-6479'
      c_dept = raw_input('Contact Dept: ')
      if not c_dept: c_dept = 'Mechanical Engineering'
      c_email = raw_input('Contact Email: ')
      if not c_email: c_email = 'vizlab@utsa.edu'
      details = raw_input('Event Details: ')
      saveit = raw_input('Save it? [y/N]: ')
      if not saveit.lower() == 'y':
        self.stdout.write("== Not Saved! ==\n\n")
      else:
        e = Event(event_title=title, event_duration=duration, event_date=edate, event_audience=audience, event_visitors=20, event_component_vizwall=True, event_component_3dtv=True, event_component_omni=True, event_component_hd2=True, event_component_smart=True, event_assistance=True, event_contact_name=c_name, event_contact_dept=c_dept, event_contact_exec=7, event_contact_phone=c_phone, event_contact_email=c_email, event_details=details, is_published=True)
        e.pub_date = edate
        e.req_date = edate
        e.last_modified = edate
        e.save()
        self.stdout.write("=======Event saved========\n\n")
      another = raw_input('Create a new one? [y/N]: ')
      if not another.lower() == 'y':
        break
