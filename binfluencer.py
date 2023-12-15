import argparse
import datetime as dt
import json
import logging
import os
from pathlib import Path
import requests
import sys
import validators

script_dir = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(
    level=logging.DEBUG,
    filename=script_dir + "/binfluencer.log",
    filemode="w",
    format=f"%(asctime)s - %(levelname)s - %(message)s",
)
logging.getLogger().addHandler(logging.StreamHandler())


def get_valid_url() -> str:
    """Accepts user input, strips and returns it if it's a valid URL"""
    url_prompt = (
        "Enter your property's bin calendar URL here. If you're not sure "
        "what that is, check the 'Getting started' section of README.md. "
        "Expect it to look something like "
        "'https://servicelayer3c.azure-api.net/wastecalendar/calendar/ical/1234567890123'\n"
    )
    while True:
        user_input = input(url_prompt).strip()
        if not validators.url(user_input):
            logging.error(f"{user_input} is an invalid URL. Please enter a valid URL.")
        else:
            return user_input


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


try:
    config = json.loads(open(script_dir + "/config.json", "r").read())
except FileNotFoundError:
    logging.info(
        f"No config file found. Initialising blank config file in {script_dir}."
    )
    config = {}

# TODO: CLI interface for customising config

if "url" not in config:
    config["url"] = get_valid_url()
    config_json = json.dumps(config, indent=4)
    with open(script_dir + "/config.json", "w") as config_file:
        config_file.write(config_json)
    logging.debug(f"Saved new URL {config['url']} to config.json")
    # TODO: delete any existing ICS files
else:
    logging.debug(f"Loaded URL {config['url']} from config.json")

# TODO: (config["ics_location"]) customisation
ics_file = config["ics_location"] if "ics_location" in config else script_dir
ics_file += "/bin_dates.ics"

refresh_rate = config["refresh_rate"] if "refresh_rate" in config else 90

ics_mod = dt.datetime.fromtimestamp(os.path.getmtime(ics_file))
since_refresh = (dt.datetime.now() - ics_mod).days
logging.info(f"{since_refresh} days since the bin collection dates were last updated.")
if since_refresh >= refresh_rate:
    logging.info(f"Refreshing...")
    r = requests.get(config["url"])
    with open(ics_file, "wb") as file:
        for chunk in r.iter_content(chunk_size=128):
            file.write(chunk)
else:
    logging.info(f"Skipping file refresh.")

events, event_date, event_name, looking_for_event = [], "", "", False

with open(ics_file, mode="r", encoding="utf-8") as file:
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
today = dt.date.today()
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
parser.add_argument(
    "--date",
    action=argparse.BooleanOptionalAction,
    help="Show next bin collection date",
)
parser.add_argument(
    "--colour",
    action=argparse.BooleanOptionalAction,
    help="Show next bin collection colour",
)
args = parser.parse_args()
if args.date:
    sys.stdout.write(f"{next_bin_date_str}")
if args.colour:
    sys.stdout.write(f"{nbc_output}")

# TODO: add tests
# TODO: weird edge case if it's today
