from __future__ import print_function
from django.http import HttpResponse
from rest_framework import response
from rest_framework.views import APIView

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from google.oauth2.credentials import Credentials
from oauth2client.client import AccessTokenCredentials
import json

def home(req):
    return HttpResponse('Home Check!')

def calendar(endpoint,code=None):
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    flow = Flow.from_client_secrets_file('credentials_web.json',scopes=SCOPES)
    flow.redirect_uri='http://localhost:8000/rest/v1/calendar/redirect'
    authorization_url,state = flow.authorization_url(access_type='offline',include_granted_scopes='true')
    if(endpoint=='init'):
        return authorization_url
    elif(endpoint=='redirect'):
        flow.fetch_token(code=code)
        return flow.credentials.to_json()

class GoogleCalendarInitView(APIView):
    def get(self,req):
        authorization_url=calendar(endpoint='init')
        return response.Response(authorization_url)
        
class GoogleCalendarRedirectView(APIView):
    def get(self,req):
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        access_token=req.query_params.dict()
        access_token=access_token['code']
        creds=calendar('redirect',access_token)
        creds=json.loads(creds)
        credentials = AccessTokenCredentials(creds['token'], 'USER_AGENT')
        service = build('calendar', 'v3', credentials=credentials)
        google_calendar_events = service.events().list(calendarId='primary', singleEvents=True,
                                          orderBy='startTime').execute()
        google_calendar_events = google_calendar_events.get('items', [])

        return response.Response(google_calendar_events)
        
