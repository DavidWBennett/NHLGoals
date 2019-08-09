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


#for i in range(0, len(goals)):
#    goals.loc[i,"Seconds"] = time.strptime(goals["Time in Game"][i],'%H:%M:%S').tm_sec + time.strptime(goals["Time in Game"][i],'%H:%M:%S').tm_min*60
    
    
GoalNoEN = goals[goals["Type"] != "EN"]
GoalNoEN = GoalNoEN[GoalNoEN["Type"] != "SHEN"]
FirstGoal =GoalNoEN[GoalNoEN["Game Goal Number"] == 1]

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


num_bins = 30


for team in Goals_List:
    plt.hist(team["Seconds"], bins = num_bins, facecolor='y', edgecolor="red");
    plt.ylabel("Goals Scored")
    plt.xlabel("Time in Game (min)")
    xticmarks = [x for x in range(0, 3600, int(3600/num_bins))]
    xticlabels = [x for x in range(0, 60, int(60/num_bins))]
    plt.xticks(xticmarks, list(map(str, xticlabels)), rotation = 90)
    plt.axvline(x=1200)
    plt.axvline(x=2400)
    plt.show()

plt.hist(GoalNoEN["Seconds"], bins = num_bins, facecolor='y', edgecolor="red");
plt.ylabel("Goals Scored")
plt.xlabel("Time in Game (min)")
xticmarks = [x for x in range(0, 3600, int(3600/num_bins))]
xticlabels = [x for x in range(0, 60, int(60/num_bins))]
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
xticmarks = [x for x in range(0, 3600, int(3600/num_bins))]
xticlabels = [x for x in range(0, 60, int(60/num_bins))]
plt.xticks(xticmarks, list(map(str, xticlabels)), rotation = 90)
plt.axvline(x=1200)
plt.axvline(x=2400)
plt.show()


############
# https://towardsdatascience.com/histograms-and-density-plots-in-python-f6bda88f5ac0
############
import seaborn as sns
FirstGoal =GoalNoEN[GoalNoEN["Game Goal Number"] == 1]

#Matplotlib Histogram
plt.hist(BOSGoals["Seconds"], bins = num_bins, facecolor='y', edgecolor="red");
plt.ylabel("First Goal Scored")
plt.xlabel("Time in Game (min)")
xticmarks = [x for x in range(0, 3600, int(3600/num_bins))]
xticlabels = [x for x in range(0, 60, int(60/num_bins))]
plt.xticks(xticmarks, list(map(str, xticlabels)), rotation = 90)
plt.axvline(x=1200)
plt.axvline(x=2400)
plt.show()

BOSGoals["Seconds"].describe()

#Seaborn Histogram
sns.distplot(BOSGoals["Seconds"], hist = True, kde = False,
             bins = num_bins, color = "blue",
             hist_kws = {'edgecolor':'black'});
    #Add labels
plt.title("Histogram of First Goals Scored in a Game")
plt.xlabel("Time in Game (Sec)")
#plt.ylabel("Probability")



for i, team in enumerate(Goals_List):
    # Set up the plot
    ax = plt.subplot(4, 2, i + 1)
    # Draw the plot
    ax.hist(team["Seconds"], bins = num_bins, facecolor='y', edgecolor="red");
    # Title and labels
    ax.set_title('Team: %s' % team.reset_index()["Team"][0], size = 10)
    ax.set_xlabel("Time in Game", size = 8)
    ax.set_ylabel("Goals Scored", size= 8)
    xticmarks = [x for x in range(0, 3600, int(3600/num_bins))]
    xticlabels = [x for x in range(0, 60, int(60/num_bins))]
    plt.xticks(xticmarks, list(map(str, xticlabels)), rotation = 90)
    plt.yticks(range(0, 11, 10))
    plt.axvline(x=1200)
    plt.axvline(x=2400)
plt.tight_layout()
plt.show()
