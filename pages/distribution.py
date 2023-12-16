from dash import Dash, html, dcc, Input, Output, clientside_callback, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import dash 
import pycountry_convert as pc
import pandas as pd
from dash_bootstrap_templates import load_figure_template
load_figure_template(["minty", "minty_dark"])

df = pd.read_csv('./data/Top_200_univs.csv',delimiter=';')

# Extraire le continent de chaque pays
def convert(row):
    cn_code = pc.country_name_to_country_alpha2(row.Location, cn_name_format = "default")        
    conti_code = pc.country_alpha2_to_continent_code(cn_code)
    country_continent_name = pc.convert_continent_code_to_continent_name(conti_code)
    return country_continent_name

# On ajoute la colonne du continent
df["continent"]=df.apply(convert,axis=1)

app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY, dbc.icons.FONT_AWESOME], suppress_callback_exceptions=True)

color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="switch"),
        dbc.Switch( id="switch", value=False, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="switch"),
    ]
)

# Graphe de distribution avec les continents
layout = dbc.Container(
    [
        html.H1("Graphes de distribution"),
        color_mode_switch,
        dcc.Graph(id="graph", className="border"),
    ],
    style={'margin': '2rem 0'}
)

@callback(
    Output("graph", "figure"),
    Input("switch", "value"),
    
)
def update_figure_template(switch_on):
    template = "minty" if switch_on else "minty_dark"
    fig = px.scatter(
        df,
        x="No of student",
        y="Research Score",
        size="International Student",
        color="continent",
        symbol="continent",
        hover_name="Name of University",
        hover_data="Location",
        log_x=True,
        size_max=30,
        template=template,
    )
    return fig

clientside_callback(
    """
    (switchOn) => {
       switchOn
         ? document.documentElement.setAttribute('data-bs-theme', 'light')
         : document.documentElement.setAttribute('data-bs-theme', 'dark')
       return window.dash_clientside.no_update
    }
    """,
    Output("switch", "id"),
    Input("switch", "value"),
)

if __name__ == "__main__":

    app.run_server(debug=True)