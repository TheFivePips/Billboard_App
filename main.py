from bs4 import BeautifulSoup
import requests
from dotenv import dotenv_values
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# env variables
config = dotenv_values('.env')
ClientID = config["CLIENTID"]
ClientSecret = config["CLIENTSECRET"]

# Spotify auth using spotipy
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="playlist-modify-private",
    redirect_uri="http://localhost:8888/callback",
    client_id=ClientID,
    client_secret=ClientSecret,
    show_dialog=True,
    cache_path="token.txt"
))

user_id = sp.current_user()["id"]

# scrape the billboard top 100 for a given date
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get("https://www.billboard.com/charts/hot-100/" + date)

soup = BeautifulSoup(response.text, 'html.parser')

songs = soup.select("div.o-chart-results-list-row-container ul li ul li h3#title-of-a-story")

song_names = [sub.getText().strip() for sub in songs]

# searching spotify for the songs by their title
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# create a new playlist in spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard Top 100", public=False)

# add those songs to the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

print("All done! Check out your playlist on Spotify!")
