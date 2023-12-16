from dash import Dash, html, dcc, Input, Output, clientside_callback
import dash
import dash_bootstrap_components as dbc
import pages

navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                      dbc.NavItem([dbc.NavLink(f"{page['name']}", href=page["relative_path"])for page in dash.page_registry.values()]),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="NavbarSimple",
    brand_href="#",
    color="primary",
    dark=True,
)
