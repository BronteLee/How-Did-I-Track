import pandas as pd
from plotly_calplot.date_extractors import get_date_coordinates
from plotly_calplot.layout_formatter import create_month_lines
from datetime import date
import plotly.graph_objects as go
import numpy as np

def val_to_text(val):
    if val == "steps":
        return "Steps"
    if val == "fairly_active_minutes":
        return "Fairly Active Minutes"
    else:
        return "Lightly Active Minutes"

def make_hover_text(dff, datatype):
    hover_text = []
    for i in dff.index:
        if dff['hours_worn'][i] != dff['hours_worn'][i]:
            hover_text.append(f"Date: {dff['date'][i].strftime('%d/%m/%Y')}<br>No Data")
        elif dff['hours_worn'][i] == 0:
            hover_text.append(f"Date: {dff['date'][i].strftime('%d/%m/%Y')}<br>Tracker not worn")
        else:
            hover_text.append(f"Date: {dff['date'][i].strftime('%d/%m/%Y')}<br>{val_to_text(datatype)}: {int(dff[datatype][i])}<br>Hours Worn: {dff['hours_worn'][i]}")
    return hover_text
    

def custom_heatmap(dff, datatype, year, weekdays_in_year, 
                   weeknumber_of_dates, month_names, month_positions
):
    wear = dff['hours_worn'].tolist()
    heatmap = go.Figure(data=go.Heatmap(
            x = weeknumber_of_dates,
            y = weekdays_in_year,
            z = dff[datatype],
            xgap= 2,
            ygap= 2,
            colorscale=[[0, "white"], [0.25, "rgb(255, 221, 193)"], [0.5, "rgb(255, 143, 57)"], [0.75, "rgb(255,111,0)"], [1, "rgb(208,90,0)"]],
            text=wear,
            hovertemplate=("%{customdata}"),
            customdata=make_hover_text(dff, datatype),
            name=year
    ), layout=make_layout(month_names, month_positions))
    kwargs = dict(
        mode="lines",
        line=dict(color="black", width=2),
        hoverinfo="skip",
    )
    for date, dow, wkn in zip(dff['date'], weekdays_in_year, weeknumber_of_dates):
        if date.day == 1:
            heatmap.add_trace(go.Scatter(x=[wkn - 0.5, wkn - 0.5], y=[dow - 0.5, 6.5], **kwargs))
            if dow:
                heatmap.add_trace(
                    go.Scatter(
                        x=[wkn - 0.5, wkn + 0.5], y=[dow - 0.5, dow - 0.5], **kwargs))
                heatmap.add_trace(go.Scatter(x=[wkn + 0.5, wkn + 0.5], y=[dow - 0.5, - 0.5], **kwargs))
    return heatmap
    
def make_layout(month_names, month_positions):
    return go.Layout(
        margin=go.layout.Margin(
            l=0,
            r=0,
            b=0,
            t=0
        ),
        title="",
        plot_bgcolor="rgb(211,211,211)",
        showlegend=False,
        height=150,
        yaxis=dict(
                showline=False,
                showgrid=False,
                zeroline=False,
                tickmode="array",
                ticktext=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                tickvals=[0, 1, 2, 3, 4, 5, 6],
                autorange="reversed",
            ),
        xaxis=dict(
                showline=False,
                showgrid=False,
                zeroline=False,
                tickmode="array",
                ticktext=month_names,
                tickvals=month_positions,
            )
    )

def create_heatmap(datatype, dff, year) -> go.Figure:
    first_date = date(year=int(year), month=1, day=1)
    last_date = date(year=int(year), month=12, day=31)
    all_year = pd.DataFrame({'date': pd.date_range(first_date, last_date)})
    dff = all_year.merge(dff, on='date', how="left")
    for i in dff.index:
        if dff['hours_worn'][i] == 0:
            dff.loc[i, [datatype]] = np.nan
    month_names = []
    for i in range (1, 13):
        month_date = date(2023, i, 1)
        month_names.append(month_date.strftime('%B'))
    month_positions, weekdays_in_year, weeknumber_of_dates = get_date_coordinates(
    dff, 'date', 1, 12)
    #return go.Figure(data=custom_heatmap(dff, datatype, year, weekdays_in_year, weeknumber_of_dates), layout=make_layout(month_names, month_positions))
    return custom_heatmap(dff, datatype, year, weekdays_in_year, weeknumber_of_dates, month_names, month_positions)
