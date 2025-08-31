import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
slack_webhook = os.getenv("SLACK_WEBHOOK_URL")

# In memory storage for all the incoming notifications
notifications = []

@app.route("/notify", methods=["POST"])
def notify():
    data = request.get_json()

    if not data or "Type" not in data or "Name" not in data or "Description" not in data:
        return jsonify({"error": "Invalid payload"}), 400

    # store the notification in memory (both Warning and Info)
    notifications.append(data)

    if data["Type"]== "Warning":
        # forward to slack
        if slack_webhook:
            requests.post(slack_webhook, json={
                "text": f" WARNING: {data['Name']} - {data['Description']}"
            })
        return jsonify({"status": "forwarded to Slack"}), 200

    elif data["Type"] == "Info":
        # Do NOT forward, just acknowledge
        return jsonify({"status": "stored but not forwarded (Info)"}), 200

    else:
        # unknown type
        return jsonify({"status": f"stored but type '{data['Type']}' not handled"}), 200


@app.route("/notifications", methods=["GET"])
def get_notifications():
    return jsonify(notifications), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
