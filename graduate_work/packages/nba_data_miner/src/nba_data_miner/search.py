# Import libraries
import requests
import pandas as pd
import html5lib
from nba_data_miner.helper_functions import abrv_translator
from nba_data_miner.helper_functions import get_espn_team,get_espn_player
from pandas import json_normalize

###### CLASSES #############
# Create team class
class Team():
    def __init__(self, name = '', abbreviation = '',
                 conference = '', wins = 0, losses = 0,
                 home_record = '', away_record = '',
                 players = {}):
        self.name = name
        self.abrv = abbreviation
        self.conf = conference
        self.wins = wins
        self.losses = losses
        self.home_rec = home_record
        self.away_rec = away_record
        self.players = players
    
    def __str__(self):
        players_df = pd.DataFrame.from_dict(self.players)
        return("Name: " + self.name + "\nAbbreviation: " +
               self.abrv + "\nConference: " + self.conf +
               "\nWins: " + str(self.wins) + "\nLosses: " + 
               str(self.losses) + "\nHome record: " + self.home_rec +
               "\nAway record: " + self.away_rec + "\nPlayers: \n" +
               str(players_df))
    
###### FUNCTIONS ########
def team(team = ""):
    """
    Fucntion that allows a user to perform a case insensitive
    search for a team by full name ('Brooklyn Nets'), short
    name ('Nets'), or abbreviation ('BKN').

    Parameters
    ----------
    team : String

    Returns
    -------
    A Team object defined as follows:
        Name: [string]
        Abbreviation: [string]
        Conference: [string]
        Wins: [int]
        Losses: [int]
        Home record: [string]
        Away record: [string]
        Players: [dict]

    Examples
    --------
    >>> from nba_data_miner import search
    >>> print(search.team("Celtics"))
    Name: Boston Celtics
    Abbreviation: BOS
    Conference: East
    Wins: 22
    Losses: 7
    Home record: 11-2
    Away record: 11-5
    Players:
    
                           0             1           2                 3              4        
    Name     Malcolm Brogdon  Jaylen Brown  JD Davison  Danilo Gallinari  Blake Griffin   
    POS                   PG            SG          SG                PF             PF           
    Age                   30            26          20                34             33            
    HT                 6' 4"         6' 6"       6' 1"            6' 10"          6' 9"        
    WT               229 lbs       223 lbs     195 lbs           236 lbs        250 lbs 
    College         Virginia    California     Alabama                --       Oklahoma 
    Salary       $22,600,000   $28,741,071                    $6,479,000     $1,836,090
    """

    # Request all teams from API
    try:
        r_teams = requests.get('https://www.balldontlie.io/api/v1/teams/')
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    # Make data frame of team information
    teams_list = list(r_teams.json().values())[0]
    teams_df = pd.DataFrame.from_records(teams_list)
    
    # Search team data frame (case insensitive)
    teams_df_lower = teams_df.copy()
    teams_df_lower['abbreviation'] = teams_df_lower['abbreviation'].str.lower()
    teams_df_lower['full_name'] = teams_df_lower['full_name'].str.lower()
    teams_df_lower['name'] = teams_df_lower['name'].str.lower()
    if team.lower() not in teams_df_lower.values: # Error check argument
        raise Exception("You must search by team name or abbreviation." + 
                        " Please check function argument.")
    else:
        # Allows for search by full name, short name, and abbreviation
        if team.lower() in teams_df_lower.full_name.values:
            i = teams_df_lower.index[teams_df_lower['full_name'] == team.lower()]
        elif team.lower() in teams_df_lower.name.values:
            i = teams_df_lower.index[teams_df_lower['name'] == team.lower()]
        elif team.lower() in teams_df_lower.abbreviation.values:
            i = teams_df_lower.index[teams_df_lower['abbreviation'] == team.lower()]
        # Search teams data frame for name, abreviation, and conference
        my_name = teams_df.loc[i,'full_name'].values.item()
        my_abrv = teams_df.loc[i,'abbreviation'].values.item()
        my_conf = teams_df.loc[i,'conference'].values.item()
        
        # Scrape win loss record from ESPN 
        try:
            espn_standings = requests.get('https://www.espn.com/nba/standings/_/group/league').content
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        espn_df_list = pd.read_html(espn_standings,flavor='html5lib')
        espn_teams = espn_df_list[0].T.reset_index().T
        espn_df = espn_df_list[1]
        espn_df.insert(loc = 0, column = "Team", value = espn_teams[0].to_list())
        for i in range(0,len(espn_df)):
            if my_name in espn_df.loc[i,'Team']:
                my_wins = espn_df.loc[i,'W']
                my_losses = espn_df.loc[i,'L']
                my_home_record = espn_df.loc[i,'HOME']
                my_away_record = espn_df.loc[i,'AWAY']
                
        # Scrape dataframe of team players and their information from ESPN
        url_abrv = abrv_translator(my_abrv)
        try:
            espn_players = requests.get('https://www.espn.com/nba/team/roster/_/name/' +
                                                                    url_abrv).content
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        espn_players_list = pd.read_html(espn_players,flavor='html5lib')
        espn_players_df = espn_players_list[0]
        espn_players_df.drop('Unnamed: 0', inplace = True, axis = 1)
        espn_players_df['Name'] = espn_players_df['Name'].str.replace(r'\d+', '', regex = True)
        espn_players_dict = espn_players_df.to_dict('index')
        
        # Make new team object with data
        team_obj = Team(name = my_name, abbreviation = my_abrv, conference = my_conf,
                    wins = my_wins, losses = my_losses, home_record = my_home_record,
                    away_record = my_away_record, players = espn_players_dict)
        # Return
        return(team_obj)
    
def player(player):
    """
    Fucntion that allows a user to perform a case insensitive
    search for a player by full name.

    Parameters
    ----------
    player : String

    Returns
    -------
    DataFrame of the player's information 
    Type: pandas.core.frame.DataFrame

    Examples
    --------
    >>> from nba_data_miner import search
    >>> search.player("Marcus Smart")
    id first_name last_name  height_feet  height_inches position            team  weight_pounds
    0  420     Marcus     Smart            6              4        G  Boston Celtics            220
    """

    # First check that the user is searching player by first and last name.
    if len(player.split()) < 2:
        print("Please use first and last names for search.")
        return
    
    # Request player from API
    try:
        r_player = requests.get('https://www.balldontlie.io/api/v1/players/?search=' + player)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    player_list = list(r_player.json().values())[0]
    player_df = pd.DataFrame.from_records(player_list)
    last_name_column = player_df.pop('last_name')
    player_df.insert(2, 'last_name', last_name_column)
    for i in range(0,len(player_df)):
        team_dict = player_df.loc[i,'team']
        player_df.loc[i,'team'] = team_dict.get('full_name')
        
    return(player_df)
