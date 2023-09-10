import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
from datetime import date
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from newcal import create_heatmap
from reflection import reflection_panel
from correlationgraph import corr_graph

dash.register_page(__name__, path='/')

df = pd.read_json("data/daily-data.json", convert_dates=False)
df['date'] = pd.to_datetime(df['date'], dayfirst=True)



layout = dbc.Row([dbc.Col([
        dbc.Row(html.H1("Overview")),
        dbc.Row([
            dbc.Col(html.P("Select Year", style={"text-align":"right"})),
            dbc.Col(dcc.Dropdown(
                [2021, 2022, 2023],
                id="year_select",
                value=2023,
                clearable=False,
                style={"width": "10vw"},
            ))
        ]),
        dbc.Row(html.H3("My Steps")),
        dbc.Row(dcc.Loading(type="circle", children=dcc.Graph(
            id="cal_steps", config={'displayModeBar': False}))),
        dbc.Row(html.P("Contextual Factors")),
        dbc.Row(dcc.Loading(type="circle", children=dcc.Graph(
            id="context_steps", config={'displayModeBar': False}))),
        dbc.Row(html.H3("My Fairly Active Minutes")),  
        dbc.Row(dcc.Loading(type="circle",children=dcc.Graph(id="cal_fairly_AM", config={
        'displayModeBar': False}))),
        dbc.Row(html.P("Contextual Factors")),
        dbc.Row(dcc.Loading(type="circle", children=dcc.Graph(
            id="context_fairly_AM", config={'displayModeBar': False}))),
        dbc.Row(html.H3("My Lightly Active Minutes")),
        dbc.Row(dcc.Loading(type="circle", children=dcc.Graph(id="cal_lightly_AM", config={
        'displayModeBar': False}))),
        dbc.Row(html.P("Contextual Factors")),
        dbc.Row(dcc.Loading(type="circle", children=dcc.Graph(
            id="context_lightly_AM", config={'displayModeBar': False}))),
        ], width=9),
    dbc.Col(reflection_panel(None), width=3, className="reflection--panel")
    ],
    style={"padding-left": "10px", "max-width": "100%"}
)

@callback(
    Output(component_id="cal_steps", component_property="figure"),
    Output(component_id="context_steps", component_property="figure"),
    Output(component_id="cal_fairly_AM", component_property="figure"),
    Output(component_id="context_fairly_AM", component_property="figure"),
    Output(component_id="cal_lightly_AM", component_property="figure"),
    Output(component_id="context_lightly_AM", component_property="figure"),
    Input(component_id='year_select', component_property='value'),
)
def update_graph(value):
    start_date = date(value, 1, 1)
    end_date = date(value, 12, 31)
    dff = df.query("date >= @start_date & date <= @end_date")
    steps = create_heatmap('steps', dff, str(value))
    context_steps = corr_graph(dff, 'steps')
    fairly_AM = create_heatmap('fairly_active_minutes', dff, str(value))
    context_fairly_AM = corr_graph(dff, 'fairly_active_minutes')
    lightly_AM = create_heatmap('lightly_active_minutes', dff, str(value))
    context_lightly_AM = corr_graph(dff, 'lightly_active_minutes')
    return steps, context_steps, fairly_AM, context_fairly_AM, lightly_AM, context_lightly_AM
    #return steps, None, fairly_AM, None, lightly_AM, None
