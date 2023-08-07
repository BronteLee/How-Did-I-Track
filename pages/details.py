import dash
from dash import html, dcc, callback, Input, Output
import dash_daq as daq
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import date

df = pd.read_json('data/daily-data.json', convert_dates=False)
df['date'] = pd.to_datetime(df['date'], dayfirst=True)

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1("Details"),
    html.Div([
        html.H3("Date Range: ", style={'display': 'inline-block'}),
        dcc.DatePickerRange(
            id="date-picker",
            first_day_of_week=1,
            display_format="DD MMM YYYY",
            min_date_allowed=date(2017, 12, 23),
            max_date_allowed=date(2023, 7, 27),
            number_of_months_shown=3,
            start_date=date(2022, 1, 1),
            end_date=date(2022, 12, 31),
            style={'padding': '10px', 'display': 'inline-block'}
        ),
        html.Div(
            children=[
                html.H3(" Low Wear Threshold: "),
            dcc.Dropdown(
                [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],
                id="low-wear-dropdown",
                value=8,
                clearable=False
            ),
            daq.BooleanSwitch(
                id="low-wear-switch",
                on=False,
                label="Hide Low Wear Days",
                style={'display': 'inline-block'}
            ),
            ], style={'display':'inline-block'}
        ),
        html.Div(id="date-error", style={'color':'red', 'display' : 'inline-block'})
    ], style={'display': 'inline-block'}),
    html.H3(children="My Steps"),
    dcc.Graph(id="steps", config={
        'displayModeBar': False}),
    html.H3(children="My Fairly Active Minutes"),
    dcc.Graph(id="fairly-am", config={
        'displayModeBar': False}),
    html.H3(children="My Lightly Active Minutes"),
    dcc.Graph(id="lightly-am", config={
        'displayModeBar': False}),
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
    Output(component_id="date-error", component_property="children"),
    Output(component_id="steps", component_property="figure"),
    Output(component_id="fairly-am", component_property="figure"),
    Output(component_id="lightly-am", component_property="figure"),
    Input(component_id='low-wear-switch', component_property='on'),
    Input(component_id='date-picker', component_property='start_date'),
    Input(component_id='date-picker', component_property='end_date'),
    Input(component_id='low-wear-dropdown', component_property='value')
)
def update_graph(on, start_date, end_date, value):
    dff = df
    date_error = ""
    if start_date > end_date:
        date_error = "Please select end date on or after " + str(start_date)
    else:
        date_error = ""
        dff = df.query("date > @start_date & date < @end_date")
    if on is True:
        dff = dff.query("hours_worn >= @value")
    steps = go.Figure(data=[go.Bar(
        x=dff['date'], y=dff['steps'],
        marker_color=adherence_colour(dff, value)
    )])
    steps.update_xaxes(title_text="Date", title_font={"size": 16})
    steps.update_yaxes(title_text="Steps", title_font={"size": 16})
    mean = np.mean(dff['steps'])
    steps.add_hline(y=mean, annotation_text="Average: "+str(int(round(mean, 0))), annotation_font_size=20)

    fairly_am = go.Figure(data=[go.Bar(
        x=dff['date'], y=dff['fairly_active_minutes'],
        marker_color=adherence_colour(dff, value)
    )])
    fairly_am.update_xaxes(title_text="Date", title_font={"size": 16})
    fairly_am.update_yaxes(title_text="Fairly Active Minutes", title_font={"size": 16})
    mean = np.mean(dff['fairly_active_minutes'])
    fairly_am.add_hline(y=mean, annotation_text="Average: "+str(int(round(mean, 0))), annotation_font_size=20)

    lightly_am = go.Figure(data=[go.Bar(
        x=dff['date'], y=dff['lightly_active_minutes'],
        marker_color=adherence_colour(dff, value)
    )])
    lightly_am.update_xaxes(title_text="Date", title_font={"size": 16})
    lightly_am.update_yaxes(title_text="Lightly Active Minutes", title_font={"size": 16})
    mean = np.mean(dff['lightly_active_minutes'])
    lightly_am.add_hline(y=mean, annotation_text="Average: "+str(int(round(mean, 0))), annotation_font_size=20)


    return date_error, steps, fairly_am, lightly_am