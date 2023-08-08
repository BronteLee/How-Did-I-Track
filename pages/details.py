import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import date, datetime
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

df = pd.read_json('data/daily-data.json', convert_dates=False)
df['date'] = pd.to_datetime(df['date'], dayfirst=True)

dash.register_page(__name__)

layout = dbc.Container([
    dbc.Row(html.H1("Details")),
    dbc.Row([
        dbc.Col(dmc.DateRangePicker(
            id="date-picker",
            label="Date Range", 
            minDate=date(2017, 12, 25),
            maxDate=date(2023, 7, 31),
            value=[date(2023, 1, 1), date(2023, 7, 20)],
            clearable=False,
        )),
        dbc.Col([
            dbc.Row(html.P(" Low Wear Threshold: ")),
            dbc.Row(dcc.Dropdown(
                [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],
                id="low-wear-dropdown",
                value=8,
                clearable=False,
        ))]),
        dbc.Col(dmc.Switch(
        id="low-wear-switch",
        size="lg",
        radius="sm",
        label="Show Low Wear Days",
        checked=True,
        color="orange"
    ),)
    ]),
    dbc.Row(html.H3(children="My Steps")),
    dbc.Row(dcc.Graph(id="steps", config={
        'displayModeBar': False})),
    dbc.Row(html.H3(children="My Fairly Active Minutes")),
    dbc.Row(dcc.Graph(id="fairly-am", config={
        'displayModeBar': False})),
    dbc.Row(html.H3(children="My Lightly Active Minutes")),
    dbc.Row(dcc.Graph(id="lightly-am", config={
        'displayModeBar': False}))
])

def adherence_colour(df, min_wear):
    vals = df['hours_worn'].tolist()
    colours = []
    for i in vals:
        if i < min_wear:
            colours.append("orange")
        else:
            colours.append("blueviolet")
    return colours

@callback(
    Output(component_id="steps", component_property="figure"),
    Output(component_id="fairly-am", component_property="figure"),
    Output(component_id="lightly-am", component_property="figure"),
    Input(component_id='low-wear-switch', component_property='checked'),
    Input(component_id='date-picker', component_property='value'),
    Input(component_id='low-wear-dropdown', component_property='value'))
def update_graph(on, dates, value):
    start_date = date.fromisoformat(dates[0])
    end_date = date.fromisoformat(dates[1])
    dff = df.query("date >= @start_date & date <= @end_date")
    if not on:
        dff = dff.query("hours_worn >= @value")

    graph_layout = go.Layout(
    margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=0  #top margin
    ), height=300
    )
    steps = go.Figure(data=[go.Bar(
        x=dff['date'], y=dff['steps'],
        marker_color=adherence_colour(dff, value),
    )], layout=graph_layout)
    steps.update_xaxes(title_text="Date", title_font={"size": 16})
    steps.update_yaxes(title_text="Steps", title_font={"size": 16})
    mean = np.mean(dff['steps'])
    steps.add_hline(y=mean, annotation_text="Average: "+str(int(round(mean, 0))), annotation_font_size=20)

    fairly_am = go.Figure(data=[go.Bar(
        x=dff['date'], y=dff['fairly_active_minutes'],
        marker_color=adherence_colour(dff, value)
    )], layout=graph_layout)
    fairly_am.update_xaxes(title_text="Date", title_font={"size": 16})
    fairly_am.update_yaxes(title_text="Fairly Active Minutes", title_font={"size": 16})
    mean = np.mean(dff['fairly_active_minutes'])
    fairly_am.add_hline(y=mean, annotation_text="Average: "+str(int(round(mean, 0))), annotation_font_size=20)

    lightly_am = go.Figure(data=[go.Bar(
        x=dff['date'], y=dff['lightly_active_minutes'],
        marker_color=adherence_colour(dff, value)
    )], layout=graph_layout)
    lightly_am.update_xaxes(title_text="Date", title_font={"size": 16})
    lightly_am.update_yaxes(title_text="Lightly Active Minutes", title_font={"size": 16})
    mean = np.mean(dff['lightly_active_minutes'])
    lightly_am.add_hline(y=mean, annotation_text="Average: "+str(int(round(mean, 0))), annotation_font_size=20)


    return steps, fairly_am, lightly_am