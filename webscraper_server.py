import requests
from bs4 import BeautifulSoup
import socket

## Functions ##
def converttostr(input_seq, seperator):
    final_str = seperator.join(input_seq)
    return final_str


## Europe
Empire_URL = 'https://siege.gg/teams/63'
BDS_URL = 'https://siege.gg/teams/367'
G2_URL = 'https://siege.gg/teams/1'
Virtus_URL = 'https://siege.gg/teams/272'
TrainHard_URL = 'https://siege.gg/teams/273'

## North America
TSM_URL = 'https://siege.gg/teams/47'
DarkZero_URL = 'https://siege.gg/teams/15'
Spacestation_URL = 'https://siege.gg/teams/16'
Oxygen_URL = 'https://siege.gg/teams/40'
Disrupt_URL = 'https://siege.gg/teams/465'

## Asia
Giants_URL = 'https://siege.gg/teams/36'
Cloud_URL = 'https://siege.gg/teams/39'
Wildcard_URL = 'https://siege.gg/teams/90'
Xavier_URL = 'https://siege.gg/teams/357'
Cyclops_URL = 'https://siege.gg/teams/108'

## LATAM
Liquid_URL = 'https://siege.gg/teams/19'
Ninja_URL = 'https://siege.gg/teams/18'
Faze_URL = 'https://siege.gg/teams/50'
MIBR_URL = 'https://siege.gg/teams/282'
INTZ_URL = 'https://siege.gg/teams/22'

Search_URL = ''

## socket connection stuff here ##

HOST = '127.0.0.1'
RECPORT = 65444
SENDPORT = 65445

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, RECPORT))
s.listen(1)

listen_var = True
data_buff = []
team = ''

while listen_var == True:
    print('Listening....')

    conn, addr = s.accept()

    try:
        print('Connected: ', addr)

        while True:
            data = conn.recv(1024).decode()
            if data:
                data_buff.append(data)
            else:
                break
    finally:
        listen_var = False
        conn.close()

region = data_buff[0]
team = data_buff[1]

if region == 'Europe':
    if team == 'Team Empire':
        Search_URL = Empire_URL
    elif team == 'BDS Esports':
        Search_URL = BDS_URL
    elif team == 'G2 Esports':
        Search_URL = G2_URL
    elif team == 'Virtus.Pro':
        Search_URL = Virtus_URL
    elif team == 'TrainHard Esports':
        Search_URL = TrainHard_URL
elif region == 'North America':
    if team == 'TSM':
        Search_URL = TSM_URL
    elif team == 'DarkZero Esports':
        Search_URL = DarkZero_URL
    elif team == 'Spacestation Gaming':
        Search_URL = Spacestation_URL
    elif team == 'Oxygen Esports':
        Search_URL = Oxygen_URL
    elif team == 'Disrupt Gaming':
        Search_URL = Disrupt_URL
elif region == 'Asia-Pacific':
    if team == 'Giants Gaming':
        Search_URL = Giants_URL
    elif team == 'Cloud9':
        Search_URL = Cloud_URL
    elif team == 'Wildcard Gaming':
        Search_URL = Wildcard_URL
    elif team == 'Xavier Esports':
        Search_URL = Xavier_URL
    elif team == 'CYCLOPS Athlete Gaming':
        Search_URL = Cyclops_URL
elif region == 'Latin America':
    if team == 'Team Liquid':
        Search_URL = Liquid_URL
    elif team == 'Ninjas in Pyjamas':
        Search_URL = Ninja_URL
    elif team == 'FaZe Clan':
        Search_URL = Faze_URL
    elif team == 'MIBR':
        Search_URL = MIBR_URL
    elif team == 'INTZ e-Sports':
        Search_URL = INTZ_URL

## entire webscraping chunk

page = requests.get(Search_URL)
soup = BeautifulSoup(page.content, 'html.parser')

# this section pulls the overall rank of the team in the region

team_intro = soup.body.find('div', class_="team__intro")
temp = team_intro.find('span', class_="meta__item")
rank_temp = temp.text
rank = rank_temp[1]

# this section pulls the player names

team_roster = soup.body.find('section', class_="team__roster pt-5 pt-lg-0 pb-4 section--alt-bg")
player_list = team_roster.find_all('div', class_="roster__player small text-center position-relative")

team_players = []

for players in player_list:
    player_name = players.find('h4', class_="mb-0 text-nowrap text-truncate")
    team_players.append(player_name.text)

## this section pulls the time last played by the team

bottom_part = soup.body.find('section', class_="section section--padded section--alt-bg")
results = bottom_part.find('div', class_="col-sm-12 col-lg-8 js-matches-list")
temp = results.find('span', class_="meta__item meta__day")
time_last_played = temp.text

## this section pulls the place last played by the team

temp = results.find('span', class_="meta__item meta__competition")
place_last_played = temp.text

## this section pulls the next day the team plays

upcoming = bottom_part.find('div', class_="col-sm-12 col-lg-4 pr-lg-5 js-matches-list")
temp = upcoming.find('span', class_="meta__item meta__day")
next_play_day = temp.text

## this section pulls the next place the team plays

temp = bottom_part.find('span', class_="meta__item meta__time")
next_play_time = temp.text

## end of webscraping. All data has been collected, now we just send it back

## begin of sending data part ##

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, SENDPORT))

details = [rank, time_last_played, place_last_played, next_play_day, next_play_time]
mail_box = details + team_players
seperator = ','
shipping_package = converttostr(mail_box, seperator)

s.send(shipping_package.encode())

print('Information Finished Sending, Shutting Down.')
s.close()