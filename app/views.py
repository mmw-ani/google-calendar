from django.http import HttpResponse,JsonResponse,HttpResponseRedirect

import datetime
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Constants
REDIRECT_URL = 'http://127.0.0.1:8000/rest/v1/calendar/redirect'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CREDENTIALS = 'credentials.json'

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


def index(request):
	return HttpResponse("Hey!")

# initial page
def GoogleCalendarInitView(request):

	flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS,SCOPES)
	flow.redirect_uri = REDIRECT_URL
	authorization_url,state=flow.authorization_url(access_type='offline',include_granted_scopes='true')
	request.session['state']= state
	return HttpResponseRedirect(authorization_url)



def GoogleCalendarRedirectView(request):
    
    state = request.session['state']
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES,state=state)
    flow.redirect_uri = REDIRECT_URL

    authorization_response = request.get_full_path()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)
    service = build('calendar', 'v3', credentials=credentials)
    
    # Events from current time.
    now = datetime.datetime.utcnow().isoformat() + 'Z' 
    events_result = service.events().list(calendarId='primary', timeMin=now,
								singleEvents=True,maxResults=10,orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        return JsonResponse({"message":'No upcoming events found.'})
    calendar=[]
    
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        calendar.append({'summary':event['summary'],start:start,end:end})
    
    return JsonResponse({"calendar":calendar,})
 
def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}