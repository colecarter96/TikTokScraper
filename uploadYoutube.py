#!/usr/bin/python
import os
import google.auth
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http
import json

# Set the OAuth 2.0 scope for managing YouTube videos
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
CLIENT_SECRETS_FILE = 'client_secrets.json'

# Connect to youtube and authenticate to use this project

def get_authenticated_service():
    """Authenticate and build the YouTube service."""
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    return googleapiclient.discovery.build('youtube', 'v3', credentials=credentials)


# Upload the video to youtube to the configured account

def upload_video(youtube, file_path, title, description, tags, category_id, privacy_status, publish_at=None):
    """Upload a video to YouTube."""
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy_status,
            "embeddable": True,
            "publicStatsViewable": True,
            "madeForKids": False  # True or False
        }
    }

    if publish_at:
        body["status"]["publishAt"] = publish_at
        body["status"]["privacyStatus"] = "private"  # Video must be private until publishAt
    
    # Create the request to upload the video
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=googleapiclient.http.MediaFileUpload(file_path, resumable=True)
    )
    
    # Execute the request
    response = request.execute()
    
    print(f"Video uploaded successfully. Video ID: {response['id']}")


