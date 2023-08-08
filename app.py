from dash import Dash, dash, html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc


app = Dash(__name__, suppress_callback_exceptions=True, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar = dbc.Navbar(
    dbc.Container(
        dbc.Row([
            dbc.Col(html.P("How-Did-I-Track?", style={"font-size": "16px", "text-decoration": "wavy"})),
            dbc.Col(dbc.NavLink("Overview", href="/", class_name="nav")),
            dbc.Col(dbc.NavLink("Details", href="/details", class_name="nav")),
            dbc.Col(dbc.NavLink("Prompt", href="/prompt", class_name="nav")),
        ], style={'width': '100%'}),
        
    ),
    color="#CBC3E3",
    sticky="top",
    style={"margin": "0"},
)

reflections = dbc.Container([
    dbc.Col([
        dbc.Row(html.H3("My Reflections")),
        dbc.Row(html.P("What have I learnt?")),
        dbc.Row(dcc.Textarea(
            id="text-learn",
            placeholder="I learnt ...",
            style={"width":"90%", "margin": "auto"})),
        dbc.Row(html.Button("Add", id="confirm-learn", style={"width":"50%", "margin": "auto"})),
        dbc.Row(html.P(id="all-learn"))
    ]),
    dbc.Col([
        dbc.Row(html.P("What will I do?")),
        dbc.Row(dcc.Textarea(
            id="text-do",
            placeholder="I will ...",
            style={"width":"90%", "margin": "auto"})),
        dbc.Row(html.Button("Add", id="confirm-do", style={"width":"50%", "margin": "auto"})),
        dbc.Row(html.P(id="all-do"))
    ])],
    style={"width":"25%","height": "100vh", "position":"fixed"})

app.layout = dbc.Container(
    [
        navbar,
        dbc.Row([
            dbc.Col(dash.page_container, width=9),
            dbc.Col(reflections)]
        )
    ],
    fluid=True,
    style={"margin": "0px", "max-width": "100%", "width": "100%"}
)

@callback(
    Output('all-learn', 'children'),
    Output('text-learn', 'value'),
    State('text-learn', 'value'),
    Input('confirm-learn', 'n_clicks')
)
def update_learn(text, clicks):
    return text, ""

@callback(
    Output('all-do', 'children'),
    Output('text-do', 'value'),
    State('text-do', 'value'),
    Input('confirm-do', 'n_clicks')
)
def update_learn(text, clicks):
    return text, ""


if __name__ == '__main__':
    app.run(debug=True)
