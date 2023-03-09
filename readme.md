# Punch In / Out Notifications

I always forget to punch in and out during the grace period so I made this script that pushes "reminder" notifications 5 minutes before the start and end of an event from a chosen internet calendar.

So why not change events directly in the calendar?

The way my work calendar works does not allow me to mass overwrite notification reminders for events! It also does an amazing thing and overwrites events when it syncs! So this is the next best thing.

## Setting up

Create a `config.json` file with the following keys:

- `calendar_url`: The URL of your internet calendar.
- `timezone`: The timezone of your calendar. EG. `Europe/London`
- `bark_api_key`: API key from [bark.day.app.](https://github.com/Finb/Bark/blob/master/README.en.md)

## Running

Run `punch-bark.py`

```json
{
    "calendar_url": "",
    "bark_api_key": "",
    "bark_url": "https://api.day.app", # Default API server
    "timezone": ""
}
```
