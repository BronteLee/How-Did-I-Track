import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc, callback, Input, Output
import pandas as pd
from datetime import date
from reflection import reflection_panel
from correlation_graph import corr_graph
from bar_graph import make_bar_graph


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
            minDate=date(2022,1,1),
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
def update_details(on, dates, value):
    start_date = date.fromisoformat(dates[0])
    end_date = date.fromisoformat(dates[1])
    dff = df.query("date >= @start_date & date <= @end_date")
    if not on:
        dff = dff.query("hours_worn >= @value")
    steps = make_bar_graph(dff, 'steps', value)
    fairly_am = make_bar_graph(dff, 'fairly_active_minutes', value)
    lightly_am = make_bar_graph(dff, 'lightly_active_minutes', value)

    return steps, corr_graph(dff, 'steps'), fairly_am, corr_graph(dff, 'fairly_active_minutes'), lightly_am, corr_graph(dff, 'lightly_active_minutes')