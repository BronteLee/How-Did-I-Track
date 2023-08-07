import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
from plotly_calplot import calplot
from datetime import date

dash.register_page(__name__, path='/')

df = pd.read_json("data/daily-data-2.json", convert_dates=False)
df['date'] = pd.to_datetime(df['date'], dayfirst=True)


layout = html.Div(
    className="page",
    children=[
    html.H1("Overview"),
    dcc.Dropdown(
                [2017, 2018, 2019, 2020, 2021, 2022, 2023],
                id="year_select",
                value=2023,
                clearable=False,
                style={"width": "40%", "padding-left": "10%"},
            ),
    html.H3("My Steps"),
    dcc.Graph(id="cal_steps", config={
        'displayModeBar': False}),
    html.H3("My Fairly Active Minutes"),
    dcc.Graph(id="cal_fairly_AM", config={
        'displayModeBar': False}),
    html.H3("My Lightly Active Minutes"),
    dcc.Graph(id="cal_lightly_AM", config={
        'displayModeBar': False})
])

@callback(
    Output(component_id="cal_steps", component_property="figure"),
    Output(component_id="cal_fairly_AM", component_property="figure"),
    Output(component_id="cal_lightly_AM", component_property="figure"),
    Input(component_id='year_select', component_property='value'),
)
def update_graph(value):
    start_date = date(value, 1, 1)
    end_date = date(value, 12, 31)
    dff = df.query("date > @start_date & date < @end_date")
    steps = calplot(
        dff,
        x='date',
        y='steps',
        gap=2,
        colorscale=[[0.0, "#e9e6eb"], [0.001, "#e9cffc"], [0.2, "#eeaaff"],[0.4, "#dd88ee"], [0.6, "#aa66cc"], [0.8, "#7744aa"], [1.0, "#442255"]],
        showscale=True,
        text="hours_worn",
        month_lines_width=2,
        month_lines_color="black",
    )
    fairly_AM = calplot(
        dff,
        x='date',
        y='fairly_active_minutes',
        gap=2,
        colorscale=[[0.0, "#e9e6eb"], [0.001, "#e9cffc"], [0.2, "#eeaaff"],[0.4, "#dd88ee"], [0.6, "#aa66cc"], [0.8, "#7744aa"], [1.0, "#442255"]],
        showscale=True,
        text="hours_worn",
        month_lines_width=2,
        month_lines_color="black",
    )
    lightly_AM = calplot(
        dff,
        x='date',
        y='lightly_active_minutes',
        gap=2,
        colorscale=[[0.0, "#e9e6eb"], [0.001, "#e9cffc"], [0.2, "#eeaaff"],[0.4, "#dd88ee"], [0.6, "#aa66cc"], [0.8, "#7744aa"], [1.0, "#442255"]],
        showscale=True,
        text="hours_worn",
        month_lines_width=2,
        month_lines_color="black",
    )
    return steps, fairly_AM, lightly_AM
