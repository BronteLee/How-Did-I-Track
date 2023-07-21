from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd

# data
# df = pd.read_csv('test.csv')
df = pd.read_json('steps-2018-01-22.json')

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='How Did I Track?'),
    html.Hr(),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    #dcc.RadioItems(options=['Steps', 'Active Minutes'], value='Steps', id='item-selection'),
    #dcc.Graph(figure={}, id='graph')
    dcc.Graph(figure=px.histogram(df, x='dateTime', y="value", nbins=31))
])
"""
@callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='item-selection', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='Day', y=col_chosen, nbins=7)
    return fig
    """

if __name__ == '__main__':
    app.run(debug=True)
