from dash import Dash, html, dcc, Input, Output, clientside_callback, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import dash 
import pycountry_convert as pc
import pandas as pd
from dash_bootstrap_templates import load_figure_template
load_figure_template(["minty", "minty_dark"])


df = pd.read_csv('./data/Top_200_univs.csv', delimiter=';')
#df = pd.read_csv('.\data\Top_200_univs.csv', delimiter=';')
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY, dbc.icons.FONT_AWESOME], suppress_callback_exceptions=True)
layout= dbc.Container(
    [
        html.H1("Jeu de données",className="content"),
        dcc.Markdown(
            '''
           
            Voici notre jeu de données après l'avoir nettoyé et traité de notre part, provenant du jeu de données **[source](https://www.kaggle.com/datasets/alitaqi000/world-university-rankings-2023)** :
            ''',
            className="content",
           
            dangerously_allow_html=True
        ),

        dbc.Table.from_dataframe(
            df,
            bordered=True,
            dark=True,
            hover=True,
            responsive=True,
            striped=True,
        ),
        
    ]
)