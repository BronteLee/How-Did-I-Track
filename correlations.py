from dash import Dash, dash, html, dcc
import pandas as pd
from datetime import date
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

app = Dash(__name__)

df = pd.read_json("data/daily-data.json", convert_dates=False)
df['date'] = pd.to_datetime(df['date'], dayfirst=True)
start_date = date(2022, 1, 1)
end_date = date(2022, 12, 31)
dff = df.query("date >= @start_date & date <= @end_date")

def adherence_colour(df, min_wear):
    vals = df['hours_worn'].tolist()
    colours = []
    for i in vals:
        if i < min_wear:
            colours.append("orange")
        else:
            colours.append("blueviolet")
    return colours

def make_bar(dff):
    graph_layout = go.Layout(
    margin=go.layout.Margin(
        l=0,
        r=0,
        b=0,
        t=0
    ), height=300
    )
    graph = go.Figure(data=[go.Bar(
        x=dff['date'], y=dff['steps'],
        marker_color=adherence_colour(dff, 10)
    )], layout=graph_layout)
    graph.update_xaxes(title_text="Date", title_font={"size": 16})
    graph.update_yaxes(title_text="Steps", title_font={"size": 16})
    mean = np.mean(dff['steps'])
    graph.add_hline(y=mean, annotation_text="Average: "+str(int(round(mean, 0))), annotation_font_size=20)
    return graph

app.layout = html.Div(children=[
    html.H1("Steps"),
    dcc.Graph(figure=make_bar(dff)),
    html.H3("Calories"),
    dcc.Graph(figure=px.scatter(x=dff['steps'], y=dff['calories'])),
    html.H3("Minutes Asleep"),
    dcc.Graph(figure=px.scatter(x=dff['steps'], y=dff['minutes_asleep'])),
    html.H3("Minutes Awake"),
    dcc.Graph(figure=px.scatter(x=dff['steps'], y=dff['minutes_awake'])),
    html.H3("Lightly Active Minutes"),
    dcc.Graph(figure=px.scatter(x=dff['steps'], y=dff['lightly_active_minutes'])),
    html.H3("Fairly Active Minutes"),
    dcc.Graph(figure=px.scatter(x=dff['steps'], y=dff['fairly_active_minutes'])),
    html.H3("Resting Heat Rate"),
    dcc.Graph(figure=px.scatter(x=dff['steps'], y=dff['resting_heart_rate'])),
    html.H1("Lightly Active Minutes"),
    html.H3("Calories"),
    dcc.Graph(figure=px.scatter(x=dff['lightly_active_minutes'], y=dff['calories'])),
    html.H3("Minutes Asleep"),
    dcc.Graph(figure=px.scatter(x=dff['lightly_active_minutes'], y=dff['minutes_asleep'])),
    html.H3("Minutes Awake"),
    dcc.Graph(figure=px.scatter(x=dff['lightly_active_minutes'], y=dff['minutes_awake'])),
    html.H3("Steps"),
    dcc.Graph(figure=px.scatter(x=dff['lightly_active_minutes'], y=dff['steps'])),
    html.H3("Fairly Active Minutes"),
    dcc.Graph(figure=px.scatter(x=dff['lightly_active_minutes'], y=dff['fairly_active_minutes'])),
    html.H3("Resting Heat Rate"),
    dcc.Graph(figure=px.scatter(x=dff['lightly_active_minutes'], y=dff['resting_heart_rate'])),
    html.H1("Fairly Active Minutes"),
    html.H3("Calories"),
    dcc.Graph(figure=px.scatter(x=dff['fairly_active_minutes'], y=dff['calories'])),
    html.H3("Minutes Asleep"),
    dcc.Graph(figure=px.scatter(x=dff['fairly_active_minutes'], y=dff['minutes_asleep'])),
    html.H3("Minutes Awake"),
    dcc.Graph(figure=px.scatter(x=dff['fairly_active_minutes'], y=dff['minutes_awake'])),
    html.H3("Steps"),
    dcc.Graph(figure=px.scatter(x=dff['fairly_active_minutes'], y=dff['steps'])),
    html.H3("Lightly Active Minutes"),
    dcc.Graph(figure=px.scatter(x=dff['fairly_active_minutes'], y=dff['lightly_active_minutes'])),
    html.H3("Resting Heat Rate"),
    dcc.Graph(figure=px.scatter(x=dff['fairly_active_minutes'], y=dff['resting_heart_rate']))
])

if __name__ == '__main__':
    app.run(debug=True)