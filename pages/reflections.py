import dash
from dash import html, dcc, callback, Input, Output, State, ctx, ALL, MATCH
import pandas as pd
from datetime import datetime
import dash_bootstrap_components as dbc
import sqlite3
import json 

dash.register_page(__name__, path_template="/reflections")

filter_con = sqlite3.connect('data/reflecting.db')
filter_cur = filter_con.cursor()
filter_result = filter_cur.execute("SELECT tag FROM tags").fetchall()
filter_tags = []
for tag in filter_result:
    filter_tags.append(tag[0])
filter_con.close()
filter_tags.sort()

layout = dbc.Row([dbc.Col([
    dbc.Row(html.H1("Reflections")),
    dbc.Row([
        dcc.Textarea(
        id="search",
        placeholder="search", className="reflections--text"),
        html.Button("Search", id="confirm-search", className="reflections--search")
    ], style={"width": "50%", "margin": "auto", "float": "unset"}),
    dbc.Row([
        html.P("Filter By", style={"width": "fit-content", "margin-left": "10%"}),
        html.Div(dcc.Dropdown(filter_tags, id='dropdown-filter', clearable=False, style={"width": "100%"}), style={"width": "50%"})
    ], style={"width": "65%", "margin": "auto", "padding": "20px"}),
    dbc.Row(html.Button("Clear All", id="clear", className="reflections--clear")),
    dbc.Row([
        dbc.Col([
            dbc.Row(html.H3("What have I learnt?")),
            dbc.Row(html.Div(id="expanded-learn", style={"overflow": "auto", "max-height": "50vh"}))
        ]),
        dbc.Col([
            dbc.Row(html.H3("What will I do?")),
            dbc.Row(html.Div(id="expanded-do", style={"overflow": "auto", "max-height": "50vh"})),
        ])
    ], style={"padding-top": "20px"})
    ])
])

def make_reflection(entry, tags):
    reflection = []
    reflection.append(html.Button("Edit", id={'role': 'edit', 'index': entry[0]}, className="reflections--edit"))
    reflection.append(html.P(entry[2]))
    add_tags = "Tags: "
    for tag in tags:
        if add_tags == "Tags: ":
            add_tags += tag[0]
        else:
            add_tags += ", " + tag[0]
    reflection.append(html.P(add_tags))
    reflection.append(html.Hr())
    return reflection


def make_reflections(data):
    reflections = []
    tag_con = sqlite3.connect("data/reflecting.db")
    tag_cur = tag_con.cursor()
    reflections.append(html.Hr())
    data.reverse()
    for entry in data: 
        tags = tag_cur.execute("SELECT tag FROM tags JOIN reflections_tags ON (tags.tag_id = reflections_tags.tag_id) WHERE reflection_id = ?", (entry[0],)).fetchall()
        reflection = make_reflection(entry, tags)
        reflections.append(html.Div(reflection, id={'role': 'reflection', "index": entry[0]}))
    tag_con.close()
    return reflections

@callback(
    Output("expanded-learn", "children"),
    Output("expanded-do", "children"),
    State("search", "value"),
    Input("confirm-search", "n_clicks"),
    Input("dropdown-filter", "value"),
    Input("clear", "n_clicks"),
)
def search_and_filter(text, n1, dropdown, n2):
    view_con = sqlite3.connect("data/reflecting.db")
    view_cur = view_con.cursor()
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    learn_data = ""
    do_data = ""
    if trigger_id == "" or trigger_id == "clear":
        learn_data = view_cur.execute('SELECT * FROM reflections WHERE type LIKE "learn"').fetchall()
        do_data = view_cur.execute('SELECT * FROM reflections WHERE type LIKE "do"').fetchall()
    elif trigger_id == "confirm-search":
        search_term = '%'+text+'%'
        learn_data = view_cur.execute('SELECT * FROM reflections WHERE text LIKE ? AND type LIKE "learn"', (search_term,)).fetchall()
        do_data = view_cur.execute('SELECT * FROM reflections WHERE text LIKE ? AND type LIKE "do"', (search_term,)).fetchall()
    elif dropdown:
        learn_data = view_cur.execute('SELECT * FROM reflections JOIN reflections_tags ON reflections.reflection_id = reflections_tags.reflection_id JOIN tags ON reflections_tags.tag_id = tags.tag_id WHERE tag = ? AND type LIKE "learn"', (dropdown,)).fetchall()
        do_data = view_cur.execute('SELECT * FROM reflections JOIN reflections_tags ON reflections.reflection_id = reflections_tags.reflection_id JOIN tags ON reflections_tags.tag_id = tags.tag_id WHERE tag = ? AND type LIKE "do"', (dropdown,)).fetchall()
    view_con.close()
    return make_reflections(learn_data), make_reflections(do_data)

@callback(
        Output({'role': 'reflection', "index": MATCH}, "children", allow_duplicate=True),
        Input({'role': 'edit', 'index': MATCH}, "n_clicks"), prevent_initial_call=True
)
def editing(n):
    if n is None:
        return dash.no_update
    trigger_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    edit_id = json.loads(trigger_id)["index"]
    edit_con = sqlite3.connect("data/reflecting.db")
    edit_cur = edit_con.cursor()
    text = edit_cur.execute("SELECT text FROM reflections WHERE reflection_id = ?", (edit_id,)).fetchone()
    db_tags = edit_cur.execute("SELECT tag FROM tags").fetchall()
    db_reflect_tags = edit_cur.execute("SELECT tag FROM tags JOIN reflections_tags ON (tags.tag_id = reflections_tags.tag_id) WHERE reflection_id = ?", (edit_id,)).fetchall()
    tags = []
    for tag in db_tags:
        tags.append(tag[0])
    reflect_tags = []
    for tag in db_reflect_tags:
        reflect_tags.append(tag[0])
    edit_con.close()
    return [dcc.Textarea(id="text-edit", value=text[0], style={"width": "90%"}),
            dcc.Dropdown(tags, reflect_tags, multi=True, placeholder="Select Tags", id="dropdown-tags", className="reflections--dropdown"),
            html.Button("Save", id={'role': 'save', 'index': edit_id}, className="reflections--save"),
            html.Button("Cancel", id={'role': 'cancel', 'index': edit_id}, className="reflections--cancel"),
            html.Button("Delete", id={'role': 'delete', 'index': edit_id}, className="reflections--delete"),
            html.Hr()]

@callback(
        Output({'role': 'reflection', "index": MATCH}, "children"),
        [State('text-edit', 'value'),
         State('dropdown-tags', 'value'),
         Input({'role': 'save', 'index': MATCH}, "n_clicks"),
         Input({'role': 'delete', 'index': MATCH}, "n_clicks"),
         Input({'role': 'cancel', 'index': MATCH}, "n_clicks")]
)
def update_reflection(text, tags, n1, n2, n3):
    if n1 is None and n2 is None and n3 is None:
        return dash.no_update
    trigger_id = json.loads(dash.callback_context.triggered[0]["prop_id"].split(".")[0])
    save_id = trigger_id["index"]
    update_type = trigger_id["role"]
    save_con = sqlite3.connect("data/reflecting.db")
    save_cur = save_con.cursor()
    if update_type == 'delete':
        save_cur.execute("DELETE FROM reflections WHERE reflection_id = ?", (save_id,))
        save_cur.execute("DELETE FROM reflections_tags WHERE reflection_id = ?", (save_id,))
        save_con.commit()
        save_con.close()
        return []
    elif update_type == 'save':
        save_cur.execute("UPDATE reflections SET text = ? WHERE reflection_id = ?", (text, save_id))
        save_cur.execute("DELETE FROM reflections_tags WHERE reflection_id = ?", (save_id,))
        for tag in tags:
            tag_id = save_cur.execute("SELECT tag_id FROM tags WHERE tag = ?", (tag,)).fetchone()[0]
            check_status = save_cur.execute("SELECT * FROM reflections_tags WHERE tag_id = ? AND reflection_id = ?", (tag_id, save_id)).fetchone()
            if check_status is None:
                save_cur.execute("INSERT INTO reflections_tags(reflection_id, tag_id) VALUES(?, ?)", (save_id, tag_id))
    save_con.commit()
    display_data = save_cur.execute("SELECT * FROM reflections WHERE reflection_id = ?", (save_id,)).fetchall()[0]
    display_tags = save_cur.execute("SELECT tag FROM tags JOIN reflections_tags ON (tags.tag_id = reflections_tags.tag_id) WHERE reflection_id = ?", (save_id,)).fetchall()
    save_con.close()
    return make_reflection(display_data, display_tags)


@callback(
    Output('all-learn', 'children'),
    Output('text-learn', 'value'),
    State('text-learn', 'value'),
    Input('confirm-learn', 'n_clicks')
)
def update_learn(text, clicks):
    update_learn_con = sqlite3.connect("data/reflecting.db")
    update_learn_cur = update_learn_con.cursor()
    if text is None: 
        data = update_learn_cur.execute('SELECT * FROM reflections WHERE type LIKE "learn"').fetchall()
        text = data[-1][2]
    else:
        update_learn_cur.execute('INSERT INTO reflections(type, text) VALUES(?,?)', ("learn", text,))
        update_learn_con.commit()
    update_learn_con.close()
    return text, ""

@callback(
    Output('all-do', 'children'),
    Output('text-do', 'value'),
    State('text-do', 'value'),
    Input('confirm-do', 'n_clicks')
)
def update_do(text, clicks):
    update_do_con = sqlite3.connect("data/reflecting.db")
    update_do_cur = update_do_con.cursor()
    if text is None: 
        data = update_do_cur.execute('SELECT * FROM reflections WHERE type LIKE "do"').fetchall()
        text = data[-1][2]
    else:
        update_do_cur.execute('INSERT INTO reflections(type, text) VALUES(?,?)', ("do", text,))
        update_do_con.commit()
    update_do_con.close()
    return text, ""

