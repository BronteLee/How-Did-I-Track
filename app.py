from dash import Dash, html, dcc
import dash


app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.Div(
        className="nav",
        children=[
            html.H1("How-Did-I-Track?"),
            html.A(dcc.Link("Overview", href="/"), className="nav--tab"),
            html.A(dcc.Link("Details", href="/details"), className="nav--tab"),
            html.A(dcc.Link("Compare", href="/compare"), className="nav--tab"),
            html.A(dcc.Link("Prompt", href="/prompt"), className="nav--tab"),
    ]),    
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)
