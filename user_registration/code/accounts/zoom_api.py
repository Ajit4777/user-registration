import jwt
import requests
import datetime
import json
from decouple import config as env

BASE_URL = env('BASE_URL')
ZOOM_API_KEY = env('ZOOM_API_KEY')
ZOOM_API_SECRET = env('ZOOM_API_SECRET')
# ZOOM_GROUP_ID = common.ZOOM_GROUP_ID


def create_jwt_token():
    payload = {'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=300),
               'iss': ZOOM_API_KEY
               }
    token = jwt.encode(payload, ZOOM_API_SECRET)
    if token:
        return token
    return None


def create_meeting_link(zoom_user_id):
    token = create_jwt_token()
    headers_api = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    zoom_id = zoom_user_id
    meeting_url = BASE_URL + f'users/{zoom_id}/meetings'
    session_name = "Test"
    data = {
        "topic": session_name,
        "type": 2,
        "start_time": str(datetime.datetime.utcnow()),
        "duration": "60",
        "password": "techpals"
    }
    response = requests.post(meeting_url, headers=headers_api, data=json.dumps(data))
    print(response.status_code)
    if response.status_code == 201:
        response = json.loads(response.content)
        ctx = {'start_url': response.get('start_url'),
               'join_url': response.get('join_url'),
               'passowrd': response.get('password'),
               'meeting_id': response.get('id')
               }
        return ctx
    return None


def delete_meeting_link(meeting_id):
    token = create_jwt_token()
    headers_api = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    delete_url = BASE_URL + 'meetings/' + str(meeting_id)
    res = requests.delete(delete_url, headers=headers_api)
    return res.status_code
