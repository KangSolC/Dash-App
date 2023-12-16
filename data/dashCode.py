from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.cluster import KMeans
import scipy.stats as stats
import seaborn as sns
import plotly.subplots as sp
import plotly.graph_objs as go
from sklearn.mixture import BayesianGaussianMixture
from sklearn.cluster import DBSCAN

#Load data
df = pd.read_csv('./first_200_univs.csv') 
df_numerical = df.select_dtypes(include=np.number).dropna()

#Correlation
correlation_matrix = df_numerical.corr()

#Initialize the application
app = Dash(__name__)

#Components to be displayed in the html page
app.layout = html.Div([
    html.Div(children='Dash Board for University Rankings'),
    #Distribution
    html.Div(children='Choisissez votre axe Y'),
    dcc.RadioItems(options = ['No of student', 'International Student', 'Research Score'], value='No of student', id='distribution-items'),
    dcc.Graph(figure={}, id='distribution-graph'),
    
    #Data table
    html.Div(children='Jeu de Données'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=15),
    
    #Matrice de Corrélation
    html.Div(children=[
        html.H4("Matrice de Corrélation :"),
        dcc.Markdown(correlation_matrix.to_markdown())
    ]),

    #Cluster
    html.Div(children='Clustering, choisissez la méthode de clustering'),
    dcc.RadioItems(options = ['K-Means', 'Gaussian Mixtures', 'DBScan'], value='K-Means', id='controls-cluster'),
    
    #Selon le choix de l'utilisateur, on lui demande la valeurs des paramètres de chaque méthode
    html.Div(id='kmeans-options', children=[
        dcc.Input(id='nombre-clusters', type='text', value='3'),
    ], style={'display': 'none'}),  # Initialement masqué
    
    html.Div(id='gaussian-options', children=[
        dcc.Input(id='nombre-gaussian', type='text', value='3'),
    ], style={'display': 'none'}),  # Initialement masqué
    
    html.Div(id='dbscan-options', children=[
        dcc.Input(id='eps', type='text', value='0.5'),
        dcc.Input(id='min-samples', type='text', value='5'),
    ], style={'display': 'none'}),  # Initialement masqué
    
    html.Button('Valider', id='valider_button'),    
    
    dcc.Graph(figure={}, id='cluster-graph')
    ])

#Ce callback affiche un input text à l'utilisateur pour saisir la valeur des paramètre(s) de méthode de Clustering
@app.callback(
    Output('kmeans-options', 'style'),
    Output('gaussian-options', 'style'),
    Output('dbscan-options', 'style'),
    Input('controls-cluster', 'value')
)
def display_options(selected_clustering):
    kmeans_style = {'display': 'block' if selected_clustering == 'K-Means' else 'none'}
    gaussian_style = {'display': 'block' if selected_clustering == 'Gaussian Mixtures' else 'none'}
    dbscan_style = {'display': 'block' if selected_clustering == 'DBScan' else 'none'}
    return kmeans_style, gaussian_style, dbscan_style

#Ce callback prend en entrée la valeur choisi par l'utilisateur en axe Y et retourne la figure de la distribution
@app.callback(
    Output(component_id='distribution-graph', component_property='figure'),
    Input(component_id='distribution-items', component_property='value')
)

def update_distribution_graph(col_chosen):
    # fig = px.histogram(df, x='University Rank', y=col_chosen, histfunc='avg')
    fig = px.histogram(df, x='University Rank', y=col_chosen)
    return fig

#Ce callback est utilisé pour leclustering
@app.callback(
    Output('cluster-graph', 'figure'),
    Input('controls-cluster', 'value'),
    Input('valider_button', 'n_clicks'),
    State('nombre-clusters', 'value'),
    State('nombre-gaussian', 'value'),
    State('eps', 'value'),
    State('min-samples', 'value')
)
def update_clustering_graph(col_chosen, valider_button, nbre_clusters, nbre_gaussian, eps, min_samples):
    # Normalize data
    df_normalized = stats.zscore(df[["No of student", "International Student", "Research Score"]])
    
    selected_features = df[['No of student', 'International Student', 'Research Score']]
    
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

    # Création d'un subplot avec 1 ligne et 2 colonnes
    fig = sp.make_subplots(rows=1, cols=2, subplot_titles=['Without Normalization', 'With Normalization'])

    # Scatter plot pour Without Normalization
    trace1 = go.Scatter(x=df['No of student'], y=df['International Student'], mode='markers', marker=dict(color=clusters))
    fig.add_trace(trace1, row=1, col=1)

    # Scatter plot pour With Normalization
    trace2 = go.Scatter(x=df['No of student'], y=df['International Student'], mode='markers', marker=dict(color=clusters_normalized))
    fig.add_trace(trace2, row=1, col=2)

    # Update layout
    fig.update_layout(title_text='Clustering Results')

    return fig

#ruun iit
if __name__ == '__main__':
    app.run(debug=True)