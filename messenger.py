import os
import requests
from dotenv import load_dotenv

#load environnnment variavles from .env

load_dotenv()

SLACK_WEBHOOK_URL = os_environ.get("SLACK_WEBHOOK_URL")
forwarded_notifications = []

def fordward_message(notification)
    if not SLACK_WEBHOOK_URL:
        print("No webhook provided. Skipping forwarding.")
        return
    message = {
        "text": f" Warning: {notification['Name']}\n{notification['Description']}"
    }
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=message)
        response.raise_for_status()
        print("Forwarded to Slack:", notification["Name"])
        forwarded_notifications.append(notification)
    except requests.exceptions.RequestException as e:
        print("Failed to send to Slack:", e)