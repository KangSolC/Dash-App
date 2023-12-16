from dash import Dash, html, dcc, Input, Output, clientside_callback
import dash
import dash_bootstrap_components as dbc
from pages import dataSet, distribution,home
import navbar 

from dash_bootstrap_templates import load_figure_template
load_figure_template(["minty", "minty_dark"])
app = Dash(__name__,external_stylesheets=[dbc.themes.MINTY, dbc.icons.FONT_AWESOME], suppress_callback_exceptions=True)

'''
app.layout = html.Div([
    

    navbar.navbar,

    html.H1('200 meilleures universités du monde en 2023'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])
'''
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Data", href="/data")),
        dbc.NavItem(dbc.NavLink("Distribution", href="/distribution")),
        dbc.NavItem(dbc.NavLink("Clustering", href="/clustering")),
    ],
    brand="Data Analysis Project TIW 23-24",
    color="primary",
    brand_href="/",
    dark=True,
    className="navbar navbar-expand-lg bg-primary",
)
gitlab_url = "https://forge.univ-lyon1.fr/p1908025/ad-projet-2024"  

# Define CSS styles for the footer
footer_style = {
    'border': '1px solid #ccc',     # Add a border at the top
     'display': 'flex',
  'align-items': 'center', 
    
   # Center-align the text
      
  'z-index': '9000',
'bottom': '0',
'left': '0',
'right': '0',
'position': 'fixed',           # Add some padding for spacing
    'background-color': '#f2f2f2'   # Set a background color
}


footer= html.Footer(
    
        children=([
            html.P("To access the project code source click on the gitlab icon"),
            dbc.Col([

        html.A(
            html.I(className="fab fa-gitlab"), # Icon from font awesome
            href=gitlab_url,
            target="_blank",
            style={'margin-right':'0'}
        ),]),
        
        html.A(
            children=([
            html.I(className="fas fa-copyright"), # Icon from font awesome
            html.P("Master TIW 2023-2023 : "),
            
            html.P(" Hajar AMAKHZOUN "),
           
            html.P(" , Mouna EL GARB "),
           html.P(", Cécilia NGUYEN "),
            ]),
            style={'display':'flex'},
           
        )]),
        style=footer_style)
   
        
            

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        navbar,
        dbc.Container(id="page-content", className="mb-4", fluid=True),
       
        dash.page_container,
    footer,
    ]
)


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/":
        return home.layout
    if pathname == "/data":
        return dataSet.layout
    elif pathname == "/distribution":
        return distribution.layout
    else:
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognized..."),
            ]
        )

if __name__ == '__main__':
    app.run(debug=True)
    