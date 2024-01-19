import argparse
import datetime as dt
import ics
import json
import logging
import os
import requests
import sys
import validators
import zoneinfo

script_dir = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(
    level=logging.WARNING,
    filename=script_dir + "/binfluencer.log",
    filemode="w",
    format=f"%(asctime)s - %(levelname)s - %(message)s",
)
logging.getLogger().addHandler(logging.StreamHandler())


class BinCollection:
    def __init__(self, colour: str, date: dt.datetime = None) -> None:
        self.colour = colour
        self.date = date


def new_config_url() -> str:
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
            config["url"] = user_input
            config_json = json.dumps(config, indent=4)
            with open(script_dir + "/config.json", "w") as config_file:
                config_file.write(config_json)
            logging.debug(f"Saved new URL {config['url']} to config.json")
            return


def parse_ics(
    ics_file: str, next_collections: list[BinCollection]
) -> list[BinCollection]:
    """Downloads ICS file and adds each bin colour's latest date to the next_collections list"""
    with open(ics_file, mode="r") as file:
        cal = ics.Calendar(file.read())
        now = dt.datetime.now().replace(tzinfo=zoneinfo.ZoneInfo("Europe/London"))

        for event in cal.events:
            if event.begin.datetime <= now:
                continue
            for bin_collection in next_collections:
                if not bin_collection.colour in event.name.lower():
                    continue
                logging.debug(
                    f"Found {bin_collection.colour} bin collection on {event.begin.datetime.strftime('%Y-%m-%d')}"
                )
                if not bin_collection.date:
                    bin_collection.date = event.begin.datetime
                elif bin_collection.date:
                    bin_collection.date = min(bin_collection.date, event.begin.datetime)
                break
        logging.debug(
            "Found next bin collection dates: "
            f"{[[bin_collection.date.strftime('%Y-%m-%d'), bin_collection.colour] for bin_collection in next_collections]}"
        )
        return next_collections


def consolidate_bins(next_collections: list[BinCollection]) -> list[BinCollection]:
    """Combines any BinCollections on the same date"""
    next_collections.sort(key=lambda x: x.date)
    new_next_collections = [next_collections[-1]]
    i = 0
    while i < len(next_collections) - 1:
        bin_collection = next_collections[i]
        next_bin_collection = next_collections[i + 1]
        if bin_collection.date == next_bin_collection.date:
            new_next_collections.append(
                BinCollection(
                    bin_collection.colour.capitalize()
                    + " and "
                    + next_bin_collection.colour.capitalize(),
                    bin_collection.date,
                )
            )
            logging.debug(
                f"Consolidated {bin_collection.colour} and {next_bin_collection.colour}"
            )
            i += 2
        else:
            bin_collection.colour = bin_collection.colour.capitalize()
            new_next_collections.append(bin_collection)
            i += 1
    return new_next_collections


def next_bin(next_collections: list[BinCollection]) -> str:
    for bin_collection in next_collections:
        if dt.datetime.now().date() == bin_collection.date.date():
            return f"Today ({bin_collection.colour})"
        elif (
            dt.datetime.now().date() + dt.timedelta(days=1)
            >= bin_collection.date.date()
        ):
            return f"Tomrorrow ({bin_collection.colour})"
        elif (
            dt.datetime.now().date() + dt.timedelta(days=7)
            >= bin_collection.date.date()
        ):
            return f"{bin_collection.date.strftime('%A')} ({bin_collection.colour})"


def next_bin_verbose(next_collections: dict) -> str:
    next_collections.sort(key=lambda x: x.date)
    verbose_string = ""
    for bin_collection in next_collections:
        if "and" in bin_collection.colour:
            plural = "s"
        else:
            plural = ""
        verbose_string += f"\nNext {bin_collection.colour.lower()} bin{plural}: {bin_collection.date.strftime('%d %B %Y')}"
    return verbose_string


def next_bin_json(next_collections: dict) -> str:
    next_collection = None
    for collection in next_collections:
        if not next_collection or collection.date < next_collection.date:
            next_collection = collection
    if dt.datetime.now().date() == next_collection.date.date():
        natural_day = "Today"
    elif dt.datetime.now().date() + dt.timedelta(days=1) >= next_collection.date.date():
        natural_day = "Tomorrow"
    elif dt.datetime.now().date() + dt.timedelta(days=7) >= next_collection.date.date():
        natural_day = next_collection.date.strftime("%A")
    else:
        natural_day = next_collection.date.strftime("%e %B")
    output = {
        "natural_day": natural_day,
        "colour": next_collection.colour,
        "date": next_collection.date.strftime("%Y-%m-%d"),
    }
    return json.dumps(output)


try:
    config = json.loads(open(script_dir + "/config.json", "r").read())
except FileNotFoundError:
    logging.info(
        f"No config file found. Initialising blank config file in {script_dir}."
    )
    config = {}

# TODO: CLI interface for customising config

if "url" not in config:
    new_config_url()
    # TODO: delete any existing ICS files
else:
    logging.debug(f"Loaded URL {config['url']} from config.json")

# TODO: Customise config["ics_location"]
ics_directory = config["ics_location"] if "ics_location" in config else script_dir
ics_file = ics_directory + "/bin_dates.ics"

refresh_rate = config["refresh_rate"] if "refresh_rate" in config else 90

since_refresh = None
if os.path.exists(ics_file):
    ics_mod = dt.datetime.fromtimestamp(os.path.getmtime(ics_file))
    since_refresh = (dt.datetime.now() - ics_mod).days
    logging.info(f"{since_refresh} days since bin collection dates were last updated.")
if since_refresh is None or since_refresh >= refresh_rate:
    logging.info(f"Downloading bin collection file...")
    r = requests.get(config["url"])
    with open(ics_file, "wb") as file:
        for chunk in r.iter_content(chunk_size=128):
            file.write(chunk)
else:
    logging.info(f"Skipping file refresh.")

if "colours" not in config:
    next_collections = [
        BinCollection("black"),
        BinCollection("blue"),
        BinCollection("green"),
    ]
else:
    next_collections = [BinCollection(colour.lower()) for colour in config["colours"]]

next_collections = parse_ics(ics_file, next_collections)
next_collections = consolidate_bins(next_collections)

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", action=argparse.BooleanOptionalAction)
parser.add_argument("--json", action=argparse.BooleanOptionalAction)
args = parser.parse_args()
if args.verbose:
    sys.stdout.write(next_bin_verbose(next_collections))
elif args.json:
    sys.stdout.write(next_bin_json(next_collections))
else:
    sys.stdout.write(next_bin(next_collections))

# TODO: add tests
