# Binfluencer 🗑🚮📆

A Python application to fetch the bin collection dates from your UK local council's
website. It will then let you know if you have to put a bin out today.

Of course, you could subscribe to the calendar your council provides, but there are two
problems with this approach. First, if you use Google Calendar, sometimes that fails to
sync ([this might
help](https://www.ryadel.com/en/google-calendar-force-update-refresh-subscribed-calendar-ics/)
if you're experiencing this problem). And, second, most people put their bins out the
night before collection. Google Calendar does not allow us to create an event which is
always the day before another event, only events on a recurring basis (which breaks down
if there is a public holiday). So you can either remember to check our phone for events
the next day, or Binfluencer can remind you.

With Binfluencer, you will never forget the bins again! Binfluencer can be run on
your [Home Assistant](https://home-assistant.io) server as a script so you can (for
instance) have a smart speaker nag you from the second you get home on bin night until
you finally put that bin out.

TODO: blogpost

# Compatibility 🧩

The app only works if your council provides ICS access to your bin calendar. Some do,
others don't. I am pretty sure those that do use the same software contractor due to UI
similarities though. Here's an incomplete list of councils I've manually checked for
compatibility:

❌ Adur & Worthing Councils  
❌ Barnet Council  
✅ Cambridge City Council  
❌ Islington Council  
✅ South Cambridgeshire District Council  

## Installation ⚙️

PyPi, presumably?

## Getting started ▶️

TODO: instructions for fetching your URL from your council website
TODO: Home Assistant configuration instructions

These settings can be changed in config.json:

* `url`: Where on the internet should Binfluencer look for your property's bin calendar
  file? See above for how to find this variable.
* `ics_location`: Where on your system should Binfluencer look for a calendar file?
  *Default: the project directory*
* `refresh_rate`: How often (integer value of days from 1 to 365) should Binfluencer
  update your calendar? *Default: 90*
* `colours`: Which colour of bins do you want to track? *Default: ["black", "blue", "green"]*

## Usage 🗑️

```
# Returns which bins you have to put out next, and when: 'Tomorrow (Blue and Green)'
python binfluencer.py 

# Returns 'Next blue bin collection: 1 February 2024; Next green bin collection: 
# Blue and Green / Next black bin collection: 8 February 2024 (Black)'
python binfluencer.py --verbose

```

## Roadmap 🗺️

* [X] Configurable fetch rate
* [ ] Mobile version with notifications

## Contributing 💻

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License 📜

[MIT](https://choosealicense.com/licenses/mit/)
