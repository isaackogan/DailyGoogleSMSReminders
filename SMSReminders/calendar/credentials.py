import os.path
from typing import List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from pydantic import BaseModel, PrivateAttr

SCOPES: List[str] = ['https://www.googleapis.com/auth/calendar.readonly']


class CredentialsProvider(BaseModel):
    """
    High level class to retrieve valid Google API credentials for the API.

    """

    # File path to the application credentials
    app_credentials_fp: str

    # File path to the user credentials
    user_credentials_fp: str

    _credentials: Optional[Credentials] = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Load user credentials if saved
        self._credentials = (
            Credentials.from_authorized_user_file(self.user_credentials_fp, SCOPES)
            if os.path.exists(self.user_credentials_fp)
            else None
        )

    @property
    def credentials(self) -> Credentials:

        # If credentials are not loaded, authenticate the user fresh
        if not self._credentials:
            self._credentials = self._authenticate_user_new()
            self._save_credentials()

        # If credentials are loaded but expired, refresh them
        if (not self._credentials.valid or self._credentials.expired) and self._credentials.refresh_token:
            self._credentials.refresh(Request())
            self._save_credentials()

        # Return the credentials
        return self._credentials

    def _authenticate_user_new(self) -> Credentials:
        flow = InstalledAppFlow.from_client_secrets_file(self.app_credentials_fp, SCOPES)
        return flow.run_local_server(port=0)

    def _save_credentials(self):
        with open(self.user_credentials_fp, 'w') as token:
            token.write(self._credentials.to_json())
