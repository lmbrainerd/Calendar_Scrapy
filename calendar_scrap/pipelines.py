# -*- coding: utf-8 -*-
"""
This is an item pipeline. It takes the information scrapped from the Dept of Archaeology
event page in events.py as a dictionary and processes it. the information is saves as
icalendar events and written to an .ics document for use in most calendars.

Author: Leah Brainerd

Set self.file name and turn on series selection if statements if needed prior to running
"""
from datetime import datetime
from icalendar import Calendar, Event


class CalendarScrapPipeline(object):

    def open_spider(self, spider):
        # Creates an instance for the calendar
        self.cal = Calendar()

        # Required information for most calendar apps to accept an icalendar file
        self.cal.add('prodid', '-//University of Cambridge Archaeology/arch.cam.ac.uk//EN')
        self.cal.add('version', '2.0')

        # Open .ics file for calendar to be written to. Change name as needed
        self.file = open('department_calendar.ics', 'wb')

    def close_spider(self, spider):
        # After process_item, the calendar gets written to the file and closed
        self.file.write(self.cal.to_ical())
        self.file.close()

    def process_item(self, item, spider):
        # This function processes the scrapped data from each event produced by events spider
        # creates an event

        # Uncomment this if you want to get only events from one series name
        # if item['Series'] == 'African Archaeology Group':
        # Uncomment this if you want to get events from one or more. Add more OR's if you want more series
        # if item['Series'] == 'African Archaeology Group' or item['Series'] == 'Asian Archaeology Group':
            event = Event()

            # Checks if there is a speaker, if not the title for the event will be the series only
            if item['Speaker'] != 0:
                event.add('summary', item['Speaker'] + " - " + item['Series'])
            else:
                event.add('summary', item['Series'])

            # Takes the date from the css format through Python datetime to be added in ical
            startDate = item['StartTime']
            startDate = startDate[0:16]
            newdate = datetime.strptime(startDate, '%Y-%m-%dT%H:%M')
            event.add('dtstart', newdate)

            # if there is an end time it is processed, if not a default of 1hr is given by package
            if item['EndTime'] != 0:
                endDate = item['EndTime']
                endDate = endDate[0:16]
                newdate2 = datetime.strptime(endDate, '%Y-%m-%dT%H:%M')
                event.add('dtend', newdate2)

            # if there is a location it is added
            if item['Location'] != 0:
                event.add('location', item['Location'])

            # Title is added as description for event
            event.add('description', item['Title'])

            # Event is added to overall calendar
            self.cal.add_component(event)
            return item
