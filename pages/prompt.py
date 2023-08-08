import dash
from dash import html, dcc
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import numpy as np


dash.register_page(__name__, path_template="/prompt/<prompt_id>")

df = pd.read_json("data/test.json", convert_dates=False)
df['start_date'] = pd.to_datetime(df['start_date'], dayfirst=True)
df['end_date'] = pd.to_datetime(df['end_date'], dayfirst=True)

padf = pd.read_json("data/daily-data-2.json", convert_dates=False)
padf['date'] = pd.to_datetime(padf['date'], dayfirst=True)

def graph_label(value):
    if value == "lightly_active_minutes":
        return "Lightly Active Minutes"
    if value == "fairly_active_minutes":
        return "Fairly Active Minutes"
    else:
        return "Steps"

def adherence_colour(df, min_wear):
    vals = df['hours_worn'].tolist()
    colours = []
    for i in vals:
        if i < min_wear:
            colours.append("orange")
        else:
            colours.append("blueviolet")
    return colours

def make_figure(padff, type):
    graph_layout = go.Layout(
    margin=go.layout.Margin(
        l=0,
        r=0,
        b=0,
        t=0
    ), height=300
    )
    graph = go.Figure(data=[go.Bar(
        x=padff['date'], y=padff[type],
        marker_color=adherence_colour(padff, 10)
    )], layout=graph_layout)
    graph.update_xaxes(title_text="Date", title_font={"size": 16})
    graph.update_yaxes(title_text=graph_label(type), title_font={"size": 16})
    mean = np.mean(padff[type])
    graph.add_hline(y=mean, annotation_text="Average: "+str(int(round(mean, 0))), annotation_font_size=20)
    return graph

def layout(prompt_id):
    dff = df.iloc[int(prompt_id)-1]
    start_date = dff['start_date']
    end_date = dff['end_date']
    padff = padf.query("date >= @start_date & date <= @end_date")
    return html.Div(children=[
        html.H1("Prompt"),
        html.H3(dff['prompt']),
        html.P(f"Date Range: {start_date.strftime('%d %b %Y')} to {end_date.strftime('%d %b %Y')}"),
        html.P(dff["text"]),
        html.H4(graph_label(dff['type'])),
        dcc.Graph(id="prompt graph", figure=make_figure(padff, dff['type']), 
            config={'displayModeBar': False}),
        html.H4("Questions"),
        html.P(dff["question1"]),
        html.P(dff["question2"])
    ])