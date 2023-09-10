import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import json
import numpy as np

dash.register_page(__name__, path="/prompt")

prompt_pages = {}

data = json.load(open("data/test.json", encoding='utf-8'))
for entry in data: 
    prompt_type = entry['type']
    complete = 1 if entry['complete'] == 'True' else 0
    if prompt_type in prompt_pages:
        prompt_pages[prompt_type]['total'] += 1
        prompt_pages[prompt_type]['complete'] += complete
        if prompt_pages[prompt_type]["prompt"] == 0 and complete == 0:
            prompt_pages[prompt_type]["prompt"] = entry['id']
    else:
        prompt_pages[prompt_type] = {"complete": complete, "total": 1}
        if complete == 0:
            prompt_pages[prompt_type]["prompt"] = entry['id']
        else:
            prompt_pages[prompt_type]["prompt"] = 0
    if "total" in prompt_pages:
        prompt_pages['total']['complete'] += complete
        prompt_pages['total']['total'] += 1
    else:
        prompt_pages['total'] = {"complete": complete, "total": 1}
    if complete == 0 and "prompt" not in prompt_pages[prompt_type]:
        prompt_pages[prompt_type]['prompt'] = entry['id']
for page in prompt_pages:
    prompt_page = prompt_pages[page]
    prompt_page['percentage'] = round((prompt_page['complete']/prompt_page['total'])*100)
prompt_pages['total']['prompt'] = np.random.choice(
            np.array([prompt_pages['steps']['prompt'], prompt_pages['lightly_active_minutes']['prompt'], 
                      prompt_pages['fairly_active_minutes']['prompt'], prompt_pages['missing_data']['prompt']]))
#print(prompt_pages)

layout = dbc.Row([dbc.Col([
    dbc.Row(html.H1("Prompt")),
    dbc.Row(html.P("""How-Did-I-Track? has analysed your data and found periods of the highest and lowest 
                   physical activity, trends, and gaps in your data. Prompts for these periods have been 
                   created to help you to understand and reflect on your physical activity""", 
                   className="prompts--text"), style={"width": "70%", "margin": "auto"}),
    dbc.Row([
        dbc.Col(html.H3("Total Progress", className="prompts--heading"), width=5),
        dbc.Col(dbc.Progress(value=prompt_pages['total']['percentage'], color="info"), width=3),
        dbc.Col(html.P(str(prompt_pages['total']['percentage'])+"%"), width=1),
        dbc.Col(dbc.NavLink("Random Prompt", href="/prompt/"+str(prompt_pages['total']['prompt']),
            className="prompts--button"), width=3),
    ], className="prompts--row"),
    dbc.Row([
        dbc.Col(html.H3("Steps", className="prompts--heading"), width=5),
        dbc.Col(dbc.Progress(value=prompt_pages['steps']['percentage'], 
                             color="info"), width=3),
        dbc.Col(html.P(str(prompt_pages['steps']['percentage'])+"%"), width=1),
        dbc.Col(dbc.NavLink("Steps Prompt", href="/prompt/"+str(prompt_pages['steps']['prompt']), 
            className="prompts--button"), width=3),
    ], className="prompts--row"),
    dbc.Row([
        dbc.Col(html.H3("Fairly Active Minutes", className="prompts--heading"), width=5),
        dbc.Col(dbc.Progress(value=prompt_pages['fairly_active_minutes']['percentage'], color="info"), width=3),
        dbc.Col(html.P(str(prompt_pages['fairly_active_minutes']['percentage'])+"%"), width=1),
        dbc.Col(dbc.NavLink("Fairly Active Minutes Prompt", href="/prompt/"+str(prompt_pages['fairly_active_minutes']['prompt']), 
            className="prompts--button"), width=3),
    ], className="prompts--row"),
    dbc.Row([
        dbc.Col(html.H3("Lightly Active Minutes", className="prompts--heading"), width=5),
        dbc.Col(dbc.Progress(value=prompt_pages['lightly_active_minutes']['percentage'], color="info"), width=3),
        dbc.Col(html.P(str(prompt_pages['lightly_active_minutes']['percentage'])+"%"), width=1),
        dbc.Col(dbc.NavLink("Lightly Active Minutes Prompt", href="/prompt/"+str(prompt_pages['lightly_active_minutes']['prompt']), 
            className="prompts--button"), width=3),
    ], className="prompts--row"),
    dbc.Row([
        dbc.Col(html.H3("Missing Data", className="prompts--heading"), width=5),
        dbc.Col(dbc.Progress(value=prompt_pages['missing_data']['percentage'], color="info"), width=3),
        dbc.Col(html.P(str(prompt_pages['missing_data']['percentage'])+"%"), width=1),
        dbc.Col(dbc.NavLink("Missing Data Prompt", href="/prompt/"+str(prompt_pages['missing_data']['prompt']), className="prompts--button"), width=3),
    ], className="prompts--row"),
])], style={"padding-left": "10px", "max-width": "100%", "padding": "20px"})
