from dash import Dash, html, dcc, Input, Output, clientside_callback
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
load_figure_template(["minty", "minty_dark"])

app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY, dbc.icons.FONT_AWESOME])

layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            html.Div(
                className="content",
                children=[
                    html.H1("Les 200 meilleures universités du monde en 2023", style={'textAlign': 'center','font-weight':'bold','padding':'5px'}),
                    html.P("Ceci est un projet réalisé par 3 étudiantes du master TIW à l'UCBL dans le cadre du module Analyse de Données en utilisant le module [DASH]. Découvrons ensemble quelles sont les meilleures universités de 2023 selon le classement mondial !")
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
                    * L'onglet **Data** montre le jeu de données traité
                    * L'onglet **Distribution** vous présentera des graphes de distribution entre différents attributs du jeu de données
                    * L'onglet **Clustering** vous montrera comment les universités peuvent être réparties en _groupes_
                    ''',style={'padding':'5px','margin-bottom':'20px','margin-top':'20px'})
                ])
        ],width=13),
    ],justify="center"),
    
])