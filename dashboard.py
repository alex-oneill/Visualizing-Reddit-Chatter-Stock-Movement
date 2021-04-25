import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

app = dash.Dash()

# SECTION: APP LAYOUT
app.layout = dbc.Container([
    dbc.Jumbotron(children=[
        html.H1('Visualizing GME Movement with Real-Time Reddit Chatter', style={'textAlign': 'center'},
                className='display-3'),
        html.P('CS666 | Enterprise Intelligence Development | Prof. Barabasi', style={'textAlign': 'center'}),
        html.P('Alex ONeill | Gio Abou Jaoude | Noah Ponticiello', style={'textAlign': 'center'},
               className='lead')
    ], className='jumbotron'),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H3('Reddit Comment Points', className='card-title'), html.Hr(),
                    html.Div('Points are calculated based on two factors.'), html.Hr(),
                    html.Div('1) If a comment is on a thread mentioning GME, it receives 0.5 points.'),
                    html.Div('2) If the comment directly mentions GME, it receives 1 point.'),
                    html.Hr(),
                    html.Div('Points are counted in groupings of 60 seconds.')
                ])
            ], className='card text-white bg-info mb-3'),
            width=2
        ),
        dbc.Col(
            dbc.Card(dcc.Graph(id='points_graph'), className='card border-info mb-3'),
            width=10
        )
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H3('GME Volume & Price Movement', className='card-title'), html.Hr(),
                    html.Div('IEX Volume and Price is used for the most up-to-date report.'), html.Hr(),
                    html.Div('IEX is only a subset of the market, so the volume does not display total trading volume'),
                ]),
                className='card text-white bg-info mb-3'),
            width=2
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(id='vol_graph'),
                    dcc.Graph(id='price_graph')
                ]),
                className='card border-info mb-3'
            ),
            width=10
        )
    ]),
    dcc.Interval(id='interval', n_intervals=0, interval=15*1000),
], fluid=True)


@app.callback([Output('vol_graph', 'figure'),
               Output('price_graph', 'figure'),
               Output('points_graph', 'figure')],
              Input('interval', 'n_intervals'))
def update_df(interval):
    if interval == 0:
        raise dash.exceptions.PreventUpdate
    else:
        updated_df = pd.read_csv('vals.csv')
        updated_df['TIME_GROUP'] = pd.to_datetime(updated_df.TIME_GROUP, unit='s').dt.\
            tz_localize('utc').dt.tz_convert('US/Eastern')

        points_graph = go.Figure(data=go.Scatter(x=updated_df['TIME_GROUP'], y=updated_df['GROUP_POINTS']))
        points_graph.update_layout(xaxis_title='Time', yaxis_title='Reddit Comment Points',
                                   title={'text': "Reddit Comment 'Points'", 'x': 0.5})

        vol_graph = go.Figure(data=go.Scatter(x=updated_df['TIME_GROUP'], y=updated_df['GROUP_VOLUME']))
        vol_graph.update_layout(xaxis_title='Time', yaxis_title='Volume', title={'text': 'GME Trading Volume',
                                                                                 'x': 0.5})

        price_graph = go.Figure(data=go.Scatter(x=updated_df['TIME_GROUP'], y=updated_df['GROUP_PRICE']))
        price_graph.update_layout(xaxis_title='Time', yaxis_title='Price', title={'text': 'GME Price',
                                                                                  'x': 0.5})

        return vol_graph, price_graph, points_graph


if __name__ == '__main__':
    app.run_server(debug=True)
