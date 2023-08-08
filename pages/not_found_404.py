from dash import html
import dash

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1("This page does not exist"),
    html.P("Click one of the options above to return to a page.")
])