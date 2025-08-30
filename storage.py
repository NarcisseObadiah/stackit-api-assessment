notifications = []

#Store notifications in memory with status: "forwarded" or ignored
def store_notification(notification, status):
    notifications.append({
        "Type": notification["Type"],
        "Name": notification["Name"],
        "Description": notification["Description"],
        "status": status
    })

