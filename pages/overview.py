import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
from plotly_calplot import calplot
from datetime import date
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/')

df = pd.read_json("data/daily-data-2.json", convert_dates=False)
df['date'] = pd.to_datetime(df['date'], dayfirst=True)

reflections = [
    dbc.Row(html.H3("My Reflections")),
    dbc.Row(html.P("What have I learnt?")),
    dbc.Row(dcc.Textarea(
        id="text-learn",
        placeholder="I learnt ...",
        style={"width":"90%", "margin": "auto"})),
    dbc.Row(html.Button("Add", id="confirm-learn", style={"width":"50%", "margin": "auto"})),
    dbc.Row(html.P(id="all-learn")),
    dbc.Row(html.P("What will I do?")),
    dbc.Row(dcc.Textarea(
        id="text-do",
        placeholder="I will ...",
        style={"width":"90%", "margin": "auto"})),
    dbc.Row(html.Button("Add", id="confirm-do", style={"width":"50%", "margin": "auto"})),
    dbc.Row(html.P(id="all-do"))
    ]

layout = dbc.Row([dbc.Col([
        dbc.Row(html.H1("Overview")),
        dbc.Row([
            dbc.Col(html.P("Select Year")),
            dbc.Col(dcc.Dropdown(
                [2017, 2018, 2019, 2020, 2021, 2022, 2023],
                id="year_select",
                value=2023,
                clearable=False,
                style={"width": "40%", "padding-left": "10%"},
            ))
        ]),
        dbc.Row(html.H3("My Steps")),
        dbc.Row(dcc.Loading(type="circle", children=dcc.Graph(
            id="cal_steps", config={'displayModeBar': False}))),
        dbc.Row(html.P("Contextual Factors")),
        dbc.Row(html.H3("My Fairly Active Minutes")),  
        dbc.Row(dcc.Loading(type="circle",children=dcc.Graph(id="cal_fairly_AM", config={
        'displayModeBar': False}))),
                dbc.Row(html.P("Contextual Factors")),
        dbc.Row(html.H3("My Lightly Active Minutes")),
        dbc.Row(dcc.Loading(type="circle", children=dcc.Graph(id="cal_lightly_AM", config={
        'displayModeBar': False}))),
        dbc.Row(html.P("Contextual Factors")),
        ], width=9),
    dbc.Col(reflections, width=3, style={"position": "fixed", "right": "0"})
    ],
    style={"padding-left": "10px", "max-width": "100%"}
)

@callback(
    Output(component_id="cal_steps", component_property="figure"),
    Output(component_id="cal_fairly_AM", component_property="figure"),
    Output(component_id="cal_lightly_AM", component_property="figure"),
    Input(component_id='year_select', component_property='value'),
)
def update_graph(value):
    start_date = date(value, 1, 1)
    end_date = date(value, 12, 31)
    dff = df.query("date >= @start_date & date <= @end_date")
    steps = calplot(
        dff,
        x='date',
        y='steps',
        gap=2,
        colorscale=[[0.0, "#e9e6eb"], [0.001, "#e9cffc"], [0.2, "#eeaaff"],[0.4, "#dd88ee"], [0.6, "#aa66cc"], [0.8, "#7744aa"], [1.0, "#442255"]],
        showscale=True,
        text="hours_worn",
        month_lines_width=2,
        month_lines_color="black",
    )
    fairly_AM = calplot(
        dff,
        x='date',
        y='fairly_active_minutes',
        gap=2,
        colorscale=[[0.0, "#e9e6eb"], [0.001, "#e9cffc"], [0.2, "#eeaaff"],[0.4, "#dd88ee"], [0.6, "#aa66cc"], [0.8, "#7744aa"], [1.0, "#442255"]],
        showscale=True,
        text="hours_worn",
        month_lines_width=2,
        month_lines_color="black",
    )
    lightly_AM = calplot(
        dff,
        x='date',
        y='lightly_active_minutes',
        gap=2,
        colorscale=[[0.0, "#e9e6eb"], [0.001, "#e9cffc"], [0.2, "#eeaaff"],[0.4, "#dd88ee"], [0.6, "#aa66cc"], [0.8, "#7744aa"], [1.0, "#442255"]],
        showscale=True,
        text="hours_worn",
        month_lines_width=2,
        month_lines_color="black",
    )
    return steps, fairly_AM, lightly_AM
