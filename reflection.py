import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
from datetime import date
import dash_bootstrap_components as dbc


def reflection_panel():
    return [
    dbc.Row(html.H3("My Reflections", className="reflection--heading")),
    dbc.Row(html.P("What have I learnt?", className="reflection-question")),
    dbc.Row(dcc.Textarea(
        id="text-learn",
        placeholder="I learnt ...",
        style={"width":"90%", "margin": "auto"})),
    dbc.Row(html.Button("Add", id="confirm-learn", className="reflection--button"), style={"padding": "10px"}),
    dbc.Row(html.P(id="all-learn")),
    dbc.Row(html.Hr()),
    dbc.Row(html.P("What will I do?", className="reflection-question")),
    dbc.Row(dcc.Textarea(
        id="text-do",
        placeholder="I will ...",
        style={"width":"90%", "margin": "auto"})),
    dbc.Row(html.Button("Add", id="confirm-do", className="reflection--button"), style={"padding": "10px"}),
    dbc.Row(html.P(id="all-do"))
    ]