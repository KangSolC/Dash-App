from dash import Dash, html, dcc, Input, Output, clientside_callback, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import dash
import dash_ag_grid as dag
import pycountry_convert as pc
import numpy as np
import pandas as pd
from dash_bootstrap_templates import load_figure_template
load_figure_template(["minty", "minty_dark"])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY, dbc.icons.FONT_AWESOME], suppress_callback_exceptions=True)

df = pd.read_csv('./data/Top_200_univs.csv', delimiter=';')

df_numerical = df.select_dtypes(include=np.number).dropna()
correlation_matrix = df_numerical.corr()

# Extraire le continent de chaque pays
def convert(row):
    cn_code = pc.country_name_to_country_alpha2(row.Location, cn_name_format = "default")
    conti_code = pc.country_alpha2_to_continent_code(cn_code)
    country_continent_name = pc.convert_continent_code_to_continent_name(conti_code)
    return country_continent_name

# On ajoute la colonne du continent
df["Continent"]=df.apply(convert,axis=1)

matrix = px.scatter_matrix(
    df,
    dimensions=["University Rank", "No of student", "International Student", "Research Score", "Teaching Score"],
    color="Continent", symbol="Continent"
)
matrix.update_traces(diagonal_visible=False)

layout= dbc.Container(
    [
        html.H1("Correlation",className="content"),
        html.H3("Matrice de corrélation",className="content"),
        dcc.Markdown(correlation_matrix.to_markdown(), className='correlation-table'),
        html.H3("Matrice de dispersion", style={'margin-top': '2rem'},className="content"),
        dcc.Graph(
            id='corr-matrix',
            figure=matrix
        )
    ]
)