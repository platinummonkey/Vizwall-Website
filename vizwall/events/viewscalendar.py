# Create your views here.

import datetime
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from calendar import HTMLCalendar, day_name, day_abbr
from vizwall.events.models import Event

monthNames = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
              5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September',
              10: 'October', 11: 'November', 12: 'December'}

class VizCalendar(HTMLCalendar):
  '''Custom HTML Calendar to format for Vis Wall Calendar'''
  def __init__(self, events, startDayOfWeek=6):
    '''Define a new calendar starting on Sunday with event collection'''
    super(VizCalendar, self).__init__()
    self.setfirstweekday(startDayOfWeek)
    self.events = events # expects a dictionary - keys are days of month, values are list of Event object models {'1': [<Event object>,...],...}
    self.vCSSclasses = {'weekrow': 'calendar-row',
                        'dayhead': 'calendar-day-head',
                        'daynp':   'calendar-day-np',
                        'day':     'calendar-day',
                        'daynumber': 'day-number'}
    self.maxEventsPerDay = 2

  def formatday(self, day, weekday):
    if day in self.events:
      ''' the day has events'''
      body=['<div class="%s">%s</div>' % (self.vCSSclasses['daynumber'], day)]
      i = 0 # just to make sure we don't show too many events
      for event in self.events[day]:
        if i < self.maxEventsPerDay:
          body.append('<p>')
          body.append('<strong><a href="/events/event/%s/">%s</a></strong><br>' % (event.pk, event.event_title))
          body.append(event.event_date.strftime('%I:%M %p'))
          body.append('</p>')
        else:
          break
        i += 1
      body.append('</div>')
    else:
      ''' the day has no events'''
      body=['<div class="%s">%s</div>' % (self.vCSSclasses['daynumber'], day)]
      body.append('<p>&nbsp;</p><p>&nbsp;</p>')
      if day is 0:
        return self.day_cell(self.vCSSclasses['daynp'], '&nbsp;')
    #return self.day_cell(self.vCSSclasses['day'], '%d %s')
    return self.day_cell(self.vCSSclasses['day'], '%s' % ''.join(body))
  

  def formatweek(self, theweek):
    ''' return a complete week as a row'''
    s = ''.join(self.formatday(d,wd) for (d,wd) in theweek)
    return '<tr class="%s">%s</tr>' % (self.vCSSclasses['weekrow'],s)
    
  
  def formatweekday(self, day):
    ''' Format weeday name as a table data''' 
    return '<td class="%s">%s</td>' % (self.vCSSclasses['dayhead'], day_name[day])

  def formatmonth(self, theyear, themonth, withyear=True):
    ''' Formats the outlining HTML table for the month'''
    v = []
    a = v.append
    a('<table cellpadding="0" cellspacing="0" class="calendar">') #\n<tbody>')
    a('\n')
    a(self.formatweekheader())
    a('\n')
    for week in self.monthdays2calendar(theyear, themonth):
      a(self.formatweek(week))
      a('\n')
    #a('</tbody></table>')
    a('</table>')
    a('\n')
    return ''.join(v)

  def day_cell(self, cssclass, body):
    return '<td class="%s">%s</td>' % (cssclass, body)

def formatEvents(eventQuery):
  '''Converts list of Event objects into dictionary format based on day value
  {'1': [<Event Object>, ... ], ... }'''
  events = {}
  # compile events list into 
  for e in eventQuery:
    if e.event_date.day in events:
      events[e.event_date.day].append(e)
    else:
      events[e.event_date.day] = [e]
  return events

def nextPrevMonth(curDateTime):
  '''Returns the previous and next month/year values'''
  cMonth = curDateTime.month
  cYear = curDateTime.year
  (nMonth, pMonth) = (cMonth+1, cMonth-1)
  if nMonth > 12:
    (nMonth, nYear) = (1, cYear+1)
  else:
    nYear = cYear
  if pMonth < 1:
    (pMonth, pYear) = (12, cYear-1)
  else:
    pYear = cYear
  return (nMonth, nYear, pMonth, pYear)
  

#### Views
def thisMonth(request):
  ''' This is the default calendar view with current month/year. '''
  d = datetime.datetime.today()
  try:
    eventQuery = Event.objects.all().filter(event_date__year=d.year, event_date__month=d.month, event_is_published=True).order_by('event_date')
    events = formatEvents(eventQuery)
  except:
    events = {}
  c = VizCalendar(events)
  calTable = c.formatmonth(d.year, d.month)
  (nMonth, nYear, pMonth, pYear) = nextPrevMonth(d)
  return render_to_response('events/calendar.html', {'month': d.month, 'monthName': monthNames[d.month], 'year': d.year, 'calendar': calTable, 'nextMonth': nMonth, 'nextYear': nYear, 'prevMonth': pMonth, 'prevYear': pYear}, context_instance=RequestContext(request))

def someMonth(request, year, month):
  ''' This method is for displaying a calendar on any other month'''
  d = datetime.datetime.today()
  try:
    (year, month) = (int(year), int(month))
    if year in range(d.year-5, d.year+5): # within +/- 5 years - can always change this, but this seemed reasonable.
      if month in range(1,13): # need 13, range doesn't include final value!
        eventQuery = Event.objects.all().filter(event_date__year=year, event_date__month=month, event_is_published=True)
        events = formatEvents(eventQuery)
        c = VizCalendar(events)
        calTable = c.formatmonth(year, month)
        (nMonth, nYear, pMonth, pYear) = nextPrevMonth(datetime.datetime(year, month, 1, 0, 0, 0))
        return render_to_response('events/calendar.html',{'month': month, 'monthName': monthNames[month], 'year': year, 'calendar': calTable, 'nextMonth': nMonth, 'nextYear': nYear, 'prevMonth': pMonth, 'prevYear': pYear}, context_instance=RequestContext(request))
  except:
    pass
  return render_to_response('events/calendar_error.html',{'month': month, 'monthName': '', 'year': year, 'calendar': '', 'nextMonth': '', 'nextYear': '', 'prevMonth': '', 'prevYear': ''}, context_instance=RequestContext(request))

