import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
slack_webhook = os.getenv("SLACK_WEBHOOK_URL")

# In-memory storage for all incoming notifications, this reset each time the service restart(Non-Persistent)
notifications = []

# Endpoint to receive notifications.

@app.route("/notify", methods=["POST"])
def notify():
    data = request.get_json()

    # Basic validation to make sure payload has required fields
    if not data or "Type" not in data or "Name" not in data or "Description" not in data:
        return jsonify({"error": "Invalid payload"}), 400

    # Store the notification in memory
    notifications.append(data)

    if data["Type"] == "Warning":
        # Forward warninngs to Slack for alerting
        if slack_webhook:
            requests.post(slack_webhook, json={
                "text": f" WARNING: {data['Name']} - {data['Description']}"
            })
        return jsonify({"status": "forwarded to Slack"}), 200

    elif data["Type"] == "Info":
        # info messages are just logged internally
        return jsonify({"status": "stored but not forwarded (Info)"}), 200
    else:
        # Handle unexpected notification types
        return jsonify({"status": f"stored but type '{data['Type']}' not handled"}), 200


#endpoint to retrieve all notifications stored in memory
@app.route("/notifications", methods=["GET"])
def get_notifications():
    return jsonify(notifications), 200

if __name__ == "__main__":
    # run on all interfaces so it works inside Docker
    app.run(host="0.0.0.0", port=5000)
