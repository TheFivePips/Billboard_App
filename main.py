from bs4 import BeautifulSoup
import requests

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get("https://www.billboard.com/charts/hot-100/" + date)

soup = BeautifulSoup(response.text, 'html.parser')

songs = soup.select("div.o-chart-results-list-row-container ul li ul li h3#title-of-a-story")

song_names = [sub.getText().strip() for sub in songs]

print(song_names)
