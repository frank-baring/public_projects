# Import libraries
import requests
import pandas as pd
import numpy as np
import html5lib
from nba_data_miner import search
from nba_data_miner.helper_functions import abrv_translator
from nba_data_miner.helper_functions import get_espn_team,get_espn_player
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
    0       GP         28.00          29.00
    1       GS           NaN            NaN
    2      MIN           NaN            NaN
    3      PTS        115.40         112.50
    4       OR         12.10           8.10
    5       DR         31.00          32.70
    6      REB         43.20          40.80
    7      AST         27.40          26.10
    8      STL          7.30           7.00
    9      BLK          5.50           7.00
    10      TO         13.00          14.10
    11      PF         21.80          21.90
    12  AST/TO          2.10           1.80
    13     FGM         43.10          41.90
    14     FGA         91.60          84.00
    15     FG%         47.00          49.90
    16     3PM         13.00          11.60
    17     3PA         34.50          31.40
    18     3P%         37.60          37.00
    19     FTM         16.30          17.00
    20     FTA         20.20          21.40
    21     FT%         80.70          79.40
    22     2PM         30.10          30.30
    23     2PA         57.00          52.60
    24     2P%         52.70          57.60
    25  SC-EFF          1.26           1.34
    26  SH-EFF          0.54           0.57
    
    * Values will be different when used but the returned
      data frame should match the above structure.
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
                             search.team(team1).name : np.round(team1_dict['values'],2),
                             search.team(team2).name : team2_dict['values']})

    return df_final
   


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
    0       GP       20.00         20.00
    1       GS       20.00         20.00
    2      MIN       31.60         36.30
    3      PTS       10.20         26.50
    4       OR        1.00          1.50
    5       DR        5.30          7.20
    6      REB        6.30          8.60
    7      AST        2.80          6.50
    8      STL        0.50          1.30
    9      BLK        1.00          0.60
    10      TO        0.80          3.30
    11      PF        2.00          2.00
    12  AST/TO        3.70          2.00
    13     FGM        4.00         10.40
    14     FGA        7.40         21.90
    15     FG%       53.70         47.50
    16     3PM        2.10          2.40
    17     3PA        4.40          7.50
    18     3P%       46.60         31.50
    19     FTM        0.30          3.40
    20     FTA        0.40          4.80
    21     FT%       62.50         70.50
    22     2PM        1.90          8.10
    23     2PA        3.00         14.50
    24     2P%       64.40         55.70
    25  SC-EFF        1.39          1.21
    26  SH-EFF        0.68          0.53
    
    * Values will be different when used but the returned
      data frame should match the above structure.
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
                                                value = np.round(stats_values[i],2))
        return(df_final)
    

