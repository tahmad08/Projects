"""Project completed using The Come Up tutorial on Youtube
https://www.youtube.com/watch?v=7J_qcttfnJA&t=468s
and
Imdad Ahad tutorial on Youtube
https://www.youtube.com/watch?v=R3XgZ__jQxw 
December 6th, 2020
"""
import json
import requests
from secret import spotify_token, spotify_user_id
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl

class CreatePlaylist:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token
        self.youtube_client = self.get_youtube_client()
        self.all_song_info = {}

    #login to youtube
    def login_yt_client(self):
        """ Log Into Youtube, Copied from Youtube Data API """
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()

        # from the Youtube DATA API
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client

    #grab liked videos
    def liked_list(self):
        #using the youtubedl library, get the list of videos you liked
        #ytdl easily parses out song name and artist
        request = self.youtube_client.videos().list(
            part="snippet,contentDetails,statistics",
            myRating="like"
        )

        response = request.execute()

        #collect each video and get important information
        for item in response["items"]:
            video_title = item["snippet"]["title"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(
                item["id"])
            
        # use youtube_dl to collect the song name & artist name
        video = youtube_dl.YoutubeDL({}).extract_info(
            youtube_url, download=False)
        song_name = video["track"]
        artist = video["artist"]

        if song_name is not None and artist is not None:
                # save all important info and skip any missing song and artist
                self.all_song_info[video_title] = {
                    "youtube_url": youtube_url,
                    "song_name": song_name,
                    "artist": artist,

                    # add the uri, easy to get song to put into playlist
                    #so now we are calling the get_spotify_uri function to get the uri of song
                    "spotify_uri": self.get_spotify_uri(song_name, artist)

                }
    #create new spotify playlist
    def create_playlist(self):
        request_body = json.dumps({
            "name": "Youtube Liked Videos",
            "description": "All liked Youtube videos",
            "public": True
        })

        #send query for playlist using requests API
        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type" : "application/json",
                "Authorization" : "Bearer {}".format(spotify_token)
            }
        )
        #json response collected?!
        response_json = response.json()
        #playlist id
        return (response_json["id"])

    #search for song on spotify
    def get_spotify_uri(self, song_name, artist):
        
        #possible error in query format
        query = "https://api.spotify.com/v1/search?q={}%2C{}&type=track%2Cartist&limit=20&offset=0".format(
            song_name,
            artist
        )

        #sending request information to get song URI
        response = requests.get(
            query,
            headers={
                "Content-Type" : "application/json",
                "Authorization" : "Bearer {}".format(spotify_token)
            }
        )

        #collecting response as JSON I THINK??!!!
        response_json = response.json()
        songs = response_json["tracks"]["items"]

        #only use the first song in the returned JSON
        uri = songs[0]["uri"]

        #first song result
        return uri


    #add song into new playlist
    def add_song(self):
        #populate our songs dictionary

        # collect all of the URIs

        # create new spotify playlist

        #populate the new playlist


