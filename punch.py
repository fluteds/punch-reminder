import requests
import json
from datetime import datetime, timedelta
from pytz import timezone
from icalendar import Calendar, Event
import time
import sys

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
                "automaticallyCopy": True,
                "copy": message
            })
        )
        print(log_prefix + 'Notification sent! Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
    except requests.exceptions.RequestException:
        print(log_prefix + ' Notification failed to send')

def main():
    config = load_config()
    # Fetch today's events from the internet calendar
    response = requests.get(config["calendar_url"])
    cal = Calendar.from_ical(response.text)
    tz = timezone(config["timezone"])
    today = datetime.now(tz).date()
    
    print(log_prefix + " Pulling events from calendar.")

    #print(f"Current time in {tz.zone}: {datetime.now()}")

    for component in cal.walk():
        if component.name == "VEVENT":
            event = Event.from_ical(component.to_ical())
            start_utc = event["DTSTART"].dt
            end_utc = event["DTEND"].dt
            start_time = start_utc.astimezone(tz)
            end_time = end_utc.astimezone(tz)

            if start_time.date() == today:
                print()
                print("EVENTS FOR TODAY")
                print()
                print(f"{event['SUMMARY']} - Start Time: {start_time} - End Time: {end_time}")
                print()
                
            if not start_time.date() == today:
                print(log_prefix + " There is not an event scheduled for today.")                
                
                # Notify 5 mins before the event
                notify_time = start_time - timedelta(minutes=5)
                if notify_time > datetime.now(tz):
                    notify_title = f"PUNCH IN" #{event['SUMMARY']}"
                    notify_message = f"Don't forget to punch in for {event['SUMMARY']} at {start_time.strftime('%I:%M %p')}"
                    wait_time = (notify_time - datetime.now(tz)).total_seconds()
                    time.sleep(wait_time)
                    send_notification(notify_title, notify_message)
                    print(log_prefix + " Notification sent for start_time time: {notify_time}")

                # Notify 5 mins before the end_time of the event
                notify_time = end_time - timedelta(minutes=5)
                if notify_time > datetime.now(tz):
                    notify_title = f"PUNCH OUT" #{event['SUMMARY']}"
                    notify_message = f"{event['SUMMARY']} ends at {end_time.strftime('%I:%M %p')}"
                    wait_time = (notify_time - datetime.now(tz)).total_seconds()
                    time.sleep(wait_time)
                    send_notification(notify_title, notify_message)
                    print(log_prefix + " Notification sent for end_time time: {notify_time}")

if __name__ == "__main__":
    main()