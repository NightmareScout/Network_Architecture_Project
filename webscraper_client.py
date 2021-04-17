import socket

HOST = '127.0.0.1'
SENDPORT = 65444
RECPORT = 65445

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, SENDPORT))
print('Connected.')
print('This terminal serves to provide information about Pro-League Siege Teams.')
print('It is updated from the internet every time you call it via webscraping.')
print('You can find information about each of the four regions, and five of the top teams of each.\n')

## Functions ##
def converttostr(input_seq, seperator):
    final_str = seperator.join(input_seq)
    return final_str

## Data Variables ##
team = ''
region = ''
rank = ''
members = []
time_last_played = ''
place_last_played = ''
next_play_day = ''
next_play_time = ''

is_region_selected = False

while is_region_selected is False:

    region_select = input('Select Region: [1] Europe, [2] North America, [3] Asia-Pacific, [4] Latin America: ')
    if region_select == '1': #Europe
        region = 'Europe'
        team_select = input('Select Team: [1] Team Empire, [2] BDS Esports, [3] G2 Esports, [4] Virtus.Pro, [5] TrainHard Esports: ')
        is_region_selected = True

        if team_select == '1':
            team = 'Team Empire'
        elif team_select == '2':
            team = 'BDS Esports'
        elif team_select == '3':
            team = 'G2 Esports'
        elif team_select == '4':
            team = 'Virtus.Pro'
        elif team_select == '5':
            team = 'TrainHard Esports'

    elif region_select == '2': #North America
        region = 'North America'
        team_select = input('Select Team: [1] TSM, [2] DarkZero Esports, [3] Spacestation Gaming, [4] Oxygen Esports, [5] Disrupt Gaming: ')
        is_region_selected = True

        if team_select == '1':
            team = 'TSM'
        elif team_select == '2':
            team = 'DarkZero Esports'
        elif team_select == '3':
            team = 'Spacestation Gaming'
        elif team_select == '4':
            team = 'Oxygen Esports'
        elif team_select == '5':
            team = 'Disrupt Gaming'

    elif region_select == '3': #Asia
        region = 'Asia-Pacific'
        team_select = input('Select Team: [1] Giants Gaming, [2] Cloud9, [3] Wildcard Gaming, [4] Xavier Esports, [5] CYCLOPS Athlete Gaming: ')
        is_region_selected = True

        if team_select == '1':
            team = 'Giants Gaming'
        elif team_select == '2':
            team = 'Cloud9'
        elif team_select == '3':
            team = 'Wildcard Gaming'
        elif team_select == '4':
            team = 'Xavier Esports'
        elif team_select == '5':
            team = 'CYCLOPS Athlete Gaming'

    elif region_select == '4': #LATAM
        region = 'Latin America'
        team_select = input('Select Team: [1] Team Liquid, [2] Ninjas in Pyjamas, [3] FaZe Clan, [4] MIBR, [5] INTZ e-Sports: ')
        is_region_selected = True

        if team_select == '1':
            team = 'Team Liquid'
        elif team_select == '2':
            team = 'Ninjas in Pyjamas'
        elif team_select == '3':
            team = 'FaZe Clan'
        elif team_select == '4':
            team = 'MIBR'
        elif team_select == '5':
            team = 'INTZ e-Sports'

    else:
        print('Invalid Choice, please restart.')

## Choices made, we need to send and receive the info here, staging it in a list for the final knowledge drop

s.send(region.encode())
s.send(team.encode())
s.close()

## right after sending data, set up for recieving ##
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, RECPORT))
s.listen(1)

listen_var = True
data_buff = []

while listen_var == True:
    print('Waiting for response....')

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


recv_data = data_buff[0].split(',')

rank = recv_data[0]
time_last_played = recv_data[1]
place_last_played = recv_data[2]
next_play_day = recv_data[3]
next_play_time = recv_data[4]

for x in range(5,10):
    members.append(recv_data[x])

seperator = ', '
members_list = converttostr(members,seperator)

## end of the recieving portion ##

## The previously mentioned knowledge drop ##

print("\n",team, "is currently ranked #", rank, "in the", region, "League.")
print("\n The members of", team, "are", members_list,".")
print("\n",team, "last played", time_last_played, "in", place_last_played,".")
print("\n Their next match will be", next_play_day, "at", next_play_time,".\n")

#print(s.recv(1024).decode())
#s.send(region_select.encode())
#print(s.recv(1024).decode())
