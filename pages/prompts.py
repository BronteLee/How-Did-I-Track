import dash
from dash import html, dcc
import dash_bootstrap_components as dbc


dash.register_page(__name__, path="/prompt")

layout = html.Div(children=[
    html.H1("Prompt"),
    html.P("""Prompts provide guided analysis to help understand and reflect 
           on your physical activity"""),
    html.H3("Total Progress"),
    dbc.Progress(value=20, color="info")
])
