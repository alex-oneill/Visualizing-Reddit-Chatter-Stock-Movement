import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from ChartVal import ChartVal
from scrape-transform-load import *

app = dash.Dash()


zipped_lists = zip()

app.layout = html.Div(

)


def start_dash(chart_obj):
    app.run_server(debug=True)


if __name__ == '__main__':
    app.run_server(debug=True)
