import pandas as pd
from datetime import date
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np

def make_hover_text(data, datatype):
    hover_text = []
    vals = []
    metrics = []
    if datatype != 'steps':
        vals.append(data[datatype]['steps'])
        metrics.append('steps')
    if datatype != 'fairly_active_minutes':
        vals.append(data[datatype]['fairly_active_minutes'])
        metrics.append('fairly_active_minutes')
    if datatype != 'lightly_active_minutes':
        vals.append(data[datatype]['lightly_active_minutes'])
        metrics.append('lightly_active_minutes')
    for i in ['calories', 'resting_heart_rate', 'minutes_asleep', 'minutes_awake']:
        vals.append(data[datatype][i])
        metrics.append(i)
    for k in range(0,len(vals)):
        text = "The higher your " + metrics[k].replace("_", " ")
        if vals[k] > 0:
            text += " the more "
        else:
            text += " the less "
        text += datatype.replace("_", " ")
        text += " you did"
        hover_text.append(text)
    #print("HOVER",hover_text)
    return hover_text

def get_index(datatype):
    index = 0
    if datatype == 'fairly_active_minutes':
        index = 1
    if datatype == 'lightly_active_minutes':
        index = 2
    return index

def x_labels(datatype):
    labels = ['Steps', 'Fairly Active Minutes', 'Lightly Active Minutes',
            'Calories', 'Resting Heart Rate', 'Minutes Asleep', 'Minutes Awake']
    if datatype == 'steps':
        labels.remove('Steps')
    if datatype == 'fairly_active_minutes':
        labels.remove('Fairly Active Minutes')
    if datatype == 'lightly_active_minutes':
        labels.remove('Lightly Active Minutes')
    return labels

def corr_graph(dff, datatype):
    data = dff[['steps', 'fairly_active_minutes', 'lightly_active_minutes',
            'calories', 'resting_heart_rate', 'minutes_asleep', 'minutes_awake']].corr(method="spearman")
    data = pd.DataFrame(data.iloc[get_index(datatype)]).drop([datatype])
    return go.Figure(
        data=go.Heatmap(
            z=data,
            x=x_labels(datatype),
            colorscale=[[0, "red"], [0.5, "white"], [1, "green"]],
            transpose=True,
            zmin= -1,
            zmax = 1,
            hovertemplate=("%{customdata}"),
            customdata=[make_hover_text(data, datatype)],
            colorbar=dict(
                tickmode="array",
                tickvals=[-1, 1],
                ticktext=["Negative Relationship", "Positive Relationship"]
            )
     ), layout=go.Layout(margin=go.layout.Margin(
            l=0,
            r=0,
            b=0,
            t=0
        ),
        yaxis=dict(visible= False),
        xaxis=dict(showline=True),
        height=145),
        )