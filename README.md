# Binfluencer 🗑🚮📆

A Python application to fetch the bin collection dates from your UK local council's website.
It will then let you know if you have to put a bin out today. OF course, you could
manually download the council-provided ICS file and add it to your calendar, but then
you need to add notifications for the day before, or remember to check your calendar,
and (worst of all), you need to go through this task every time the council adds new bin
dates. For my council, that's every three months, and I forget.

With Binfluencer, you will never forget the bins again! Binfluencer can also be run on
your [Home Assistant](https://home-assistant.io) server as a script so you can (for
instance) have a smart speaker nag you from the second you get home on bin night until
you finally put that bin out.

TODO: blogpost

# Compatibility 🧩

The app only works if your council provides ICS access to your bin calendar. Some do,
others don't. I am pretty sure those that do use the same software contractor due to UI
similarities though. Here's an incomplete list of councils I've manually checked for
compatibility:

❌ Adur & Worthing Councils\\
❌ Barnet Council\\
✅ Cambridge City Council\\
❌ Islington Council\\
✅ South Cambridgeshire District Council\\

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

## Usage 🗑️

## Roadmap 🗺️

* [ ] Weekly fetch
* [ ] Configuration feature
* [ ] Mobile version with notifications

## Contributing 💻

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License 📜

[MIT](https://choosealicense.com/licenses/mit/)
