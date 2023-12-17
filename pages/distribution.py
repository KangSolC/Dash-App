from dash import Dash, html, dcc, Input, Output, clientside_callback, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import dash 
import pycountry_convert as pc
import pandas as pd
from pages import home
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



# Graphe de distribution avec les continents
layout = dbc.Container(
    [
        html.H1("Graphes de distribution",className="content"),
        html.Div(children='Sélectionnez l\'axe Y'),
        dcc.RadioItems(
            options = {
                'No of student': 'Nombre des Étudiants',
                'International Student': 'Étudiants Internationaux',
                'Teaching Score': 'Score d\'Enseignement',
                'Research Score': 'Score de Recherche'
            },
            value='No of student',
            id='distribution-items'
        ),
        html.Br(),
        dcc.Graph(figure={}, id='distribution-graph'),

        html.Div(
            home.color_mode_switch,style={'visibility':'hidden'}),
        html.H6("Distribution du nombre d'étudiants par rapport au score de recherche avec\
                 comme taille le nombre d'étudiants internationaux",className="content",style={'margin-top':'-20px'}),

        dcc.Graph(id="graph", className="border"),
        html.Br(),
        html.H6("Distribution du nombre d'étudiants internationaux par rapport au rang de l'université avec\
                 comme taille le nombre total d'étudiants ",className="content"),
        dcc.Graph(id="graph2", className="border"),
    ]
)

#Ce callback prend en entrée la valeur choisi par l'utilisateur en axe Y et retourne la figure de la distribution
@callback(
    Output(component_id='distribution-graph', component_property='figure'),
    Input(component_id='distribution-items', component_property='value')
)

def update_distribution_graph(col_chosen):
    fig = px.histogram(df, x='University Rank', y=col_chosen)
    return fig


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

@callback(
    Output("graph2", "figure"),
    Input("switch", "value"),
)

def update_figure_template2(switch_on):
    template = "minty" if switch_on else "minty_dark"
    fig2 = px.scatter(
        df,
        x="International Student",
        y="University Rank",
        size="International Student",
        color="continent",
        symbol="continent",
        hover_name="Name of University",
        hover_data="Location",
        log_x=True,
        size_max=40,
        template=template,
    )
    return fig2

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