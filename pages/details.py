import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import date
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from reflection import reflection_panel
from correlationgraph import corr_graph


df = pd.read_json('data/synthetic-daily-data.json', convert_dates=False)
df['date'] = pd.to_datetime(df['date'], dayfirst=True)

dash.register_page(__name__)

layout = dbc.Row([dbc.Col([
    dbc.Row(html.H1("Details")),
    dbc.Row([
    dbc.Col([
        dbc.Row(html.P("Date Range", style={"text-align": "center"})),
        dbc.Row(dmc.DateRangePicker(
            id="date-picker",
            minDate=date(2017, 12, 25),
            maxDate=date(2023, 9, 6),
            value=[date(2023, 1, 1), date(2023, 9, 6)],
            clearable=False,
            style={"margin": "auto"}
    ))]),
    dbc.Col([
        dbc.Row(html.P("Minimum Hours of Tracker Wear", style={"text-align": "center"})),
        dbc.Row(dcc.Dropdown(
            [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],
            id="low-wear-dropdown",
            value=10,
            clearable=False), 
            style={"bottom": "0", "width": "50%", "margin": "auto"})
    ]),
        dbc.Col([
            dbc.Row(html.P("Show Days Below Minimum", style={"text-align": "center"})),
            dbc.Row(dmc.Switch(
        id="low-wear-switch",
        size="lg",
        radius="sm",
        checked=True,
        color="orange", style={"width": "fit-content", "margin": "auto"}), )
        ])
    ]),
        dbc.Row(html.H3(children="My Steps")),
        dbc.Row(dcc.Graph(id="steps", config={
            'displayModeBar': False})),
        dbc.Row(html.P("Contextual Factors")),
        dbc.Row(dcc.Loading(type="circle", children=dcc.Graph(
            id="context_steps_details", config={'displayModeBar': False}))),
        dbc.Row(html.H3(children="My Fairly Active Minutes")),
        dbc.Row(dcc.Graph(id="fairly-am", config={
            'displayModeBar': False})),
        dbc.Row(html.P("Contextual Factors")),
        dbc.Row(dcc.Loading(type="circle", children=dcc.Graph(
            id="context_fairly_AM_details", config={'displayModeBar': False}))),
        dbc.Row(html.H3(children="My Lightly Active Minutes")),
        dbc.Row(dcc.Graph(id="lightly-am", config={
            'displayModeBar': False})),
        dbc.Row(html.P("Contextual Factors")),
        dbc.Row(dcc.Loading(type="circle", children=dcc.Graph(
            id="context_lightly_AM_details", config={'displayModeBar': False})))
    ], width=9),
dbc.Col(reflection_panel(None), width=3, className="reflection--panel")],
style={"padding-left": "10px", "max-width": "100%"}
)

def adherence_colour(df, min_wear):
    vals = df['hours_worn'].tolist()
    colours = []
    for i in vals:
        if i < min_wear:
            colours.append("orange")
        else:
            colours.append("blueviolet")
    return colours

def val_to_text(val):
    if val == "steps":
        return "Steps"
    if val == "fairly_active_minutes":
        return "Fairly Active Minutes"
    if val == "hours_worn":
        return "Hours Worn"
    else:
        return "Lightly Active Minutes"

def make_hover_text(dff, datatype):
    hover_text = []
    for i in dff.index:
        hover_text.append(f"{dff['date'][i].strftime('%a %d/%m/%Y')}<br>{val_to_text(datatype)}: {int(dff[datatype][i])}")
    return hover_text

@callback(
    Output(component_id="steps", component_property="figure"),
    Output(component_id="context_steps_details", component_property="figure"),
    Output(component_id="fairly-am", component_property="figure"),
    Output(component_id="context_fairly_AM_details", component_property="figure"),
    Output(component_id="lightly-am", component_property="figure"),
    Output(component_id="context_lightly_AM_details", component_property="figure"),
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
            l=0,
            r=0,
            b=0,
            t=0
        ), 
        height=300
    )
    steps = go.Figure(data=[go.Bar(
        x=dff['date'], y=dff['steps'],
        marker_color=adherence_colour(dff, value),
        hovertemplate=("%{customdata}"),
        customdata=make_hover_text(dff, 'steps'),
    )], layout=graph_layout)
    steps.update_xaxes(title_text="Date", title_font={"size": 16})
    steps.update_yaxes(title_text="Steps", title_font={"size": 16})
    mean = np.mean(dff['steps'])
    steps.add_hline(y=mean, line_width=3,
                    annotation_text="Average: "+str(int(round(mean, 0))), 
                    annotation_font_size=12, annotation_bgcolor="white")
    fairly_am = go.Figure(data=[go.Bar(
        x=dff['date'], y=dff['fairly_active_minutes'],
        marker_color=adherence_colour(dff, value),
        hovertemplate=("%{customdata}"),
        customdata=make_hover_text(dff, 'fairly_active_minutes'),
    )], layout=graph_layout)
    fairly_am.update_xaxes(title_text="Date", title_font={"size": 16})
    fairly_am.update_yaxes(title_text="Fairly Active Minutes", title_font={"size": 16})
    mean = np.mean(dff['fairly_active_minutes'])
    fairly_am.add_hline(y=mean, line_width=3,
                        annotation_text="Average: "+str(int(round(mean, 0))), 
                        annotation_font_size=12,  annotation_bgcolor="white")

    lightly_am = go.Figure(data=[go.Bar(
        x=dff['date'], y=dff['lightly_active_minutes'],
        marker_color=adherence_colour(dff, value),
        hovertemplate=("%{customdata}"),
        customdata=make_hover_text(dff, 'lightly_active_minutes'),
    )], layout=graph_layout)
    lightly_am.update_xaxes(title_text="Date", title_font={"size": 16})
    lightly_am.update_yaxes(title_text="Lightly Active Minutes", title_font={"size": 16})
    mean = np.mean(dff['lightly_active_minutes'])
    lightly_am.add_hline(y=mean, line_width=3,
                         annotation_text="Average: "+str(int(round(mean, 0))), 
                         annotation_font_size=12,  annotation_bgcolor="white")


    return steps, corr_graph(dff, 'steps'), fairly_am, corr_graph(dff, 'fairly_active_minutes'), lightly_am, corr_graph(dff, 'lightly_active_minutes')