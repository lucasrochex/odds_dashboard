# Import external packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta, datetime
# Import internal custom packages
from src.database.data_retriever import get_odds_48
from src.data_treament.odds_shapper import prepare_odd_df, sort_slopes

# External style sheet
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
# Initiate App
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css])

leagues_reduction = ['usa-usl-league-one', 'conmebol-copa-sudamericana', 'conmebol-copa-libertadores',
          'uefa-champions-league', 'mexico-primera-division', 'brazil-serie-a', 'england-premier-league',
          'spain-la-liga', 'italy-serie-a', 'germany-bundesliga', 'uefa-europa-league', 'argentina-liga-pro',
          'brazil-serie-b', 'usa-major-league-soccer', 'france-ligue-1', 'france-ligue-2',
          'spain-segunda-division', 'england-championship', 'italy-serie-a', 'italy-serie-b',
          'brazil-cup']
df_48 = get_odds_48()
leagues = df_48['league'].unique()
df_48_filtered = df_48[df_48['league'].isin(leagues_reduction)]
games_48 = prepare_odd_df(df_48[df_48['league']==leagues[0]])
odds_48 = games_48.columns
games_48_slope = prepare_odd_df(df_48_filtered)
sorted_slopes = sort_slopes(games_48_slope)
print(sorted_slopes)
# App layout
app.layout = html.Div([
    dbc.Row(
        children = [html.Div("Odds", style={'fontSize': 36, 'width': '95%'})],
        style = {'marginLeft': '10px', 'marginRight': '10px', 'marginTop': '10px'}),
    html.Div([
            dcc.Dropdown(
                    id="leagues_48_options",
                    options=[{'label': item, 'value': item} for item in leagues],
                    value= leagues[0],
                    multi=True
                )
        ], style={'width': '99%', 'verticalAlign': 'center', 'marginLeft': '10px', 'marginRight': '5px'}
        ),
    html.Div([
            dcc.Dropdown(
                    id="games_48_options",
                    options=[{'label': item, 'value': item} for item in odds_48],
                    value= odds_48,
                    multi=True
                )
        ], style={'width': '99%', 'verticalAlign': 'center', 'marginLeft': '10px', 'marginRight': '5px'}
        ),
    html.Div('Odds ultimas 48 horas', style={'textAlign': 'center', 'fontSize': 20, 'marginBottom': '1px'}),
    html.Div(children=[
        html.Div(className='totals_graph', children=[
            dcc.Graph(figure={}, id='odds_48_graph')
        ], style={'marginTop': '1px', 'height': '98%', 'marginLeft': '10px', 'marginRight': '10px'})
    ]),
    dcc.Interval(id='interval-updater', interval=120*1000, n_intervals=0),
    html.Div([
            dcc.Dropdown(
                    id="games_slopes",
                    options=[{'label': item, 'value': item} for item in sorted_slopes],
                    value= sorted_slopes[:5],
                    multi=True
                )
        ], style={'width': '99%', 'verticalAlign': 'center', 'marginLeft': '10px', 'marginRight': '5px'}
        ),
    html.Div('Tendências de queda', style={'textAlign': 'center', 'fontSize': 20, 'marginBottom': '1px'}),
    html.Div(children=[
        html.Div(className='totals_graph', children=[
            dcc.Graph(figure={}, id='slopes_48_graph')
        ], style={'marginTop': '1px', 'height': '98%', 'marginLeft': '10px', 'marginRight': '10px'})
    ])
], className='dbc')

# Best reductions
@app.callback(
    Output("slopes_48_graph", "figure"),
    Input("games_slopes", "value"),
    Input("interval-updater", "n_intervals")
)
def update_best_slopes_48_odds(items, n_intervals):
    df_48 = get_odds_48()
    games_48 = prepare_odd_df(df_48)
    if isinstance(items, str):
        data = [go.Scatter(x=games_48.index,
                    y=games_48[items],
                    #mode='markers',l
                    line_shape='spline',
                    connectgaps = True,
                    name= items)]    
    else:
        data = [go.Scatter(x=games_48.index,
                        y=games_48[label],
                        #mode='markers',l
                        line_shape='spline',
                        connectgaps = True,
                        name= label) for label in items
                    ]
    layout = go.Layout()
    fig = go.Figure(data=data,layout=layout)
    return fig

# Update team dropdown menu's content
@app.callback(
    Output('games_48_options','options'),
    Output('games_48_options', 'value'),
    Input('leagues_48_options', 'value')
)
def update_games_list(value):
    df_48 = get_odds_48()
    if isinstance(value, str):
        games_48 = prepare_odd_df(df_48[df_48['league']==value])    
    else:
        games_48 = prepare_odd_df(df_48[df_48['league'].isin(value)])
    odds_48 = games_48.columns
    return([{'label': i, 'value': i} for i in odds_48], odds_48[0])

# Update last 48 hours odd graph
@app.callback(
    Output("odds_48_graph", "figure"),
    Input("interval-updater", "n_intervals"),
    Input("games_48_options", "value")
)
def update_last_48_odds(n_intervals, items):
    df_48 = get_odds_48()
    games_48 = prepare_odd_df(df_48)
    if isinstance(items, str):
        data = [go.Scatter(x=games_48.index,
                    y=games_48[items],
                    #mode='markers',l
                    line_shape='spline',
                    connectgaps = True,
                    name= items)]    
    else:
        data = [go.Scatter(x=games_48.index,
                        y=games_48[label],
                        #mode='markers',l
                        line_shape='spline',
                        connectgaps = True,
                        name= label) for label in items
                    ]
    layout = go.Layout()
    fig = go.Figure(data=data,layout=layout)
    return fig

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8029)
