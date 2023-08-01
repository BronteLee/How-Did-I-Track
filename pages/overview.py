import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
from plotly_calplot import calplot
from datetime import date

dash.register_page(__name__, path='/')

df = pd.read_json("data/daily-data.json", convert_dates=False)
df['date'] = pd.to_datetime(df['date'], dayfirst=True)


layout = html.Div(
    className="main",
    children=[
    html.H1("Overview"),
    dcc.Dropdown(
                [2017, 2018, 2019, 2020, 2021, 2022, 2023],
                id="year_select",
                value=2023,
                clearable=False
            ),
    dcc.Graph(id="cal_plot", style={'width': '70%'})
])

@callback(
    Output(component_id="cal_plot", component_property="figure"),
    Input(component_id='year_select', component_property='value'),
)
def update_graph(value):
    start_date = date(value, 1, 1)
    end_date = date(value, 12, 31)
    dff = df.query("date > @start_date & date < @end_date")
    plot = calplot(
        dff,
        x='date',
        y='steps',
        gap=2,
        colorscale="purples",
    )
    return plot
