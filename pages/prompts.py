import dash
from dash import html, dcc
import dash_bootstrap_components as dbc


dash.register_page(__name__, path="/prompt")

layout = dbc.Row([dbc.Col([
    dbc.Row(html.H1("Prompt")),
    dbc.Row(html.P("""How-Did-I-Track? has analysed your data and found periods of the highest and lowest 
                   physical activity, trends, and gaps in your data. Prompts for these periods have been 
                   created to help you to understand and reflect on your physical activity""", className="prompt--text"), style={"width": "70%", "margin": "auto"}),
    dbc.Row([
        dbc.Col(html.H3("Total Progress", className="prompt--heading"), width=5),
        dbc.Col(dbc.Progress(value=20, color="info"), width=3),
        dbc.Col(html.P("20%"), width=1),
        dbc.Col(dbc.NavLink("Random Prompt", href="/prompt/1",
            className="prompt--button"), width=3),
    ], className="prompt--row"),
    dbc.Row([
        dbc.Col(html.H3("Steps", className="prompt--heading"), width=5),
        dbc.Col(dbc.Progress(value=50, color="info"), width=3),
        dbc.Col(html.P("50%"), width=1),
        dbc.Col(dbc.NavLink("Steps Prompt", href="/prompt/1", 
            className="prompt--button"), width=3),
    ], className="prompt--row"),
    dbc.Row([
        dbc.Col(html.H3("Fairly Active Minutes", className="prompt--heading"), width=5),
        dbc.Col(dbc.Progress(value=75, color="info"), width=3),
        dbc.Col(html.P("75%"), width=1),
        dbc.Col(dbc.NavLink("Fairly Active Minutes Prompt", href="/prompt/2", 
            className="prompt--button"), width=3),
    ], className="prompt--row"),
    dbc.Row([
        dbc.Col(html.H3("Lightly Active Minutes", className="prompt--heading"), width=5),
        dbc.Col(dbc.Progress(value=20, color="info"), width=3),
        dbc.Col(html.P("20%"), width=1),
        dbc.Col(dbc.NavLink("Lightly Active Minutes Prompt", href="/prompt/1", 
            className="prompt--button"), width=3),
    ], className="prompt--row"),
    dbc.Row([
        dbc.Col(html.H3("Missing Data", className="prompt--heading"), width=5),
        dbc.Col(dbc.Progress(value=20, color="info"), width=3),
        dbc.Col(html.P("20%"), width=1),
        dbc.Col(dbc.NavLink("Missing Data Prompt", href="/prompt/1", className="prompt--button"), width=3),
    ], className="prompt--row"),
])], style={"padding-left": "10px", "max-width": "100%", "padding": "20px"})
