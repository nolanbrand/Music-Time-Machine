from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import pprint

BILLBOARD_URL = "https://www.billboard.com/charts/hot-100/"

SPOTIFY_CLIENT_ID = "Your Client ID"
SPOTIFY_CLIENT_SECRET = "Your Client Secret"
REDIRECT_URI = "http://example.com"
SCOPE = "playlist-modify-private"


#Billboard Top 100 List Creation based on user input date
user_input = input("Which year do you want to travel to? Type date in this format YYYY-MM-DD: ")

user_date_url = BILLBOARD_URL + user_input + "/"

billboard_response = requests.get(url=user_date_url)

soup = BeautifulSoup(billboard_response.text, "html.parser")

top_100_songs = soup.select("li ul li h3")

top_100_artists = soup.select("li ul li span")

top_100_song_list = [song.getText().strip() for song in top_100_songs]

temp_list = [artist.getText().strip() for artist in top_100_artists]

top_100_artist_list = [temp_list[i] for i in range(0, len(temp_list), 7)]


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    username="1253105011",
    cache_path="token.txt"
)
)

user_id = sp.current_user()["id"]

song_uri_list = []
for name, artist in zip(top_100_song_list, top_100_artist_list):
    result = sp.search(q=f"track:{name} artist:{artist}")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uri_list.append(uri)
    except IndexError:
        print(f"{name} - {artist} does not exist in Spotify Library")
        result = sp.search(q=f"track:{name}")

playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{user_input} Billboard Top 100",
    public=False,
)

#print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uri_list)

