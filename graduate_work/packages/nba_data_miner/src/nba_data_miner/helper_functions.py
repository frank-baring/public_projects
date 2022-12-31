# Import libraries
import requests
import pandas as pd
import os
import html5lib
from json import dumps, loads
from pandas import json_normalize

def abrv_translator(abrv_in):
    # Abbreviation directory to sync espn and balldontlie API
    abrv_dir = {'espn':['ATL','BOS','BKN','CHA','CHI','CLE','DAL','DEN','DET',
                       'GS','HOU','IND','LAC','LAL','MEM','MIA','MIL','MIN',
                       'NO','NY','OKC','ORL','PHI','PHX','POR','SAC','SA',
                       'TOR','UTAH','WSH'],
                'api':['ATL','BOS','BKN','CHA','CHI','CLE','DAL','DEN','DET',
                      'GSW','HOU','IND','LAC','LAL','MEM','MIA','MIL','MIN',
                      'NOP','NYK','OKC','ORL','PHI','PHX','POR','SAC','SAS',
                      'TOR','UTA','WAS']}
    abrv_df = abrv_df = pd.DataFrame(abrv_dir)
    if abrv_in not in abrv_dir['api']:
        raise Exception("That abbreviation does not match with the api." +
                        " Please run search.team(your team), to find correct abbrevation.")
    else:
        abrv_out = abrv_df.loc[abrv_df.index[abrv_df['api'] == abrv_in][0],'espn']
        return(abrv_out) # Returns espn abbreviation for searching
    
def get_espn_team(request):
    # Function to scrape stats about a team in the NBA and return a dict.
    stats_content = pd.read_html(request,flavor='html5lib')
    stats_metrics = stats_content[1].columns.tolist() + stats_content[2].columns.tolist()
    stats_values_overall = stats_content[1].iloc[len(stats_content[1])-1,:].tolist()
    stats_values_shooting =  stats_content[2].iloc[len(stats_content[2])-1,:].tolist()
    stats_values_final = stats_values_overall + stats_values_shooting

    # Check stats data frames are same length
    if len(stats_metrics) != len(stats_metrics):
            raise Exception("There seems to be a problem with the ESPN data. Check columns.")
    elif len(stats_values_final) != len(stats_values_final):
            raise Exception("There seems to be a problem with the ESPN data. Check values.")
    else:
        final_dict = {'metrics' : stats_metrics, 'values' : stats_values_final}
        return(final_dict)
    
def get_espn_player(request, player_name):
    # Function to scrape stats about a player in the NBA and return a dict.
    
    # Get index of player in team data frame
    stats_content = pd.read_html(request,flavor='html5lib')
    stats_metrics = stats_content[1].columns.tolist() + stats_content[2].columns.tolist()
    name_df = stats_content[0]
    name_count = name_df['Name'].str.contains(player_name).sum()
    if name_count < 1: # Check if player currently plays for the NBA
        return(0)
    else:
        ind = name_df[name_df['Name'].str.contains(player_name)].index.tolist()[0]
        stats_values_overall = stats_content[1].iloc[ind,:].tolist()
        stats_values_shooting =  stats_content[2].iloc[ind,:].tolist()
        stats_values_final = stats_values_overall + stats_values_shooting

        # Check stats data frames are same length
        if len(stats_metrics) != len(stats_metrics):
                raise Exception("There seems to be a problem with the ESPN data. Check columns.")
        elif len(stats_values_final) != len(stats_values_final):
                raise Exception("There seems to be a problem with the ESPN data. Check values.")
        else:
            final_dict = {'metrics' : stats_metrics, 'values' : stats_values_final}
            return(final_dict)

