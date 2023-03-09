import requests
import json
from datetime import datetime, timedelta
from pytz import timezone
from icalendar import Calendar, Event
import time

# TODO keep system memory active? somehow?

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
                "automaticallyCopy": True,
                "copy": message
            })
        )
        print('Notification sent! Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
    except requests.exceptions.RequestException:
        print('Notification failed to send')

def main():
    config = load_config()
    # Fetch today's events from the internet calendar
    response = requests.get(config["calendar_url"])
    cal = Calendar.from_ical(response.text)
    tz = timezone(config["timezone"])
    today = datetime.now(tz).date()

    print(f"Current time in {tz.zone}: {datetime.now()}")

    for component in cal.walk():
        if component.name == "VEVENT":
            event = Event.from_ical(component.to_ical())
            start_utc = event["DTSTART"].dt
            end_utc = event["DTEND"].dt
            start = start_utc.astimezone(tz)
            end = end_utc.astimezone(tz)

            if start.date() == today:
                print(f"Event: {event['SUMMARY']}")
                #print(f"Start time (UTC): {start_utc}")
                print(f"Start time ({tz.zone}): {start}")
                #print(f"End time (UTC): {end_utc}")
                print(f"End time ({tz.zone}): {end}")

                # Notify 5 mins before the event
                notify_time = start - timedelta(minutes=5)
                if notify_time > datetime.now(tz):
                    notify_title = f"PUNCH IN" #{event['SUMMARY']}"
                    notify_message = f"Don't forget to punch in for {event['SUMMARY']} at {start.strftime('%I:%M %p')}"
                    wait_time = (notify_time - datetime.now(tz)).total_seconds()
                    time.sleep(wait_time)
                    send_notification(notify_title, notify_message)
                    print(f"Notification sent for start time: {notify_time}")

                # Notify 5 mins before the end of the event
                notify_time = end - timedelta(minutes=5)
                if notify_time > datetime.now(tz):
                    notify_title = f"PUNCH OUT" #{event['SUMMARY']}"
                    notify_message = f"{event['SUMMARY']} ends at {end.strftime('%I:%M %p')}"
                    wait_time = (notify_time - datetime.now(tz)).total_seconds()
                    time.sleep(wait_time)
                    send_notification(notify_title, notify_message)
                    print(f"Notification sent for end time: {notify_time}")

if __name__ == "__main__":
    main()