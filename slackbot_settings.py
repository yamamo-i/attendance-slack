import os

API_TOKEN = os.getenv("SLACK_API_TOKEN")
ERRORS_TO = os.getenv("ERROR_TO")
PLUGINS = [
    "attendance_slack.plugins",
]
