# Import libraries
import requests
import pandas as pd
import html5lib
import os
from nba_data_miner import compare
from nba_data_miner import search
from nba_data_miner.helper_functions import abrv_translator
from nba_data_miner.helper_functions import get_espn_team,get_espn_player
from json import dumps, loads
from pandas import json_normalize

def test_teams():
    # A test to check that field goal, 3P, 2P and FT make rates
    # are equal to (made/attempted)*100, when comparing teams.
    # Other metrics cannot be tested as the data is updated after
    # each game.
    
    # Collect implied make rates from df.
    df = compare.teams("BKN", "BOS")

    for i in [1,2]:
        FG_test = (df.iloc[13,i]/df.iloc[14,i])*100
        three_p_test = (df.iloc[16,i]/df.iloc[17,i])*100
        two_p_test = (df.iloc[22,i]/df.iloc[23,i])*100
        FT_test = (df.iloc[19,i]/df.iloc[20,i])*100

        # Test with assert
        # We grant a +/- of 1 for the make rates as ESPN tends to
        # update their data on a delay.
        assert(round(FG_test,1)-1 <= df.iloc[15,i] <= round(FG_test,1)+1),"Field goal % value is incorrect."
        assert(round(three_p_test,1)-1 <= df.iloc[18,i] <= round(three_p_test,1)+1),"Three point % value is incorrect."
        assert(round(two_p_test,1)-1 <= df.iloc[24,i] <= round(two_p_test,1)+1),"Two point % value is incorrect."
        assert(round(FT_test,1)-1 <= df.iloc[21,i] <= round(FT_test,1)+1),"Free throw % value is incorrect."

def test_players():
    # A test to check that the test_players() function returns
    # a data frame of player stats when used correctly.
    # The test will search for whichever two players are first
    # on the San Antonio Spurs roster, so that the test does
    # not have to be constantly updated.

    # Collect implied make rates from df.
    espn_players = requests.get('https://www.espn.com/nba/team/roster/_/name/SA').content
    espn_players_list = pd.read_html(espn_players,flavor='html5lib')
    espn_players_df = espn_players_list[0]
    espn_players_df.drop('Unnamed: 0', inplace = True, axis = 1)
    espn_players_df['Name'] = espn_players_df['Name'].str.replace(r'\d+', '', regex = True)
    my_player1 = espn_players_df.Name[0]
    my_player2 = espn_players_df.Name[1]
    df = compare.players(my_player1, my_player2)

    # Test that df exists with assert. ESPN's data updates
    # too slowly to test computation of make rate as 
    # in test_teams().
    assert(df is not None)
