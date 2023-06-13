import os
import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Initialize the Slack bot
slack_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(token=slack_token)

# Define the submission time frame
SUBMISSION_START_TIME = datetime.time(8, 0)  # 8:00 AM
SUBMISSION_END_TIME = datetime.time(20, 0)  # 8:00 PM

# Check if the current time is within the daily input submission time frame
def is_within_submission_timeframe():
    current_time = datetime.datetime.now().time()

    return SUBMISSION_START_TIME <= current_time <= SUBMISSION_END_TIME

# Retrieve the user's profile picture URL from Slack
def get_user_profile_picture(user_id):
    try:
        response = client.users_profile_get(user=user_id)
        assert response["ok"]

        profile = response["profile"]
        picture_url = profile["image_512"]  # Choose the desired image size

        return picture_url
    except SlackApiError as error:
        print("Error retrieving user profile:"
              f"{error.response['error']}")

def send_submission_closed_message(user_id):
    try:
        response = client.chat_postMessage(
            channel=user_id,
            text="Sorry, the input submission is closed for today."
             "Please submit your response tomorrow.",
        )
        assert response["ok"]
    except SlackApiError as error:
        print("Error sending submission closed message:"
               f"{error.response['error']}")

# Handle the user's message event
def handle_message(event):
    user_id = event["user"]
    user_answer = event["text"]

    # Check if it's still within the daily input submission time frame
    if is_within_submission_timeframe():
        # Process the user's answer
        picture_url = get_user_profile_picture(user_id)
        # send_request_to_backend(user_id, user_answer, picture_url)
    else:
        # Send a message informing the user that the input
        # submission is closed for the day
        send_submission_closed_message(user_id)


# Example endpoint in your backend to receive Slack events
def slack_event_endpoint(request):
    event = request.json  # Assuming the event payload is in JSON format

    if "event" in event:
        handle_message(event["event"])

    return "OK" # Return a response to acknowledge the event reception
