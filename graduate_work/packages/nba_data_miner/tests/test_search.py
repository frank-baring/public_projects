# Import libraries
import requests
import pandas as pd
import html5lib
import os
from nba_data_miner import search
from nba_data_miner import compare
from nba_data_miner.helper_functions import abrv_translator
from nba_data_miner.helper_functions import get_espn_team,get_espn_player
from json import dumps, loads
from pandas import json_normalize


def test_team():
    # A test to check that the search.team() function
    # returns a team class with coherent values for
    # W/L records, home record, and away record.

    # Collect data
    my_team = search.team("OKC")
    wins = my_team.wins
    losses = my_team.losses
    home_rec = my_team.home_rec
    away_rec = my_team.away_rec
    home_win = int(home_rec.split("-")[0])
    home_loss = int(home_rec.split("-")[1])
    away_win = int(away_rec.split("-")[0])
    away_loss = int(away_rec.split("-")[1])

    # Test with assert
    assert(wins == home_win + away_win), "Home/away record does not reflect W/L."
    assert(losses == home_loss + away_loss), "Home/away record does not reflect W/L."

def test_player():
    # A test to check that the search.team() function
    # creates a data frame when the user searches for 
    # a player in the NBA.
    # The test will search for whichever player is first
    # on the Boston Celtics roster, so that the test does
    # not have to be constantly updated.
    
    # Collect data
    espn_players = requests.get('https://www.espn.com/nba/team/roster/_/name/BOS').content
    espn_players_list = pd.read_html(espn_players,flavor='html5lib')
    espn_players_df = espn_players_list[0]
    espn_players_df.drop('Unnamed: 0', inplace = True, axis = 1)
    espn_players_df['Name'] = espn_players_df['Name'].str.replace(r'\d+', '', regex = True)
    my_player = espn_players_df.Name[0]
    my_player_df = search.player(my_player)
    
    # Test with assert
    assert(my_player_df is not None)


    
