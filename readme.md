# Punch In / Out Notifications

I forget to punch in and out during the grace period so I made this script that pushes "reminder" notifications 5 minutes before the start and end of an event from a chosen internet calendar.

So why not change events directly in the calendar?

The way my work calendar works does not allow me to mass overwrite notification reminders for events! It also does an amazing thing and overwrites events when it syncs so this is the next best thing.

## Setting up

- Install `requrements.txt`

Create a `config.json` file with the following keys:

- `calendar_url`: The URL of your public internet calendar.
- `timezone`: The timezone of your calendar. EG. [Europe/London](https://timezonedb.com/time-zones)
- `bark_api_key`: API key from [bark.day.app.](https://github.com/Finb/Bark/blob/master/README.en.md)

## Running

Note: Running the script once a day should be plenty unless you know the events update more often. Your device must also have an active internet connection to recieve the notifcations.

- Run `punch.py`.

The script closes itself once all the notifications for the event have been sent.
