# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 07:50:33 2019

@author: David
"""

import os
os.chdir("C:\\Users\\David\\OneDrive\\Documents\\OneDrive\\Boston Bruins Goals 2018-2019") #David's Computer
#os.chdir("C:\\Users\\dwben\\OneDrive\\Boston Bruins Goals 2018-2019") #Caity's Computer
dirpath = os.getcwd()
print(dirpath)
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import time
import PPandRegularGoals
import JustRegularGoals
import ScheduleFunction
pd.set_option('display.max_rows', 500);
pd.set_option('display.max_columns', 500);
pd.set_option('display.width', 1000);

    
schedules = ScheduleFunction.team_schedule_list #Import the schedules from the ScheduleFunction script.
season_game_list = []

for schedule in schedules:
    date = schedule
    game_list = []
    for dates in date:
        url = f"https://www.hockey-reference.com/boxscores/{dates}.html#all_scoring"
        games_html = urlopen(url)
        #games_html = open(f"C:\\Users\\dbge\\OneDrive - Chevron\\Random\\{dates}.html") #This is for use if you have individual games saves as HTML code.
        games_soup = BeautifulSoup(games_html, 'lxml')
            
        table = games_soup.find('table')
        rows = table.findAll('tr')
        str_cells = str(rows)
        cleantext = BeautifulSoup(str_cells, 'lxml').get_text()
        
        try: #This is needed because some of the games have two types of goals. For example, SH and EN. I needed to account for these.
            commaindex = cleantext.index("\n\t\t\t,") #
            commaindex = commaindex + 4 #
            cleantext = cleantext[:(commaindex-4)] +  cleantext[(commaindex+6):(commaindex+8)] + "\n\n" + cleantext[(commaindex+8):] #
            s = cleantext.split(',') #
        except ValueError:
            s = cleantext.split(',')
            
        try: # Some games had two types of goals, twice. Therefore, I needed to repeat this section of code. I never saw a game with two types of goals, three times.
            commaindex = cleantext.index("\n\t\t\t,") 
            commaindex = commaindex + 4 #
            cleantext = cleantext[:(commaindex-4)] +  cleantext[(commaindex+6):(commaindex+8)] + "\n\n" + cleantext[(commaindex+8):] #
            s = cleantext.split(',') #
        except ValueError:
            s = s
        
            
        for i in range(1,len(s)):
            s[i] = s[i].replace("\t", "")
            
        df = pd.DataFrame(s) #This is our very unstrucutred data frame.
            
        #This section of code splits the dataframe into columns that are labeled with tags.
        df[0] = df[0].str.split('\n')
        tags = df[0].apply(pd.Series)
        tags = tags.rename(columns = lambda x: 'tag_' + str(x))
        df = pd.concat([df[:], tags[:]], axis = 1)
        
        df["tag_0"] = df["tag_0"].str.strip() 
        #Shootouts were eliminated fromt this dataset, which is what this code is doing.
        if len(df[df["tag_0"]== "Shootout"].index.values) == 0:
            df = df
        else:
            df = df[:int(df[df["tag_0"]== "Shootout"].index.values)] #
        
        df_width = len(df.columns)
        
        if  df_width == 15 or df_width == 14:
            cleanedDF = PPandRegularGoals.PPandRegularGoals(df, dates)
            game_list.append(cleanedDF)
            print(dates) #This helps the user know where the function is at any given time in the algorithm.
            time.sleep(3) #This is to help avoid being blacklisted for web scraping.
        elif df_width == 10 or df_width == 9:
            cleanedDF = JustRegularGoals.JustRegularGoals(df, dates)
            game_list.append(cleanedDF)
            print(dates)
            time.sleep(3)        
        else:
            print(dates)
    goals = pd.concat(game_list).reset_index().drop(columns = ['index'])
    goals = goals[['Period', 'Team', 'Type', 'Scorer', 'Assist1', 'Assist2', 'Season Goal Number', 
               'Time in Game', 'Time in Period', 'Home Team', 'Date']]
    season_game_list.append(goals)



goals = pd.concat(season_game_list).reset_index().drop(columns = ['index'])
MetropolitanGoals = goals.drop_duplicates() #The 'Metropolitan' can be changed according to what division is being extracted.
MetropolitanGoals.to_csv("Metropolitan2019.csv") #The 'Metropolitan' can be changed according to what division is being extracted.
