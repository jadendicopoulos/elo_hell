import os 
print(os.getcwd())
import pandas as pd
import numpy as np
from riotwatcher import LolWatcher, ApiError 
import time

my_api_key = ''

lol_watcher = LolWatcher(my_api_key, default_status_v4=True)

player_region = 'na1'
player_name = 'ping my ult'

player = lol_watcher.summoner.by_name(player_region, player_name)
player_ranked_stats = lol_watcher.league.by_summoner(player_region, player['id'])
print(player_ranked_stats)

versions = lol_watcher.data_dragon.versions_for_region(player_region)
champions_version = versions['n']['champion']
summoner_spells_version=versions['n']['summoner']
items_version=versions['n']['item']
current_champ_list = lol_watcher.data_dragon.champions(champions_version)

player_matches = lol_watcher.match.matchlist_by_puuid(player_region, player['puuid'])

n_games = 20
Games = {}
Game_duration=np.zeros(n_games)
Damage = np.zeros(n_games)

j=0
cont=0
while cont<n_games:
    try:
        last_match = player_matches[cont]
        match_detail = lol_watcher.match.by_id(player_region, last_match)
        participants = []
        for row in match_detail['metadata']['participants']:
            participants_row = {}
            participants_row['champion'] = row['championId']
            participants_row['win'] = row['stats']['win']
            participants_row['assists'] = row['stats']['assists']
            participants.append(participants_row)
        Games[j] = pd.DataFrame(participants)
        champ_dict = {}
        for key in static_champ_list['data']: 
            row = static_champ_list['data'][key] 
            champ_dict[row['key']] = row['id']
            summoners_dict = {}
        for key in static_summoners_list['data']:
            row = static_summoners_list['data'][key]
            summoners_dict[row['key']] = row['id']
            Summoner_name = []
        for row in match_detail['participantIdentities']:
            Summoner_name_row = {}
            Summoner_name_row=row['player']['summonerName']
            Summoner_name.append(Summoner_name_row)
            i=0
        for row in participants:
            row['championName'] = champ_dict[str(row['champion'])]
            row['Summoner_name']=Summoner_name[i]
            row['Summoner Spell 1']=summoners_dict[str(row['spell1'])]
            row['Summoner Spell 2']=summoners_dict[str(row['spell2'])]
            i+=1
  
        Games[j]= pd.DataFrame(participants)
        for index, row in Games[j].iterrows():
            if row['Summoner_name']=='%YOUR SUMMONER NAME%':
                Damage[j]=row['totalDamageDealt']
                Gold[j]=row['goldEarned']
            time.sleep(10)
            j+=1
            cont+=1
    except:
        cont+=1