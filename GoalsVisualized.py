# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 13:32:37 2019

@author: dwben
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
import time
%matplotlib inline

import os
os.chdir("C:\\Users\\David\\OneDrive\\Documents\\OneDrive\\Boston Bruins Goals 2018-2019") #David's Computer
#os.chdir("C:\\Users\\dwben\\OneDrive\\Boston Bruins Goals 2018-2019") #Caity's Computer
dirpath = os.getcwd()


goals = pd.read_csv("Metropolitan2019.csv")


for i in range(0, len(goals)):
    goals.loc[i,"Seconds"] = time.strptime(goals["Time in Game"][i],'%H:%M:%S').tm_sec + time.strptime(goals["Time in Game"][i],'%H:%M:%S').tm_min*60
    
    
GoalNoEN = goals[goals["Type"] != "EN"]
GoalNoEN = GoalNoEN[GoalNoEN["Type"] != "SHEN"]

Metropolitan_Teams = ["TBL", "BOS", "TOR", "MTL", "FLA", "BUF", "DET", "OTT"]
TBLGoals = GoalNoEN[GoalNoEN["Team"] == "TBL"]
BOSGoals = GoalNoEN[GoalNoEN["Team"] == "BOS"]
TORGoals = GoalNoEN[GoalNoEN["Team"] == "TOR"]
MTLGoals = GoalNoEN[GoalNoEN["Team"] == "MTL"]
FLAGoals = GoalNoEN[GoalNoEN["Team"] == "FLA"]
BUFGoals = GoalNoEN[GoalNoEN["Team"] == "BUF"]
DETGoals = GoalNoEN[GoalNoEN["Team"] == "DET"]
OTTGoals = GoalNoEN[GoalNoEN["Team"] == "OTT"]
Goals_List = [TBLGoals, BOSGoals, TORGoals, MTLGoals, FLAGoals, BUFGoals, DETGoals, OTTGoals]


num_bins = 15
for team in Goals_List:
    plt.hist(team["Seconds"], bins = num_bins, facecolor='y', edgecolor="red");
    plt.ylabel("Goals Scored")
    plt.xlabel("Time in Game (min)")
    xticmarks = [x for x in range(0, 3600, int(3600/bins))]
    xticlabels = [x for x in range(0, 60, int(60/bins))]
    plt.xticks(xticmarks, list(map(str, xticlabels)), rotation = 90)
    plt.axvline(x=1200)
    plt.axvline(x=2400)
    plt.show()

plt.hist(GoalNoEN["Seconds"], bins = num_bins, facecolor='y', edgecolor="red");
plt.ylabel("Goals Scored")
plt.xlabel("Time in Game (min)")
xticmarks = [x for x in range(0, 3600, int(3600/bins))]
xticlabels = [x for x in range(0, 60, int(60/bins))]
plt.xticks(xticmarks, list(map(str, xticlabels)), rotation = 90)
plt.axvline(x=1200)
plt.axvline(x=2400)
plt.show()


##########################
# Use the histogram function to bin the data
counts, bin_edges = np.histogram(BOSGoals["Seconds"], bins=num_bins)

# Now find the cdf
cdf = np.cumsum(counts)

# And finally plot the cdf
plt.plot(bin_edges[1:], cdf)
xticmarks = [x for x in range(0, 3600, int(3600/bins))]
xticlabels = [x for x in range(0, 60, int(60/bins))]
plt.xticks(xticmarks, list(map(str, xticlabels)), rotation = 90)
plt.axvline(x=1200)
plt.axvline(x=2400)
plt.show()
