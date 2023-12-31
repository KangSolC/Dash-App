from dash import Dash, html, dcc, Input, Output, clientside_callback
import dash
import dash_bootstrap_components as dbc
from pages import home, dataSet, distribution, correlation, clustering
from dash_bootstrap_templates import load_figure_template
load_figure_template(["minty", "minty_dark"])
app = Dash(__name__,external_stylesheets=[dbc.themes.MINTY, dbc.icons.FONT_AWESOME], suppress_callback_exceptions=True)


# Navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Dataset", href="/dataset")),
        dbc.NavItem(dbc.NavLink("Distribution", href="/distribution")),
        dbc.NavItem(dbc.NavLink("Correlation", href="/correlation")),
        dbc.NavItem(dbc.NavLink("Clustering", href="/clustering")),
    ],
    brand="Projet d'Analyse de Données / TIW 2023-2024",
    color="primary",
    brand_href="/",
    dark=True,
    className="navbar navbar-expand-lg bg-primary",
)

# Footer
project_url = "https://github.com/KangSolC/Dash-App"

footer_style = {
    'border-top': '1px solid #ccc',
    'display': 'flex',
    'align-items': 'center',
    'justify-content': 'space-between',
    'padding': '8px',
    'color':' #176B87',
    'background-color':'#FAF7F0'
}

footer= html.Footer(
    children=([
        html.Div([
            html.A([
                "Accéder au projet",
                html.I(className="fab fa-github") 
            ],
            href=project_url,
            target="_blank",
            style={'margin-right':'0','color':' #176B87'}
            )
        ]),

        html.Div([
            html.I(className="fas fa-copyright"),
            html.Div("Master TIW 2023-2024 : Hajar AMAKHZOUN, Mouna EL GARB, Cécilia NGUYEN"),
        ],
        style={'display': 'flex', 'align-items': 'center', 'gap': '.5rem'}
    )]),
    style=footer_style)

# Main layout
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        navbar,
        dbc.Container(id="page-content", fluid=True, style={'margin': '20px 0'}),
       
        dash.page_container,
    footer,
    ]
)


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/":
        return home.layout
    if pathname == "/dataset":
        return dataSet.layout
    elif pathname == "/distribution":
        return distribution.layout
    elif pathname == "/correlation":
        return correlation.layout
    elif pathname == "/clustering":
        return clustering.layout
    else:
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognized..."),
            ]
        )

if __name__ == '__main__':
    app.run(debug=False)
    