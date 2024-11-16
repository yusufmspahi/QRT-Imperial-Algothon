import re
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Slack Bot Token
slack_token = "xoxb-8020284472341-8039987322498-YEEIK18xtnAGj8JDyHTTzoff"
client = WebClient(token=slack_token)

# The ID of the Slack channel where passcodes are posted
channel_id = "C080P6M4DKL"

# Joe Arrowsmiths ID as someone is sending fake codes
trusted_user_id = "U080GCRATP1"

# Regex to extract filename and passcode
message_pattern = re.compile(r"Data has just been released '([^']+)' the passcode is '([^']+)'", re.IGNORECASE)


def get_latest_file_and_passcode(channel_id):
    try:
        # Fetch latest messages
        response = client.conversations_history(channel=channel_id, limit=10)
        messages = response.get("messages", [])

        for message in messages:
            # Filter messages by Joe Arrowsmith
            if message.get("user") == trusted_user_id:
                text = message.get("text", "")
                match = message_pattern.search(text)
                if match:
                    filename, passcode = match.groups()
                    return filename, passcode

        return None, None  # No valid file or passcode found
    except SlackApiError as e:
        print(f"Error fetching messages: {e.response['error']}")
        return None, None


def get_all_file_passcodes(channel_id):

    try:
        # Fetch the latest messages from Slack
        response = client.conversations_history(channel=channel_id, limit=100)
        messages = response.get("messages", [])
        file_passcode_pairs = []

        for message in messages:
            # Check if the message is from the trusted user
            if message.get("user") == trusted_user_id:
                text = message.get("text", "")
                match = message_pattern.search(text)
                if match:
                    filename, passcode = match.groups()
                    file_passcode_pairs.append((filename, passcode))

        return file_passcode_pairs
    except SlackApiError as e:
        print(f"Error fetching messages: {e.response['error']}")
        return []
