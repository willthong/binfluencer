# Goes to Cambridge City Council's website (cambridge.gov.uk) and returns the
# next bin date for blue, green and black bins

# Setup: go to https://www.cambridge.gov.uk/check-when-your-bin-will-be-emptied and
# retrieve the ID
BASE_URL = "https://servicelayer3c.azure-api.net/wastecalendar/calendar/ical/"
ID = "200004199980"
import urllib.request
import datetime
import sys
import argparse

# Download file
url = BASE_URL + ID
# TODO: ICS location customisation
# urllib.request.urlretrieve(url, "/config/scripts/bins.ics")
urllib.request.urlretrieve(url, "./bins.ics")

events = []


def create_event(event_date, event_name):
    event = {"date": event_date, "name": event_name}
    events.append(event)


def get_colour(event_name):
    return event_name.split()[0].lower()


def find_next(colour, events):
    for event in events:
        event_colour = get_colour(event["name"])
        if event_colour == colour:
            return event["date"]


looking_for_event = False
event_date = ""
event_name = ""

with open("./bins.ics", mode="r", encoding="utf-8") as file:
    line_index = 0
    for line in file:
        if line.startswith("BEGIN:VEVENT"):
            looking_for_event = True
        if line.startswith("END:VEVENT"):
            looking_for_event = False
            create_event(event_date, event_name)
        if looking_for_event and line.startswith("DTSTART;VALUE=DATE:"):
            event_date = int((line.split(":")[1]).strip())
        if looking_for_event and line.startswith("SUMMARY:"):
            event_name = (line.split(":")[1]).strip()
        line_index += 1

# Remove dates in the past
events_future = []
today = datetime.date.today()
today = int(today.strftime("%Y%m%d"))
for event in events:
    if event["date"] >= today:
        events_future.append(event)

# Sort list of events by date
dates = []
last_date = 0
for event in events_future:
    dates.append(event)
    if event["date"] > last_date:
        dates.remove(event)
        dates.append(event)
    last_date = event["date"]
next_bin_date = dates[0]["date"]
next_bin_date_str = str(dates[0]["date"])
next_bin_date_str = (
    next_bin_date_str[0:4] + "-" + next_bin_date_str[4:6] + "-" + next_bin_date_str[6:8]
)


next_black = find_next("black", events_future)
next_blue = find_next("blue", events_future)
next_green = find_next("green", events_future)

next_bin_colours = []
for event in events_future:
    if event["date"] == next_bin_date:
        next_bin_colours.append(get_colour(event["name"]))
if "blue" in next_bin_colours and "green" in next_bin_colours:
    nbc_output = "Blue and Green"
else:
    nbc_output = next_bin_colours[0].title()

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--date", help="Show next bin collection date")
parser.add_argument("-c", "--colour", help="Show next bin collection colour")
args = parser.parse_args()
if args.date:
    sys.stdout.write(f"{next_bin_date_str}")
if args.colour:
    sys.stdout.write(f"{nbc_output}")
