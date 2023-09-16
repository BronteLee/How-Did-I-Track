import dash
from dash import html, dcc, Input, Output, callback
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import numpy as np
import dash_bootstrap_components as dbc
from reflection import reflection_panel
from correlationgraph import corr_graph
import sqlite3

dash.register_page(__name__, path_template="/prompt/<prompt_id>")

padf = pd.read_json("data/eval-daily-data.json", convert_dates=False)
padf['date'] = pd.to_datetime(padf['date'], dayfirst=True)

def graph_label(value):
    if value == "lightly_active_minutes":
        return "Lightly Active Minutes"
    if value == "fairly_active_minutes":
        return "Fairly Active Minutes"
    else:
        return "Steps"

def adherence_colour(df, min_wear):
    vals = df['hours_worn'].tolist()
    colours = []
    for i in vals:
        if i < min_wear:
            colours.append("orange")
        else:
            colours.append("blueviolet")
    return colours

def make_figure(padff, type):
    graph_layout = go.Layout(
    margin=go.layout.Margin(
        l=0,
        r=0,
        b=0,
        t=0
    ), height=300
    )
    graph = go.Figure(data=[go.Bar(
        x=padff['date'], y=padff[type if type != "missing_data" else "steps"],
        marker_color=adherence_colour(padff, 10)
    )], layout=graph_layout)
    graph.update_xaxes(title_text="Date", title_font={"size": 16})
    graph.update_yaxes(title_text=graph_label(type), title_font={"size": 16})
    mean = np.mean(padff[type if type != "missing_data" else "steps"])
    graph.add_hline(y=mean, annotation_text="Average: "+str(int(round(mean, 0))), annotation_font_size=20)
    return graph

def layout(prompt_id):
    prompt_con = sqlite3.connect('data/reflecting.db')
    prompt_cur = prompt_con.cursor()
    prompt = prompt_cur.execute("SELECT * FROM prompts WHERE prompt_id = ?", (prompt_id,)).fetchone()
    prev = prompt_cur.execute("SELECT prompt_id FROM prompts WHERE type = ? and prompt_id < ? ORDER BY prompt_id DESC", (prompt[1], prompt_id)).fetchone()
    next = prompt_cur.execute("SELECT prompt_id FROM prompts WHERE type = ? and prompt_id > ? ORDER BY prompt_id ASC", (prompt[1], prompt_id)).fetchone()
    prompt_con.close()
    prompt = list(prompt)
    prev = -1 if prev is None else prev[0]
    next = -1 if next is None else next[0]
    start_date = datetime.strptime(prompt[3], "%d/%m/%Y")
    end_date = datetime.strptime(prompt[4], "%d/%m/%Y")
    padff = padf.query("date >= @start_date & date <= @end_date")
    if prompt[1] == 'missing_data':
        prompt[1] = 'steps'
    return dbc.Row([dbc.Col([
        dbc.Row(html.H1("Prompt")),
        dbc.Row([dbc.Col(html.H3(prompt[5]), width=8), 
                 dbc.Col(dbc.NavLink("Prev", href="/prompt/"+str(prev), disabled=(True if prev == -1 else False), className="prompt--buttons")),
                 dbc.Col(dbc.NavLink("Next", href="/prompt/"+str(next), disabled=(True if next == -1 else False), className="prompt--buttons")),
                 dbc.Col(html.Button(id="button_complete", className="prompt--complete"))]),
        dbc.Row(html.P(f"Date Range: {start_date.strftime('%d %b %Y')} to {end_date.strftime('%d %b %Y')}")),
        dbc.Row(html.P(prompt[6])),
        dbc.Row(html.H4(graph_label(prompt[1]))),
        dbc.Row(dcc.Graph(id="prompt graph", figure=make_figure(padff, prompt[1]), 
            config={'displayModeBar': False})),
        dbc.Row(html.P("Contextual Factors")),
        dbc.Row(dcc.Graph(id="prompt-correlations", figure=corr_graph(padff, prompt[1]), config={'displayModeBar': False})),
        dbc.Row(html.H4("Questions")),
        dbc.Row(html.P(prompt[7])),
        dbc.Row(html.P(prompt[8])),
        dbc.Row(dcc.Store(id='prompt_id', data=prompt_id))
        ], width=9),
        dbc.Col(reflection_panel(None), width=3, className="reflection--panel")
        ], style={"padding-left": "10px", "max-width": "100%"})

@callback(
    Output('button_complete', 'children'),
    Output('button_complete', 'style'),
    Input('button_complete', 'n_clicks'),
    Input('prompt_id', 'data')
)
def complete_button(n, prompt_id):
    complete_con = sqlite3.connect('data/reflecting.db')
    complete_cur = complete_con.cursor()
    new_title = ""
    style = {}
    current = complete_cur.execute("SELECT complete FROM prompts WHERE prompt_id = ?", (int(prompt_id),)).fetchone()[0]
    if n:
        if current == 0:
            complete_cur.execute("UPDATE prompts SET complete = 1 WHERE prompt_id = ?", (int(prompt_id),))
            new_title = "Completed!"
            style['background-color'] = "rgb(49, 176, 49)"
        else:
            complete_cur.execute("UPDATE prompts SET complete = 0 WHERE prompt_id = ?", (int(prompt_id),))
            new_title = "Mark Complete"
            style['background-color'] = "sandybrown"
            style['color'] = "black"
    else:
        if current == 0:
           new_title = "Mark Complete"
           style['background-color'] = "sandybrown"
           style['color'] = "black"
        else:
            new_title = "Completed!"
            style['background-color'] = "rgb(49, 176, 49)"
    complete_con.commit()
    complete_cur.close()
    return new_title, style