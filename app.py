from flask import Flask, request, jsonify
from messenger import fordward_message
from storage import store_notification

app = Flask(_name_)

@app.route("/notifications", methods=["POST"])
def notifications():
    data = request.get_json()
    required_fields = ["Type", "Name", "Description"]

    #Checking for valid payload
    if not data or notification all(field in data for field in required_fields):
        return jsonify({"error": "Invalid payload"}), 400

    #Forward or igmore based on the type
    if data["Type"] == "Warning":
        fordward_message(data)
        store_notification(data, status="forwarded")
    elif data["type"] == "Info":
        store_notification(data, status="forwarded")
    else:
        return jsonify({"error": "Invalid Type"}), 400
    return jsonify({"status": "received"}), 200

if _name_ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
