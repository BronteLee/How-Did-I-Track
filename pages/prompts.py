import dash
import dash_bootstrap_components as dbc
import numpy as np
import sqlite3
from dash import html

dash.register_page(__name__, path="/prompt")

def layout():
    con = sqlite3.connect('data/reflecting.db')
    cur = con.cursor()
    prompt_pages = {}
    prompt_options = []
    for entry in ["total", "steps", "lightly_active_minutes", "fairly_active_minutes", "missing_data"]:
        prompt_page = {}
        if entry == 'total':
            prompt_page['total'] = cur.execute("SELECT COUNT(*) FROM prompts").fetchone()[0]
            prompt_page['complete'] = cur.execute("SELECT COUNT(*) FROM prompts WHERE complete = 1").fetchone()[0]
            prompt_page['percentage'] = round((prompt_page['complete']/prompt_page['total'])*100)

        else:
            prompt_page['total'] = cur.execute("SELECT COUNT(*) FROM prompts WHERE type = ?", (entry,)).fetchone()[0]
            prompt_page['complete'] = cur.execute("SELECT COUNT(*) FROM prompts WHERE type = ? AND complete = 1", (entry,)).fetchone()[0]
            prompt_page['prompt'] = cur.execute("SELECT prompt_id FROM prompts WHERE type = ? AND complete = 0", (entry,)).fetchone()
            if prompt_page["prompt"] is None:
                prompt_page['prompt'] = cur.execute("SELECT prompt_id FROM prompts WHERE type = ?", (entry,)).fetchone()[0]
            else:
                prompt_page["prompt"] = prompt_page["prompt"][0]
                prompt_options.append(prompt_page["prompt"])
            prompt_page['percentage'] = round((prompt_page['complete']/prompt_page['total'])*100)
        prompt_pages[entry] = prompt_page
    con.close()
    prompt_pages['total']['prompt'] = np.random.choice(
            np.array(prompt_options))
    return dbc.Row([dbc.Col([
    dbc.Row(html.H1("Prompt")),
    dbc.Row(html.P("""How-Did-I-Track? has analysed your data and found periods of the highest and lowest 
                   physical activity, trends, and gaps in your data. Prompts for these periods have been 
                   created to help you to understand and reflect on your physical activity. 
                   Your progress towards reviewing the prompts is tracked below.""", 
                   className="prompts--text"), style={"width": "70%", "margin": "auto"}),
    dbc.Row([
        dbc.Col(html.H3("Total Progress", className="prompts--heading"), width=5),
        dbc.Col(dbc.Progress(value=prompt_pages['total']['percentage'], color="info"), width=3),
        dbc.Col(html.P(str(prompt_pages['total']['percentage'])+"%"), width=1),
        dbc.Col(dbc.NavLink("Random Prompt", href="/prompt/"+str(prompt_pages['total']['prompt']),
            className="prompts--button"), width=3),
    ], className="prompts--row"),
    dbc.Row([
        dbc.Col(html.H4("Steps", className="prompts--heading"), width=5),
        dbc.Col(dbc.Progress(value=prompt_pages['steps']['percentage'], 
                             color="info"), width=3),
        dbc.Col(html.P(str(prompt_pages['steps']['percentage'])+"%"), width=1),
        dbc.Col(dbc.NavLink("Steps Prompt", href="/prompt/"+str(prompt_pages['steps']['prompt']), 
            className="prompts--button"), width=3),
    ], className="prompts--row"),
    dbc.Row([
        dbc.Col(html.H4("Fairly Active Minutes", className="prompts--heading"), width=5),
        dbc.Col(dbc.Progress(value=prompt_pages['fairly_active_minutes']['percentage'], color="info"), width=3),
        dbc.Col(html.P(str(prompt_pages['fairly_active_minutes']['percentage'])+"%"), width=1),
        dbc.Col(dbc.NavLink("Fairly Active Minutes Prompt", href="/prompt/"+str(prompt_pages['fairly_active_minutes']['prompt']), 
            className="prompts--button"), width=3),
    ], className="prompts--row"),
    dbc.Row([
        dbc.Col(html.H4("Lightly Active Minutes", className="prompts--heading"), width=5),
        dbc.Col(dbc.Progress(value=prompt_pages['lightly_active_minutes']['percentage'], color="info"), width=3),
        dbc.Col(html.P(str(prompt_pages['lightly_active_minutes']['percentage'])+"%"), width=1),
        dbc.Col(dbc.NavLink("Lightly Active Minutes Prompt", href="/prompt/"+str(prompt_pages['lightly_active_minutes']['prompt']), 
            className="prompts--button"), width=3),
    ], className="prompts--row"),
    dbc.Row([
        dbc.Col(html.H4("Missing Data", className="prompts--heading"), width=5),
        dbc.Col(dbc.Progress(value=prompt_pages['missing_data']['percentage'], color="info"), width=3),
        dbc.Col(html.P(str(prompt_pages['missing_data']['percentage'])+"%"), width=1),
        dbc.Col(dbc.NavLink("Missing Data Prompt", href="/prompt/"+str(prompt_pages['missing_data']['prompt']), className="prompts--button"), width=3),
    ], className="prompts--row"),
])], style={"padding-left": "10px", "max-width": "100%", "padding": "20px"})