# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 07:51:10 2019

@author: David
"""

# Just Regular Goals
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import numpy as np
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


#################################

def JustRegularGoals(df, dates):
    df = df.iloc[:, 1:8]
    df.columns = ['Period', 'Time in Period', "Team", "Type", 'Scorer', 'Assist1', 'Assist2']
    df['Period'] = df['Period'].str.strip('[')
             
        
    df['Period'] = df['Period'].replace(" ", np.NaN)
    df['Period'] = df['Period'].replace("", np.NaN)
    df['Period'] = df['Period'].fillna(method = 'ffill')
        
    df = df.dropna(thresh = 4).reset_index().drop(['index'], axis = 1)
    df['Scorer'], df['Season Goal Number'] = df['Scorer'].str.split('(',1).str
    df['Season Goal Number'] = df['Season Goal Number'].str.rstrip(')')
    for i in range(0,len(df)):
        if "1st OT" in df.loc[i,'Period']:
            df.loc[i,'Period'] = "OT1"
        elif "2nd OT" in df.loc[i, 'Period']:
                    df.loc[i,'Period'] = "OT2"
        else:
            df.loc[i,'Period'] = df.loc[i,'Period'].strip()[:1]      
    
    
    df['Assist2'] = df['Assist2'].str.lstrip(' and ')
    df["Time in Period (split)"] = df["Time in Period"].str.split(":")
    tags = df["Time in Period (split)"].apply(pd.Series)
    tags = tags.rename(columns = lambda x: 'tag_' + str(x))
    df = pd.concat([df[:], tags[:]], axis = 1)
        
    for i in range(0,len(df)):
        if df.loc[i,"Period"] == "1":
            df.loc[i,"tag_0"] = df.loc[i,"tag_0"]
        elif df.loc[i, "Period"] == "2":
            df.loc[i,"tag_0"] = str(int(df.loc[i,"tag_0"]) + 20)
        elif df.loc[i, "Period"] == "3":
            df.loc[i,"tag_0"] = str(int(df.loc[i,"tag_0"]) + 40)
    df["Time in Game"] = "00:" + df["tag_0"] + ":" + df["tag_1"]
    df['Time in Game'] = pd.to_datetime(df['Time in Game']).dt.time #The .dt is called a .dt accessor
    df = df.drop(["Time in Period (split)", "tag_0", "tag_1"], axis = 1)
    df['Time in Period'] = "00:" + df["Time in Period"]
    df['Time in Period'] = pd.to_datetime(df['Time in Period']).dt.time
    df["Date"] = str(dates)[:8]
    df["Date"] = pd.to_datetime(df["Date"])
     df["Home Team"] = str(dates)[9:]

    df["Game Goal Number"]  = df.index+1
    
  #The following custom function came from Stack Overflow:
    # https://stackoverflow.com/questions/25119524/pandas-conditional-rolling-count
    def count_consecutive_items_n_cols(df, col_name_list, output_col):
        cum_sum_list = [
            (df[col_name] != df[col_name].shift(1)).cumsum().tolist() for col_name in col_name_list
        ]
        df[output_col] = df.groupby(
            ["_".join(map(str, x)) for x in zip(*cum_sum_list)]
        ).cumcount() + 1
        return df
    df = df.sort_values(by=['Team'])
    df = count_consecutive_items_n_cols(df, ["Team", "Date"], "Team Goal Number")
    df = df.sort_values(by=['Game Goal Number'])


##
    
    for k in range(0,len(df)):
        if df.loc[k, "Game Goal Number"] == 1:
            if df.loc[k, "Team"] == df.loc[k,"Home Team"]:
                df.loc[k,"AwayGoal"] = 0 
                df.loc[k,"HomeGoal"] = 1
            else:
                df.loc[k,"AwayGoal"] = 1
                df.loc[k,"HomeGoal"] = 0
        elif df.loc[k, "Team"] == df.loc[k,"Home Team"]:
            df.loc[k,"AwayGoal"] = df.loc[k-1,"AwayGoal"]
            df.loc[k,"HomeGoal"] = df.loc[k-1, "HomeGoal"] +1
        else:
            df.loc[k,"AwayGoal"] = df.loc[k-1, "AwayGoal"] +1
            df.loc[k,"HomeGoal"] = df.loc[k-1, "HomeGoal"]
    
    for k in range(0,len(df)):
        if abs(df.loc[k, "AwayGoal"] - df.loc[k, "HomeGoal"]) == 1:
            df.loc[k,"Impact"] = "Go-Ahead Goal"
        elif abs(df.loc[k, "AwayGoal"] - df.loc[k, "HomeGoal"]) == 0:
            df.loc[k,"Impact"] = "Tie"
        elif abs(df.loc[k, "AwayGoal"] - df.loc[k, "HomeGoal"]) > abs(df.loc[k-1, "AwayGoal"] - df.loc[k-1, "HomeGoal"]):
            df.loc[k, "Impact"] = "Insurance Goal"
        else:
            df.loc[k,"Impact"] = "Lead Shrunk"

##

    cleanedDF = df
    return cleanedDF    
    
######################
# Testing based on two games
######################
#date = ['201810200VAN', '201811030NSH']
date = ['201810200VAN', '201811030NSH', '201811170ARI', '201811160DAL']

game_list = []

for dates in date:
    url = f"https://www.hockey-reference.com/boxscores/{dates}.html#all_scoring"
    games_html = urlopen(url)
    #games_html = open(f"C:\\Users\\dbge\\OneDrive - Chevron\\Random\\{dates}.html")
    games_soup = BeautifulSoup(games_html, 'lxml')
        
    table = games_soup.find('table')
    rows = table.findAll('tr')
    str_cells = str(rows)
    cleantext = BeautifulSoup(str_cells, 'lxml').get_text()
        
    s = cleantext.split(',')
        
    for i in range(1,len(s)):
        s[i] = s[i].replace("\t", "")
        
    df = pd.DataFrame(s)
        
    df[0] = df[0].str.split('\n')
    tags = df[0].apply(pd.Series)
    tags = tags.rename(columns = lambda x: 'tag_' + str(x))
    df = pd.concat([df[:], tags[:]], axis = 1)
    df_width = len(df.columns)

    cleanedDF = JustRegularGoals(df, dates)
    game_list.append(cleanedDF)

goals = pd.concat(game_list).reset_index().drop(columns = ['index'])

