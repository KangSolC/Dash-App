from dash import Dash, html, dcc, Input, Output, clientside_callback
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
load_figure_template(["minty", "minty_dark"])

app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY, dbc.icons.FONT_AWESOME])
color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="switch"),
        dbc.Switch( id="switch", value=False, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="switch"),
    ]
)
layout = dbc.Container([
    color_mode_switch,
    dbc.Row([
        dbc.Col([
            html.Div(
                className="content",
                children=[
                    html.H1("Les 200 meilleures universités du monde en 2023", style={'textAlign': 'center','font-weight':'bold','padding':'5px','color':'#176B87'}),
                    html.P("Ce projet a été réalisé par trois étudiantes du master TIW à l'UCBL, dans le cadre du module Analyse de Données en utilisant le framework DASH."),
                    html.P("Découvrons ensemble quelles sont les meilleures universités en 2023 selon le classement mondial, en utilisant les méthodes d'analyse de données !")

                ])
            ],
            width=13
        ),
    ],justify="center"),
                            
    dbc.Row([
        dbc.Col([
            dbc.Carousel(
                items=[
                    {"key": "1","header":"Claude Bernard-Lyon1 University", "src": "./assets/Doua.jpg","img_style":{"height":"700px"}},
                    {"key": "2","header":"Harvard University", "src": "./assets/harvard.jpg","img_style":{"height":"700px"}},
                    {"key": "3", "header":"Hogwarts University","src": "./assets/hogwarts.jpg","img_style":{"height":"700px"}},
                ],
                controls=False,
                indicators=True,
                interval=2000,
                ride="carousel",
            )],
        width=13
        )
    ],justify="center"),

    dbc.Row([
        dbc.Col([
            html.Div(
                className="content",
                children=[
                    dcc.Markdown('''
                    _**Nous pouvons voir les analyses suivantes :**_
                    * L'onglet **Dataset** expose le jeu de données étudié
                    * L'onglet **Distribution** présente des graphes de distribution pour différents attributs du jeu de données
                    * L'onglet **Correlation** met en avant les corrélations entre les attributs
                    * L'onglet **Clustering** montre comment les universités peuvent être regroupées en _clusters_ en fonction de leur score de recherche
                    ''',style={'padding':'5px','margin-top':'20px'})
                ])
        ],width=13),
    ],justify="center"),
    
])