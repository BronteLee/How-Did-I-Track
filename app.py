from dash import Dash, dash, html, dcc
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
    dbc.Row(html.H3("My Reflections")),
    dbc.Row(html.P("What have I learnt?")),
    dbc.Row(html.P("What will I do?"))

])

app.layout = dbc.Container(
    [
        dbc.Row(navbar),
        dbc.Row([
            dbc.Col(dash.page_container, width=9),
            dbc.Col(reflections)]
        )
    ],
    style={"margin": "0px", "max-width": "100%", "width": "100%"}
)

if __name__ == '__main__':
    app.run(debug=True)
