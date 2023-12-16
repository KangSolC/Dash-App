from dash import Dash, html, dcc, Input, Output, clientside_callback, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import dash 
import pycountry_convert as pc

import pandas as pd

from dash_bootstrap_templates import load_figure_template
load_figure_template(["minty", "minty_dark"])


df = pd.read_csv('data\Top_200_univs.csv', delimiter=';')
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY, dbc.icons.FONT_AWESOME], suppress_callback_exceptions=True)
layout= dbc.Container(
    [
        dcc.Markdown('''
          Le résultat du traitement des **[données](https://www.kaggle.com/datasets/alitaqi000/world-university-rankings-2023)** est le suivant : 
                ''',style={'padding':'5px','margin-bottom':'20px','margin-top':'20px'}, dangerously_allow_html=True),
        # 'This is an inlined <dccLink href="https://www.google.com" /> with text on both sides',
   # dangerously_allow_html=True,
       dbc.Table.from_dataframe(
    # using the same table as in the above example
    df,
    bordered=True,
    dark=True,
    hover=True,
    responsive=True,
    striped=True,
    
),
dbc.Pagination(max_value=15),
        
    ]

)