from dash import Dash, html, dcc, Input, Output, clientside_callback, callback, State
import plotly.express as px
import dash_bootstrap_components as dbc
import dash 
import pycountry_convert as pc
from sklearn.mixture import BayesianGaussianMixture
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
import pandas as pd
from dash_bootstrap_templates import load_figure_template
import scipy.stats as stats
import matplotlib.pyplot as plt
import plotly.tools as tls
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
load_figure_template(["minty", "minty_dark"])

df = pd.read_csv('./data/Top_200_univs.csv', delimiter=';')
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY, dbc.icons.FONT_AWESOME], suppress_callback_exceptions=True)

layout= dbc.Container(
    [
        html.H1("Clustering",className="content"),
        html.H6('Choisissez une méthode de clustering :',className="content"),
        dcc.RadioItems(options = ['K-Means', 'Gaussian Mixtures', 'DBScan'], value='K-Means', id='controls-cluster',className="content"),
        
        #Selon le choix de l'utilisateur, on lui demande la valeurs des paramètres de chaque méthode
        html.Div(id='kmeans-options',className="content", children=[
            html.Label('Nombre de Clusters pour K-Means', style={'margin-right': '10px'}),
            dcc.Input(id='nombre-clusters', type='text', value='3', style={'width': '60px'}),
        ], style={'display': 'none'}),  
        
        html.Div(id='gaussian-options',className="content", children=[
            html.Label('Nombre de Composantes pour Gaussian Mixtures', style={'margin-right': '10px'}),
            dcc.Input(id='nombre-gaussian', type='text', value='3', style={'width': '60px'}),
        ], style={'display': 'none'}),  
        
        html.Div(id='dbscan-eps',className="content", children=[
        html.Label('Epsilon pour DBScan', style={'margin-right': '10px'}),
        dcc.Input(id='eps', type='text', value='0.5', style={'width': '60px'}),
        ], style={'display': 'none', 'margin-bottom': '10px'}),  

        html.Div(children=[]),

        html.Div(id='dbscan-nbre-min', children=[
            html.Label('Nombre minimum d\'échantillons pour DBScan',className="content", style={'margin-right': '10px'}),
            dcc.Input(id='min-samples', type='text', value='5', style={'margin-bottom': '10px', 'width': '60px'}),
        ], style={'display': 'none', 'margin-bottom': '10px'}),  

        html.Button('Confirmer', id='valider_button',className='btn btn-info'),
        
        html.H3("Avec normalisation des données",className="content",style={'margin-top':'20px'}),
        dcc.Graph(figure={}, id='cluster-with-normalization'),
        html.H3("Sans normalisation des données",className="content",style={'margin-top': '20px'}),
        dcc.Graph(figure={}, id='cluster-without-normalization')
        
    ]
)

#Ce callback affiche un input text à l'utilisateur pour saisir la valeur des paramètre(s) de méthode de Clustering
@callback(
    Output('kmeans-options', 'style'),
    Output('gaussian-options', 'style'),
    Output('dbscan-eps', 'style'),
    Output('dbscan-nbre-min', 'style'),
    Input('controls-cluster', 'value')
)
def display_options(selected_clustering):
    kmeans_style = {'display': 'block' if selected_clustering == 'K-Means' else 'none'}
    gaussian_style = {'display': 'block' if selected_clustering == 'Gaussian Mixtures' else 'none'}
    dbscan_eps_style = {'display': 'block' if selected_clustering == 'DBScan' else 'none'}
    dbscan_nbre_min_style = {'display': 'block' if selected_clustering == 'DBScan' else 'none'}
    return kmeans_style, gaussian_style, dbscan_eps_style, dbscan_nbre_min_style

#Ce callback est utilisé pour le clustering
@callback(
    Output('cluster-with-normalization', 'figure'),
    Output('cluster-without-normalization', 'figure'),
    Input('controls-cluster', 'value'),
    Input('valider_button', 'n_clicks'),
    State('nombre-clusters', 'value'),
    State('nombre-gaussian', 'value'),
    State('eps', 'value'),
    State('min-samples', 'value')
)
def update_clustering_graph(col_chosen, valider_button, nbre_clusters, nbre_gaussian, eps, min_samples):
    # Normaliser les données
    df_normalized = stats.zscore(df[["No of student", "Research Score"]])
    
    selected_features = df[['No of student', 'Research Score']]
    
    if col_chosen == 'K-Means':
        try:
            nbre_c = int(nbre_clusters)
        except ValueError:
            nbre_c = 3
            
        kmeans = KMeans(n_clusters=int(nbre_c), random_state=42)
        clusters = kmeans.fit_predict(selected_features)
        clusters_normalized = kmeans.fit_predict(df_normalized)

    elif col_chosen == 'Gaussian Mixtures':
        try:
            nbre_g = int(nbre_gaussian)
        except ValueError:
            nbre_g = 3

        gaussian = BayesianGaussianMixture(n_components=nbre_g)
        clusters = gaussian.fit_predict(selected_features)
        clusters_normalized = gaussian.fit_predict(df_normalized)

    elif col_chosen == 'DBScan':
        try:
            eps_value = float(eps)
            min_samples_value = int(min_samples)
        except ValueError:
            eps_value = 0.5 
            min_samples_value = 5

        dbscan = DBSCAN(eps=eps_value, min_samples=min_samples_value)
        clusters = dbscan.fit_predict(selected_features)
        clusters_normalized = dbscan.fit_predict(df_normalized)

    # Création de Scatter plot pour le graphe Without Normalization
    fig1, ax1 = plt.subplots(figsize=(13, 5))
    sns.scatterplot(data=df, x="No of student", y="Research Score", hue=clusters, palette='deep', ax=ax1)
    
    # Création Scatter plot pour le graphe With Normalization
    fig2, ax2 = plt.subplots(figsize=(13, 5))
    sns.scatterplot(data=df, x="No of student", y="Research Score", hue=clusters_normalized, palette='deep', ax=ax2)

    # Convertir en Plotly figures
    plotly_fig1 = tls.mpl_to_plotly(fig1)
    plotly_fig2 = tls.mpl_to_plotly(fig2)

    return plotly_fig1, plotly_fig2