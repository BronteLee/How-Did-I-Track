from datetime import date
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np

# data
df = pd.read_json('daily-data.json', convert_dates=False)
df['date'] = pd.to_datetime(df['date'], dayfirst=True)

df1 = pd.read_json('moderately-active-minutes-merged.json')
df1['dateTime'] = pd.to_datetime(df1['dateTime'], format="%m/%d/%Y")
df2 = pd.read_json('lightly-active-minutes-merged.json')
df2['dateTime'] = pd.to_datetime(df2['dateTime'], format="%m/%d/%Y")

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='How Did I Track?'),
    html.Hr(),
    html.Div(["Date Range: ",
              dcc.DatePickerRange(
                  id="date-picker",
                  first_day_of_week=1,
                  display_format="DD MMM YYYY",
                  min_date_allowed=date(2017, 12, 23),
                  max_date_allowed=date(2023, 7, 21),
                  number_of_months_shown=4,
                  start_date=date(2022, 1, 1),
                  end_date=date(2022, 12, 31)
              )], style={'display': 'inline-block'}),
    html.H2(children="Steps"),
    dcc.Graph(id="graph"),
    html.H2(children='Moderately Active Minutes'),
    dcc.Graph(id='graph1'),
    html.H2(children='Lightly Active Minutes'),
    dcc.Graph(id='graph2'),
    html.H2(children="Adherence"),
    dcc.Graph(id="graph3")
])


@callback(
    Output(component_id="graph", component_property="figure"),
    Output(component_id="graph1", component_property="figure"),
    Output(component_id="graph2", component_property="figure"),
    Output(component_id="graph3", component_property="figure"),
    Input(component_id='date-picker', component_property='start_date'),
    Input(component_id='date-picker', component_property='end_date')
)
def update_graph(start_date, end_date):
    dff = df.query("date > @start_date & date < @end_date")
    graph = px.bar(dff, x="date", y="steps", labels={"date": "Date", "steps": "Steps"})
    mean = np.mean(dff['steps'])
    graph.add_hline(y=mean, annotation_text="Average: "+str(int(round(mean, 0))), annotation_font_size=20)
    graph.update_traces(marker_color="orange")

    dff1 = df1.query("dateTime > @start_date & dateTime < @end_date")
    graph1 = px.bar(dff1, x="dateTime", y="value", labels={"dateTime": "Date", "value": "Minutes"})
    mean1 = np.mean(dff1['value'])
    graph1.add_hline(y=mean1, annotation_text="Average: "+str(int(round(mean1, 0))), annotation_font_size=20)
    graph1.update_traces(marker_color="orange")

    dff2 = df2.query("dateTime > @start_date & dateTime < @end_date")
    graph2 = px.bar(dff2, x="dateTime", y="value", labels={"dateTime": "Date", "value": "Minutes"})
    mean2 = np.mean(dff2['value'])
    graph2.add_hline(y=mean2, annotation_text="Average: "+str(int(round(mean2, 0))), annotation_font_size=20)
    graph2.update_traces(marker_color="orange")

    dff3 = df.query("date > @start_date & date < @end_date")
    graph3 = px.bar(dff3, x="date", y="hours-worn", labels={"date": "Date", "hours-worn": "Hours Worn"})
    mean3 = np.mean(dff3['hours-worn'])
    graph3.add_hline(y=mean3, annotation_text="Average: "+str(int(round(mean3, 0))), annotation_font_size=20)
    graph3.update_traces(marker_color="orange")

    return graph, graph1, graph2, graph3


if __name__ == '__main__':
    app.run(debug=True)
