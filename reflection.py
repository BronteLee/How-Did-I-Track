import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
from datetime import date
import dash_bootstrap_components as dbc


def reflection_panel(questions):
    if questions is None:
        questions = ["What have I learnt?", "What will I do?"]
    return [
    dbc.Row(html.H3("My Reflections", className="reflection--heading")),
    dbc.Row(html.P(questions[0], className="reflection--question")),
    dbc.Row([
        dbc.Col(dcc.Textarea(
        id="text-learn",
        placeholder="I learnt ...",
        className="reflection--input"), style={"padding-right": "0"}, width=8),
        dbc.Col(html.Button("Add", id="confirm-learn", className="reflection--button"), className="reflection--buttoncol")
    ]),
    dbc.Row(html.Div(id="all-learn", className="reflection--text"), style={"padding-left":"9px", "padding-right":"5px", "padding-bottom":"10px"}),
    dbc.Row(html.Hr()),
    dbc.Row(html.P(questions[1], className="reflection--question")),
    dbc.Row([
        dbc.Col(dcc.Textarea(
        id="text-do",
        placeholder="I will ...",
        className="reflection--input"), style={"padding-right": "0"}, width=8),
        dbc.Col(html.Button("Add", id="confirm-do", className="reflection--button"), className="reflection--buttoncol")
    ]),
    dbc.Row(html.Div(id="all-do", className="reflection--text"), style={"padding-left":"9px", "padding-right":"5px", "padding-bottom":"10px"}),
    dbc.Row(dbc.NavLink("Edit and View My Reflections", href="/reflections", className="reflection--more"))
    ]