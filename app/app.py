import os
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import dash
from os import path
import pickle
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objs as go


with open(path.join("assets", "fig_jam_map.pkl"), "rb") as handle:
    fig_jam_map = pickle.load(handle)
with open(path.join("assets", "fig_jam_normalized.pkl"), "rb") as handle:
    fig_jam_normalized = pickle.load(handle)
with open(path.join("assets", "fig_traffic_map.pkl"), "rb") as handle:
    fig_traffic_map = pickle.load(handle)
with open(path.join("assets", "hourly_hm.pkl"), "rb") as handle:
    jam_git_hm = pickle.load(handle)
with open(path.join("assets", "fig_daily_jammed.pkl"), "rb") as handle:
    fig_daily_jam = pickle.load(handle)
with open(path.join("assets", "fig_simult_ac_jammed.pkl"), "rb") as handle:
    fig_simult_ac_jammed = pickle.load(handle)
with open(path.join("assets", "jammed_duration_box.pkl"), "rb") as handle:
    jammed_duration_box = pickle.load(handle)

# Navbar
ZHAW_LOGO = path.join("assets", "zhaw.png")


navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            # html.Img(
                            #     src=dash.get_asset_url("logo2.png"),
                            #     height="40px",
                            # ),
                            dbc.NavbarBrand(
                                "Effect of Jamming on Civil Aviation in Eastern Europe Feb - Aug 22",
                                className="ms-2",
                            ),
                        ],
                        width={"size": "auto"},
                    )
                ],
                align="center",
                className="g-0",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Nav(
                                [
                                    dbc.NavItem(
                                        dbc.DropdownMenu(
                                            children=[
                                                dbc.DropdownMenuItem(
                                                    "Romania - Bulgaria - Moldova",
                                                    href="/",
                                                ),
                                                dbc.DropdownMenuItem(
                                                    "Kaliningrad",
                                                    href="/kali",
                                                ),
                                            ],
                                            nav=True,
                                            in_navbar=True,
                                            label="Zone Selection",
                                        )
                                    ),
                                ],
                                navbar=True,
                            )
                        ],
                        width={"size": "auto"},
                    )
                ],
                align="center",
            ),
            dbc.Col(dbc.NavbarToggler(id="navbar-toggler", n_clicks=0)),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Collapse(
                            dbc.Nav(
                                [
                                    dbc.NavItem(dbc.NavLink("About", href="/")),
                                    dbc.Col(
                                        [
                                            html.Img(
                                                src=ZHAW_LOGO,
                                                height="50px",
                                            ),
                                        ],
                                        width={"size": "auto"},
                                    ),
                                ]
                            ),
                            id="navbar-collapse",
                            is_open=False,
                            navbar=True,
                        )
                    )
                ],
                align="center",
            ),
        ],
        fluid=True,
    ),
    color="light",
    dark=False,
)


with open(path.join("assets", "hourly_hm.pkl"), "rb") as handle:
    HM_30M = pickle.load(handle)


def drawFigure(fig, card_header=None, id=None):
    fig.update_layout(
        autosize=True,
    )
    return dbc.Card(
        [
            dbc.CardHeader(card_header),
            dbc.CardBody(
                [
                    html.Div(
                        [
                            dcc.Graph(
                                figure=fig,
                                id=id,
                                style={"height": "100%", "width": "100%"},
                                # config={
                                #     "responsive": True,
                                # },
                            ),
                        ],
                        style={"height": "100%", "width": "100%"},
                        className="h-100",
                    )
                ],
                style={"height": "100%", "width": "100%"},
            ),
        ],
        style={
            "padding": 5,
            "margin": 15,
            "height": "100%",
        },
    )


debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True


# Build App
app = dash.Dash(
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
    external_stylesheets=[dbc.themes.FLATLY],
)
server = app.server

app.layout = html.Div(
    [
        dbc.Container(
            [
                navbar,
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                drawFigure(
                                    fig_traffic_map,
                                    card_header="Traffic Flows:",
                                    id="traffic_hex",
                                ),
                            ],
                            lg=4,
                            md=12,
                            xs=12,
                        ),
                        dbc.Col(
                            [
                                drawFigure(
                                    fig_jam_map,
                                    card_header="Jammed Count:",
                                    id="jamming_hex",
                                )
                            ],
                            lg=4,
                            md=12,
                            xs=12,
                        ),
                        dbc.Col(
                            [
                                drawFigure(
                                    fig_jam_normalized,
                                    card_header="Jammed Percentage:",
                                    id="percentage_hex",
                                )
                            ],
                            lg=4,
                            md=12,
                            xs=12,
                        ),
                    ],
                    align="center",
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                drawFigure(
                                    jam_git_hm,
                                    card_header="Jamming Intensity:",
                                    id="4",
                                )
                            ],
                            width=12,
                        ),
                    ],
                    align="center",
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                drawFigure(
                                    fig_daily_jam,
                                    card_header="Number of jammed flights per day:",
                                    id="daily_jam",
                                )
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                drawFigure(
                                    fig_simult_ac_jammed,
                                    card_header="Simultaneous Aircraft Jammed:",
                                    id="6",
                                )
                            ],
                            width=3,
                        ),
                        dbc.Col(
                            [
                                drawFigure(
                                    jammed_duration_box,
                                    card_header="Jammed duration per flight:",
                                    id="7",
                                )
                            ],
                            width=3,
                        ),
                    ],
                    align="center",
                ),
            ],
            fluid=True,
            style={
                "height": "calc(100vh - 45px)",
            },
        )
    ]
)


# Run app and display result inline in the notebook
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8050", debug=debug)
