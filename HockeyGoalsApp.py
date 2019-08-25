# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 12:04:04 2019

@author: dwben
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objs as go

#https://dash.plot.ly/interactive-graphing

#goals = pd.read_csv("C:\\Users\\David\\OneDrive\\Documents\\OneDrive\\Boston Bruins Goals 2018-2019\\Metropolitan2019.csv")
goals = pd.read_csv("C:\\Users\\dwben\\OneDrive\\Boston Bruins Goals 2018-2019\\Metropolitan2019.csv")
x = goals["Seconds"]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
        'background': '#1111111',
        'text': '#7FDBFF'}


app.layout = html.Div(children=[
    html.H1(children='NHL Regular Season Goals',
            style = {'textAlign': 'center','color' : colors['text']}),
    html.Div(children='2018-2019 Season', style = {
            'textAlign': 'center',
            'color': colors['text']
            }),
    dcc.Graph(
        id='Scoring Histogram',
        figure={
            'data': [go.Histogram(x = x)],
            'layout': {'title': 'Goals Scored per Minute'}
                }
                ),
    dcc.Input(id = "team", value = "initial team", type = 'text'),
])

@app.callback(
        Output(component_id = 'Scoring Histogram', component_property = 'figure'),
        [Input(component_id = "team", component_property = "value")]
        )

def update_output_div(input_value):
    return 'You have entered "{}"'.format(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)
    
    
