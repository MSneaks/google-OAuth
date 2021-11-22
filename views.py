from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import json
import io



#Aquire credentials
def google_auth():
    credentials = None
    if os.path.exists('token.pickle'):
        print('Loading Credentials From File...')
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('Refreshing Access Token...')
            credentials.refresh(Request())
        else:
            print('Fetching New Tokens...')
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json',
                scopes=["https://www.googleapis.com/auth/drive"]
            )
            flow.run_local_server(port=8080, prompt='consent',
                                authorization_prompt_message='')
            credentials = flow.credentials
            with open('token.pickle', 'wb') as f:
                print('Saving Credentials for Future Use...')
                pickle.dump(credentials, f)
    return (credentials)


#Make request to Google Drive API. Title and data should be provided
def makeDriveRequest(credentials,token,title,data):
    drive = build("drive","v3",credentials=credentials)
    token = token
    name = title
    parent_id = 'root'
    contents = data
    para = {
        "name": name,
        "parents": [parent_id],
        "mimeType": "application/vnd.google-apps.document"
        }
    res = requests.post(
    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
    headers={"Authorization": "Bearer " + token},
    files={
        'metadata': ('metadata', json.dumps(para), 'application/json'),
        'file': ('file', io.BytesIO(contents.encode('utf-8')), 'text/plain')
    }
)
