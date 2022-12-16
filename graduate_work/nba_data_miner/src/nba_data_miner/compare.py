# Import libraries
import requests
import pandas as pd
import numpy as np
import os
import html5lib
import search
from helper_functions import abrv_translator
from helper_functions import get_espn_team,get_espn_player
from json import dumps, loads
from pandas import json_normalize

def teams(team1,team2):
    """
    Compares the stats of two NBA teams.

    Parameters
    ----------
    team1 : String
    team2 : String

    Returns
    -------
    A data frame of side-by-side stats for the two teams.
    Type: pandas.core.frame.DataFrame

    Examples
    --------
    >>> from nba_data_miner import compare
    >>> compare.teams("Suns","Nets")
          stat  Phoenix Suns  Brooklyn Nets
    0       GP        28.000          29.00
    1       GS           NaN            NaN
    2      MIN           NaN            NaN
    3      PTS       115.400         112.50
    4       OR        12.100           8.10
    5       DR        31.000          32.70
    6      REB        43.200          40.80
    7      AST        27.400          26.10
    8      STL         7.300           7.00
    9      BLK         5.500           7.00
    10      TO        13.000          14.10
    11      PF        21.800          21.90
    12  AST/TO         2.100           1.80
    13     FGM        43.100          41.90
    14     FGA        91.600          84.00
    15     FG%        47.000          49.90
    16     3PM        13.000          11.60
    17     3PA        34.500          31.40
    18     3P%        37.600          37.00
    19     FTM        16.300          17.00
    20     FTA        20.200          21.40
    21     FT%        80.700          79.40
    22     2PM        30.100          30.30
    23     2PA        57.000          52.60
    24     2P%        52.700          57.60
    25  SC-EFF         1.261           1.34
    26  SH-EFF         0.540           0.57
    """
    # Get names for web scraping
    abrv1 = search.team(team1).abrv
    abrv2 = search.team(team2).abrv
    
    # Scrape stats on both teams
    # Team 1
    stats1_r = requests.get('https://www.espn.com/nba/team/stats/_/name/' + 
                                            abrv_translator(abrv1)).content
    team1_dict = get_espn_team(stats1_r)
    
    # Team 2 
    stats2_r = requests.get('https://www.espn.com/nba/team/stats/_/name/' + 
                                            abrv_translator(abrv2)).content
    team2_dict = get_espn_team(stats2_r)

    # Return final data frame
    df_final = pd.DataFrame({'stat' : team2_dict['metrics'],
                             search.team(team1).name : team1_dict['values'],
                             search.team(team2).name : team2_dict['values']})
    
    print(df_final)


def players(player1,player2):
    """
    Compares the stats of two NBA players.

    Parameters
    ----------
    player1 : String
    player2 : String

    Returns
    -------
    A data frame of side-by-side stats for the two players.
    Type: pandas.core.frame.DataFrame

    Examples
    --------
    >>> from nba_data_miner import compare
    >>> compare.players("Al Horford","Lebron James")
          stat  Al Horford  LeBron James
    0       GP      20.000         20.00
    1       GS      20.000         20.00
    2      MIN      31.600         36.30
    3      PTS      10.200         26.50
    4       OR       1.000          1.50
    5       DR       5.300          7.20
    6      REB       6.300          8.60
    7      AST       2.800          6.50
    8      STL       0.500          1.30
    9      BLK       1.000          0.60
    10      TO       0.800          3.30
    11      PF       2.000          2.00
    12  AST/TO       3.700          2.00
    13     FGM       4.000         10.40
    14     FGA       7.400         21.90
    15     FG%      53.700         47.50
    16     3PM       2.100          2.40
    17     3PA       4.400          7.50
    18     3P%      46.600         31.50
    19     FTM       0.300          3.40
    20     FTA       0.400          4.80
    21     FT%      62.500         70.50
    22     2PM       1.900          8.10
    23     2PA       3.000         14.50
    24     2P%      64.400         55.70
    25  SC-EFF       1.388          1.21
    26  SH-EFF       0.680          0.53
    """
    # First check that the user is searching player by first and last name.
    if len(player1.split()) < 2 or len(player2.split()) < 2 :
        print("Please use first and last names for players.")
        return
    
    # Search players to get team aabreviation for searching
    # accounting for multiple search results.
    try:# Try searching for the players
        player1_df = search.player(player1)
        player2_df = search.player(player2)
    except KeyError:# Error check
        print("Please check your player search.")
    else:# Else, collect abbreviations and search stats for all players in results
        players1 = (player1_df['first_name'] + " " + player1_df['last_name']).tolist()
        teams1 = player1_df['team'].tolist()
        players2 = (player2_df['first_name'] + " " + player2_df['last_name']).tolist()
        teams2 = player2_df['team'].tolist()
        # Concatenate lists
        players_final = players1 + players2
        teams_final = teams1 + teams2
        abrv_list = []
        for team in teams_final:
            abrv_list.append(abrv_translator(search.team(team).abrv))
        # Collect stats
        stats_values = []
        metrics = []
        to_pop = []
        for i in range(0,len(abrv_list)):
            stats_r = requests.get('https://www.espn.com/nba/team/stats/_/name/' + 
                                                             abrv_list[i]).content
            stats_dict = get_espn_player(stats_r,players_final[i])
            if stats_dict != 0:
                stats_values.append(stats_dict['values'])
                metrics = stats_dict['metrics']
            else: # Handle players no longer in NBA
                to_pop.append(players_final[i])
        players_final = [e for e in players_final if e not in to_pop]
        # Make final data frame
        df_final = pd.DataFrame(data = metrics, columns = ['stat'])
        for i in range(0,len(stats_values)):
            if players_final[i] not in df_final.columns:
                df_final.insert(loc = df_final.shape[1], column = players_final[i], 
                                                            value = stats_values[i])
            
        print(df_final)
    

