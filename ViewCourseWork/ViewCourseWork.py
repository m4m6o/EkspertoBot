from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import glob, os


users = 0
os.chdir("/")
for file in glob.glob("*.pickle"):
    user += 1

SCOPES = ['https://www.googleapis.com/auth/classroom.coursework.students.readonly']

def ViewCourseWork(chat_id, course_id):
    
    course_id = ''
    creds            = None
    pickleToken_path = "AddCourse/" + str(chat_id) + "_token.pickle"
    credentials_path = "AddCourse/credentials.json"

    if os.path.exists(pickleToken_path):
        with open(pickleToken_path, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow  = Flow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=users)
        
        with open(pickleToken_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds)
    
    students_list = service.courses().courseWork().list(courseId = course_id).execute()
    return students_list
