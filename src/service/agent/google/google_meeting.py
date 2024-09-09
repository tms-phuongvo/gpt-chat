import datetime
import os.path
import logging
from langchain_core.tools import tool
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


class GoogleMeeting:

    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    def __init__(self):
        self.__get_credentials()

    def __get_credentials(self):
        self.cred = None
        if os.path.exists("token.json"):
            self.cred = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        if not self.cred or not self.cred.valid:
            if self.cred and self.cred.expired and self.cred.refresh_token:
                self.cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "src/service/agent/google/credentials.json", self.SCOPES
                )
                self.cred = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(self.cred.to_json())

    def create_event(
        self, summary, location, description, start_time, end_time, attendees
    ):
        service = build("calendar", "v3", credentials=self.cred)

        event = {
            "summary": summary,
            "location": location,
            "description": description,
            "start": {
                "dateTime": start_time.isoformat(),
                "timeZone": "Asia/Ho_Chi_Minh",
            },
            "end": {
                "dateTime": end_time.isoformat(),
                "timeZone": "Asia/Ho_Chi_Minh",
            },
            "attendees": [{"email": attendee} for attendee in attendees],
            "conferenceData": {
                "createRequest": {
                    "requestId": f"{summary}-{start_time.isoformat()}",
                    "conferenceSolutionKey": {"type": "hangoutsMeet"},
                }
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 24 * 60},
                    {"method": "popup", "minutes": 10},
                ],
            },
        }

        event = (
            service.events()
            .insert(calendarId="primary", body=event, conferenceDataVersion=1)
            .execute()
        )
        logging.info(f"Event created: {event.get('htmlLink')}")
        logging.info(
            f"Google Meet link: {event['conferenceData']['entryPoints'][0]['uri']}"
        )
        return event["conferenceData"]["entryPoints"][0]["uri"]

    def booking_meeting(
        self, summary: str, email: str | list[str], date: str, time: str
    ) -> str:

        summary = summary
        location = "Google Meet"
        description = ""

        start_time = datetime.datetime.strptime(f"{date} {time}", "%d/%m/%Y %H:%M")
        end_time = start_time + datetime.timedelta(minutes=30)
        attendees = email if isinstance(email, list) else [email]
        meet_link = self.create_event(
            summary, location, description, start_time, end_time, attendees
        )

        return meet_link


@tool
def booking_meeting_tool(summary: str, email: list[str], date: str, time: str) -> str:
    """
    Collect enough of that information if the user requests a meeting.
    Ask one question at a time to collect enough information.
    Make sure to validate the information before asking the next question.

    Args:
        summary: Meeting summary
        email: List email of attendees
        date: Date of the meeting with format dd/mm/yyyy
        time: Dime of the meeting with format hh:mm
    """
    return f"Booking meeting with google for {summary} based on {date} and {time}"
