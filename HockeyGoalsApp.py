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
Metropolitan2019 = pd.read_csv("C:\\Users\\dwben\\OneDrive\\Boston Bruins Goals 2018-2019\\Metropolitan2019.csv")
Atlantic2019 = pd.read_csv("C:\\Users\\dwben\\OneDrive\\Boston Bruins Goals 2018-2019\\Atlantic2019.csv")
Central2019 = pd.read_csv("C:\\Users\\dwben\\OneDrive\\Boston Bruins Goals 2018-2019\\Central2019.csv")
Pacific2019 = pd.read_csv("C:\\Users\\dwben\\OneDrive\\Boston Bruins Goals 2018-2019\\Pacific2019.csv")

Central2018 = pd.read_csv("C:\\Users\\dwben\\OneDrive\\Boston Bruins Goals 2018-2019\\Central2018.csv")
Pacific2018 = pd.read_csv("C:\\Users\\dwben\\OneDrive\\Boston Bruins Goals 2018-2019\\Pacific2018.csv")

Metropolitan2019["Season"] = 2019
Atlantic2019["Season"] = 2019
Central2019["Season"] = 2019
Pacific2019["Season"] = 2019

goals = Metropolitan2019.append(Atlantic2019)
goals = goals.append(Central2019)
goals = goals.append(Pacific2019)
goals = goals.append(Pacific2018)
goals = goals.append(Central2018)

######

goals = goals.drop_duplicates()
goals["Type"] = ["Regular" if x is np.nan else x for x in goals["Type"]]
#goals = Metropolitan

available_teams = sorted(goals["Team"].unique())
available_teams.insert(0, "League")
season = goals["Season"].unique()
impact = list(goals["Impact"].unique())
impact.insert(0, "All")
goal_types = list(goals["Type"].unique())
goal_types.insert(0, "All")
#goal_types.insert(1, "Exclude Empty Net")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {'background': '#1111111', 'text': '#7FDBFF'}


app.layout = html.Div(children=[
            html.H1(children='NHL Regular Season Goals', style = {'textAlign': 'center','color' : colors['text']}),
            html.Div(children='Time of Scoring Comparison', style = {'textAlign': 'center', 'color': colors['text']}),
    html.Div([
            dcc.Dropdown(id = 'season1-dropdown', options = [{'label':i, 'value':i} for i in season], value = '2019')
            ], style = {'width': '10%', 'display':'inline-block', "padding":"10px 5px"}),
    html.Div([
            dcc.Dropdown(id = 'team1-column', options = [{'label':i, 'value':i} for i in available_teams], value = 'BOS')
            ], style = {'width': '10%', 'display':'inline-block', "padding":"10px 5px"}),
     html.Div([
            dcc.Dropdown(id = 'season2-dropdown', options = [{'label':i, 'value':i} for i in season], value = '2019')
            ], style = {'width': '10%', 'display':'inline-block', "padding":"10px 5px"}),    
    html.Div([
            dcc.Dropdown(id = 'team2-column', options = [{'label':i, 'value':i} for i in available_teams], value = 'League')
            ], style = {'width': '10%', 'display':'inline-block', "padding":"10px 5px"}),
    html.Div([
            dcc.Dropdown(id = 'impact', options = [{'label':i, 'value':i} for i in impact], value = 'All')
            ], style = {'width': '20%', 'display':'inline-block', "padding":"10px 5px"}),    
   html.Div([
            dcc.Dropdown(id = 'goal-type', options = [{'label':i, 'value':i} for i in goal_types], value = 'All')
            ], style = {'width': '20%', 'display':'inline-block', "padding":"10px 5px"}),
     html.Div([
            dcc.Dropdown(id = 'bin-size',  options=[
                            {'label': "30 Minute Intervals", 'value': 2},
                            {'label': "20 Minute Intervals", 'value': 3},
                            {'label': "5 Minute Intervals", 'value': 12},
                            {'label': "3 Minute Intervals", 'value': 20},
                            {'label': "2 Minute Intervals", 'value': 30},
                            {'label': "1 Minute Intervals", 'value': 60}], 
                        optionHeight = 35, 
                        value = 12,
                    className = "Select Time Interval")
            ], style = {'width': '20%', 'display':'inline-block', "padding":"10px 5px"}),
    dcc.Graph(id= 'teamScoringHistogram')
])
    

@app.callback(
        Output(component_id = "teamScoringHistogram", component_property = 'figure'),
        [Input(component_id = "team1-column", component_property = "value"),
         Input(component_id = "team2-column", component_property = "value"),
         Input(component_id = "bin-size", component_property = "value"),
         Input(component_id = "season1-dropdown", component_property = "value"),
         Input(component_id = "season2-dropdown", component_property = "value"),
         Input(component_id = "impact", component_property = "value"),
         Input(component_id = "goal-type", component_property = "value")
        ]
        )

def update_team_graph(team_name1, team_name2, num_bins, season_option1, season_option2, impact_type, goal_type):

    dff1 = goals[goals["Season"] == int(season_option1)]
    dff2 = goals[goals["Season"] == int(season_option2)] 
####################    
    if team_name1 == "League":
        dff1 = dff1
    else:
        dff1 = dff1[dff1["Team"] == team_name1]
    if team_name2 == "League":
        dff2 = dff2
    else:
        dff2 = dff2[dff2["Team"] == team_name2] 
###################
    if impact_type == "All":
        dff1 = dff1
        dff2 = dff2
    else:
        dff1 = dff1[dff1["Impact"] == impact_type]
        dff2 = dff2[dff2["Impact"] == impact_type]
######################    
    if goal_type == "All":
        dff1 = dff1
        dff2 = dff2
    #elif goal_type == "Exclude Empyt Net":
       # dff1 = dff1[dff1["Type"] != "EN"]
        #dff1 = dff1[dff1["Type"] != "SHEN"]
        #dff1 = dff1[dff1["Type"] != "PPEN"]
        
        #dff2 = dff2[dff2["Type"] != "EN"]
        #dff2 = dff2[dff2["Type"] != "SHEN"]
        #dff2 = dff2[dff2["Type"] != "PPEN"]
    else:
        dff1 = dff1[dff1["Type"] == goal_type]
        dff2 = dff2[dff2["Type"] == goal_type]


    
    trace1 = go.Histogram(
                x = dff1["Seconds"], histnorm='probability', name= str(season_option1) + " " + team_name1,
                xbins=dict( # bins used for histogram
                    start=0.0,
                    end=3600,
                    size=3600/num_bins),
                marker_color='green', opacity=0.75
            )
    trace2 = go.Histogram(
                x=dff2["Seconds"], histnorm='probability', name= str(season_option2) + " " +  team_name2,
                xbins=dict(
                    start=0,
                    end=3600,
                    size=3600/num_bins),
                marker_color='blue', opacity=0.75
            )
    updated1 = go.Layout(
                title_text= team_name1, # title of plot
                xaxis_title_text='Seconds in Game', # xaxis label
                yaxis_title_text='Probability', # yaxis label
                bargap=0.1, # gap between bars of adjacent location coordinates
                bargroupgap=0.0, # gap between bars of the same location coordinates
                shapes=[
                    # Line Vertical
                    go.layout.Shape(
                        type="line",
                        x0=1200,
                        y0=0,
                        x1=1200,
                        y1=0.3,
                        line=dict(
                            color="black",
                            width=3
                        )),
                            # Line Vertical
                    go.layout.Shape(
                        type="line",
                        x0=2400,
                        y0=0,
                        x1=2400,
                        y1=0.3,
                        line=dict(
                            color="black",
                            width=3
                        )),
            ])
    return {
            "data" : [trace1, trace2],
            "layout":  go.Layout(
            xaxis={
                'title': "Minutes",
                'type': 'linear',
                "tickmode" : "array",
                "tickvals" : [x for x in range(0, 3600, int(3600/num_bins))],
                "ticktext" : [str(int(x/60)) for x in range(0, 3600, int(3600/num_bins))]},
                shapes = [
                    # Line Vertical
                    go.layout.Shape(
                        type="line", x0=1200, y0=0, x1=1200, y1= 1.5/num_bins, #0.3/np.log(num_bins),#
                        line=dict(
                            color="black",
                            width=3
                        )),
                            # Line Vertical
                    go.layout.Shape(
                        type="line", x0=2400, y0=0, x1=2400, y1=1.5/num_bins, #0.3/np.log(num_bins),#
                        line=dict(
                            color="black",
                            width=3
                        ))
            ]
            
            #"layout":  updated1
            )}

#go.layout.Shape = {"type": "line", "x0":1200,"y0":0,"x1":1200,"y1":0.3})


if __name__ == '__main__':
    app.run_server(debug=True)
