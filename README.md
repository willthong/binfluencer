# Binfluencer 🗑🚮

A Python application to fetch the bin collections from your UK local council's website.
It will then let you know if you have to put a bin out today. OF course, you could
manually download the council-provided ICS file and add it to your calendar, but then
you need to add notifications for the day before, or remember to check your calendar,
and (worst of all), you need to go through this task every time the council adds new bin
dates. For my council, that's every three months, and I forget.

With Binfluencer, you will never forget the bins again! If you have [Home
Assistant](https://home-assistant.io), Binfluencer can be run on your server as a script
so you can (for instance) have a smart speaker nag you from the second you get home on
bin night until you finally put that bin out.

#TODO: blogpost

# Compatibility

The app only works if your council provides ICS access to your bin calendar. Some do,
others don't. I am pretty sure those that do use the same provider due to UI similarities
though. Here's an incomplete list of councils I've manually checked for compatibility:

❌ Adur & Worthing Councils
✅ Cambridge City Council
✅ South Cambridgeshire District Council

## Installation ⚙️

PyPi, presumably?

## Getting started ▶️

#TODO: instructions for fetching your ID from your council website
#TODO: Home Assistant configuration instructions

## Roadmap 🗺️

* [ ] Weekly fetch 
* [ ] Configuration feature
* [ ] Mobile version with notifications

## Contributing 💻

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License 📄

[MIT](https://choosealicense.com/licenses/mit/)
