# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 12:04:04 2019

@author: dwben
"""


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import plotly.graph_objs as go

#https://dash.plot.ly/interactive-graphing

#goals = pd.read_csv("C:\\Users\\David\\OneDrive\\Documents\\OneDrive\\Boston Bruins Goals 2018-2019\\Metropolitan2019.csv")
Metropolitan = pd.read_csv("C:\\Users\\dwben\\OneDrive\\Boston Bruins Goals 2018-2019\\Metropolitan2019.csv")
#Atlantic = pd.read_csv("C:\\Users\\dwben\\OneDrive\\Boston Bruins Goals 2018-2019\\Atlantic2019.csv")
#Central = pd.read_csv("C:\\Users\\dwben\\OneDrive\\Boston Bruins Goals 2018-2019\\Central2019.csv")
#Pacific = pd.read_csv("C:\\Users\\dwben\\OneDrive\\Boston Bruins Goals 2018-2019\\Pacific2019.csv")

#goals = Metropolitan.append(Atlantic)
#goals = goals.append(Central)
#goals = goals.append(Pacific)
#goals = goals.drop_duplicates()
goals = Metropolitan

available_teams = sorted(goals["Team"].unique())
number_of_bins = 6

xticmarks = [x for x in range(0, 3600, int(3600/number_of_bins))]
hist_list = []
df1 = pd.DataFrame()
for i in available_teams:
    hist, bin_edges = np.histogram(goals[goals["Team"] == i]["Seconds"], bins = xticmarks) #The bin_edges represents the time period. The hist represents how many goals were scored in that time period.
    df = pd.DataFrame({i : hist}).transpose()
    df1 = df1.append(df)
#data = np.stack(hist_list)
#dataset = pd.DataFrame({"0-120":data[:,0], "121-240" : data[:,1]})
#dataset
df2 =pd.DataFrame(df1.mean())
go.Histogram(x = df2, name = "Division Total", nbinsx = number_of_bins)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {'background': '#1111111', 'text': '#7FDBFF'}


app.layout = html.Div(children=[
            html.H1(children='NHL Regular Season Goals', style = {'textAlign': 'center','color' : colors['text']}),
            html.Div(children='2018-2019 Season', style = {'textAlign': 'center', 'color': colors['text']}),
    html.Div([
            dcc.Dropdown(id = 'crossfilter-team-column', options = [{'label':i, 'value':i} for i in available_teams], value = 'BOS')
            ], style = {'width': '10%', 'display':'inline-block', "padding":"10px 5px"}),
    dcc.Graph(id= 'teamScoringHistogram'),
    html.Div(dcc.Slider(id = 'bin-size', 
                        min = 1, 
                        max = 60, 
                        value = 30, 
                        marks = {str(x): str(x) for x in [2,3,12,20,30,60]}),
             style = {"width" : "100%", "padding" : "0px 20px, 20px 20px"})
])
    

@app.callback(
        Output(component_id = "teamScoringHistogram", component_property = 'figure'),
        [Input(component_id = "crossfilter-team-column", component_property = "value"),
         Input(component_id = "bin-size", component_property = "value")]
        )

def update_team_graph(teamName, binSize):
    dff = goals[goals["Team"] == teamName]
    return {
            "data" : [
                    go.Histogram(x = dff["Seconds"], name = teamName, histnorm = "probability", nbinsx = binSize), #, cumulative_enabled = True
                    go.Histogram(x = goals["Seconds"], name = "League", histnorm = "probability", nbinsx = binSize)], #, cumulative_enabled = True
            "layout" : go.Layout(title=teamName,
                                 xaxis = {"title": "Minutes", "nticks": int(360/binSize),# "tick0":0, "dtick":120, "range": [0, 3600],
                                          "tickvals":[x for x in range(0, 3600, int(3600/binSize))],
                                          "ticktext": [x for x in range(0, 60, int(60/binSize))]},
                                 yaxis = {"title" : "Probability of Goal Scored", "range":[0,0.5]},
                                 #shape = {"type":"line", "line": {"x0": 1200, "y0":0, "x1":1200, "y1":0.5}}
                                 )
            }


#def update_team_graph(teamName):
#    dff = goals[goals["Team"] == teamName]
#    return {'data': [go.Histogram(x = dff["Seconds"])],
#            'layout': go.Layout(xaxis = {"title" : "Seconds"},yaxis = {"title" : "Goals Scored"})
#            }
    
#def update_league_graph(teamName):
#    dff = goals[goals["Team"] == teamName]
#    return {'data': [go.Histogram(x = dff["Seconds"])],
#            'layout': go.Layout(xaxis = {"title" : "Seconds"},yaxis = {"title" : "Goals Scored"})
#            }


if __name__ == '__main__':
    app.run_server(debug=True)
    
    
