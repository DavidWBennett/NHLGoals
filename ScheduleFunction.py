# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 07:47:04 2019

@author: David
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

#teams = ["BOS", "TBL", "TOR", "MTL", "FLA", "BUF", "DET", "OTT"] #Atlantic Division
teams = ["WSH", "NYI", "PIT", "CAR", "CBJ", "PHI", "NYR", "NJD"] #Metropolitan Divison
#teams = ["NSH", "STL", "WPG", "DAL", "CHI", "COL", "MIN"] #Central Divison
#teams = ["CGY", "SJS", "VEG", "ARI", "VAN", "ANA", "EDM", "LAK"] #Pacific Divison
year = 2019 #Change this to pull previous years' data.

team_schedule_list = []

for team in teams:
    schedule_url = f"https://www.hockey-reference.com/teams/{team}/{year}_games.html"
    schedule_html = urlopen(schedule_url)
    
    schedule_soup = BeautifulSoup(schedule_html, 'lxml')
    rows = schedule_soup.find_all('tr')
    
    game_links = []
    all_links = schedule_soup.find_all("a")
    for link in all_links:
        game_links.append(link.get("href"))
    
    #This section is for extracting the identifier for each game, which is the date,
    #followed by a 0, and the three letter home team. Example: 201811040BOS
    game_links = [x for x in game_links if "boxscores/20" in x]
    game_links = [s.strip("/boxscores/") for s in game_links]
    game_links = [s.strip(".html") for s in game_links]

    regular_season_links = game_links[:82] #The regular season is the first 82 games.
    team_schedule_list.append(regular_season_links)

