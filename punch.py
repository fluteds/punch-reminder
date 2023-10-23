# TODO
# Refresh events periodically incase of changes

import requests
import json
from datetime import datetime, timedelta
from pytz import timezone
from icalendar import Calendar, Event
import time

log_prefix = "[" + datetime.now().strftime("%I:%M %p") + "]"

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def send_notification(title, message):
    """Sends a notification using bark.day.app"""
    config = load_config()
    try:
        response = requests.post(
            url=f"https://api.day.app/{config['bark_api_key']}",
            headers={
                "Content-Type": "application/json; charset=utf-8",
            },
            data=json.dumps({
                "title": title,
                "body": message,
                "sound": "alarm",
                "url": "shortcuts://run-shortcut?name=Dayforce",
                "level": "timeSensitive",
                "group": "Punch Reminders",
                "automaticallyCopy": "1"
            })
        )
        print(log_prefix + f'Notification sent! Response HTTP Status Code: {response.status_code}')
    except requests.exceptions.RequestException:
        print(log_prefix + f'Notification failed to send. Response HTTP Status Code: {response.status_code}')

def main():
    config = load_config()
    response = requests.get(config["calendar_url"])
    cal = Calendar.from_ical(response.text)
    tz = timezone(config["timezone"])  # Use the timezone from the config
    today = datetime.now(tz).date()
    events_today = False  # Flag to check if there are any events for today to stop multiple logs

    for component in cal.walk():
        if component.name == "VEVENT":
            event = Event.from_ical(component.to_ical())
            start_utc = event["DTSTART"].dt
            end_utc = event["DTEND"].dt
            start = start_utc.astimezone(tz)
            end = end_utc.astimezone(tz)

            if start.date() == today:
                events_today = True  # There is an event for today
                print()
                print("EVENTS FOR TODAY")
                print()
                print(f"{event['SUMMARY']} - Start: {start.strftime('%H:%M')} - End: {end.strftime('%H:%M')}")
                print()

                # Notify 5 mins before the event
                notify_time = start - timedelta(minutes=5)
                if notify_time > datetime.now(tz):
                    notify_title = f"PUNCH IN" #{event['SUMMARY']}"
                    notify_message = f"Don't forget to punch in for {event['SUMMARY']} at {start.strftime('%H:%M')}"
                    wait_time = (notify_time - datetime.now(tz)).total_seconds()
                    time.sleep(wait_time)
                    send_notification(notify_title, notify_message)
                    print(f"Notification sent for start time: {notify_time}")

                # Notify 5 mins before the end of the event
                notify_time = end - timedelta(minutes=5)
                if notify_time > datetime.now(tz):
                    notify_title = f"PUNCH OUT" #{event['SUMMARY']}"
                    notify_message = f"{event['SUMMARY']} ends at {end.strftime('%H:%M')}"
                    wait_time = (notify_time - datetime.now(tz)).total_seconds()
                    time.sleep(wait_time)
                    send_notification(notify_title, notify_message)
                    print(f"Notification sent for end time: {notify_time}")
    if not events_today:
        print("No events for today.")  # Add a console log if there are no events

if __name__ == "__main__":
    main()
