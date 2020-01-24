"""
This is a spider which scraps events from the Dept of Archaeology University of Cambridge
events page based on seminar series chosen by the user. It cycles through 1 year of events.
The information is checked and outputted as a dictionary to the item pipeline
CalendarScrapPipeline.

Author: Leah Brainerd

Set DEPTH_LIMIT prior to running
"""

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess


class CalendarSpider (CrawlSpider):

    # CrawlSpider is the most common basic spider which allows for rules to be added
    # Required to identify the spider and needs to be unique
    name = "events"
    allowed_domains = ['arch.cam.ac.uk']
    # The starting URL for scrapping, change if you want to start at a different week
    start_urls = ['https://www.arch.cam.ac.uk/events']

    # Defines how many weeks of the calendar you want to go through by limiting the
    # amount of pages crawled before stopping. Change to 1 less than the number you want.
    custom_settings = {
        # 52
        'DEPTH_LIMIT': 51
    }

    def parse(self, response):
        # Loop through all events on a page and store the information in a dictionary for use in the pipeline
        for event in response.css('div.ds-1col.node.node-event-instance.view-mode-weekly_event_calendar.clearfix'):
            # Check if there is an end time and pull, if not then value of 0
            if len(event.css('span[datatype*="xsd:dateTime"]::attr(content)').getall()) == 2:
                endTimePull = event.css('span[datatype*="xsd:dateTime"]::attr(content)')[1].get()
            elif len(event.css('span[datatype*="xsd:dateTime"]::attr(content)').getall()) == 1:
                endTimePull = 0

            # Check if there is a location and pull, if not then value of 0
            if len(event.css('div.field-name-field-event-location .even::text')) == 1:
                locationPull = event.css('div.field-name-field-event-location .even::text').get()
            else:
                locationPull = 0

            # Check if there is a speaker and pull, if not then value of 0
            if len(event.css('div.field-name-field-event-speaker .even::text')) == 1:
                speakerPull = event.css('div.field-name-field-event-speaker .even::text').get()
            else:
                speakerPull = 0

            # Throw it in a dictionary and return it.
            yield {
                'Title': event.css('a::text').get(),
                'Series': event.css('a::text')[1].get(),
                'StartTime': event.css('span[datatype*="xsd:dateTime"]::attr(content)').get(),
                'EndTime': endTimePull,
                'Location': locationPull,
                'Speaker': speakerPull,
            }

        # Shortcut to pull the next week from the "Next" button and run it
        for a in response.css('li.date-next a'):
            yield response.follow(a, callback=self.parse)



