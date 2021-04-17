import requests
from bs4 import BeautifulSoup
import socket

## socket connection stuff here

HOST = '127.0.0.1'
PORT = 65444

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept
    with conn:
        print('Connected by:', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)


## webscrapin stuff here

URL = 'https://siege.gg/teams/47'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

team_roster = soup.body.find('section', class_="team__roster pt-5 pt-lg-0 pb-4 section--alt-bg")

player_list = team_roster.find_all('div', class_="roster__player small text-center position-relative")

TSM_players = []

for players in player_list:
    player_name = players.find('h4', class_="mb-0 text-nowrap text-truncate")
    TSM_players.append(player_name.text)

print(TSM_players)