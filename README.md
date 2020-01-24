# Calendar_Scrapy
Cambridge Department of Archaeology Events Calendar Web Scrap

This web scrapping requires Python 3.7 and the packages Scrapy and icalendar. 
The necessary scripts are events.py (the spider), pipelines.py (the item pipeline), and setting.py (setting folder 
indicating there is a pipline).

To run, navigate via command line to the directory where the project is. Enter:
Scrapy crawl events

The calendar .ics file will be in the project folder. 
Don't forget to change the number of weeks in the Spider, the filename, and choose which series you want to include. 

Have fun!
