from datetime import datetime

def log_action(action):

    with open("activity.log", "a") as file:

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        file.write(
            f"{timestamp} - {action}\n"
        )
