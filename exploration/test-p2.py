from datetime import date
from dash import Dash, html, dcc, callback, Output, Input
import dash_daq as daq
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

df = pd.read_json('data/daily-data.json', convert_dates=False)
df['date'] = pd.to_datetime(df['date'], dayfirst=True)

app = Dash(__name__)

app.layout = html.Div([
    html.H2(children='How Did I Track?'),
    html.Hr(),
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
                #style={'width': '80px','padding': '10px', 'display': 'inline-block'}
                #style={'width':'100%', 'display': 'inline-block'}
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
    html.H2(children="Steps"),
    dcc.Graph(id="steps"),
    html.H2(children="Adherence"),
    dcc.Graph(id="graph3"),
])

def adherence_colour(df, min_wear):
    vals = df['hours_worn'].tolist()
    colours = []
    for i in vals:
        if i < min_wear:
            colours.append("red")
        else:
            colours.append("orange")
    return colours

@callback(
    Output(component_id="date-error", component_property="children"),
    Output(component_id="steps", component_property="figure"),
    Output(component_id="graph3", component_property="figure"),
    Input(component_id='low-wear-switch', component_property='on'),
    Input(component_id='date-picker', component_property='start_date'),
    Input(component_id='date-picker', component_property='end_date'),
    Input(component_id='low-wear-dropdown', component_property='value')
)
def update_graph(on, start_date, end_date, value):
    dff = df
    date_error = ""
    print("S", str(start_date), "F", str(end_date), type(start_date))
    if start_date > end_date:
    #if date.strptime(start_date, "%Y/%m/%d") > date.strptime(end_date, "%Y/%m/%d"):
        date_error = "Please select end date on or after " + str(start_date)
    else:
        date_error = ""
        dff = df.query("date > @start_date & date < @end_date")
    if on is True:
        dff = dff.query("hours_worn >= @value")
    graph = go.Figure(data=[go.Bar(
        x=dff['date'], y=dff['steps'],
        marker_color=adherence_colour(dff, value)
    )])
    graph.update_xaxes(title_text="Date", title_font={"size": 16})
    graph.update_yaxes(title_text="Steps", title_font={"size": 16})
    #graph = px.bar(dff, x="date", y="steps", labels={"date": "Date", "steps": "Steps"})
    mean = np.mean(dff['steps'])
    graph.add_hline(y=mean, annotation_text="Average: "+str(int(round(mean, 0))), annotation_font_size=20)
    #graph.update_traces()

    graph3 = px.bar(dff, x="date", y="hours_worn", labels={"date": "Date", "hours_worn": "Hours Worn"})
    mean3 = np.mean(dff['hours_worn'])
    graph3.add_hline(y=mean3, annotation_text="Average: "+str(int(round(mean3, 0))), annotation_font_size=20)
    graph3.update_traces(marker_color="orange")

    return date_error, graph, graph3


if __name__ == '__main__':
    app.run(debug=True)
