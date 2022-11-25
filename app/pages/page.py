from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from os import path
import pickle


def get_navbar():
    return dbc.Navbar(
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
                                    "GNSS - RFI",
                                    className="ms-2",
                                    href="/",
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
                                                        href="/buromo",
                                                        id="buromo-link",
                                                    ),
                                                    dbc.DropdownMenuItem(
                                                        "Kaliningrad",
                                                        href="/kal",
                                                        id="kal-link",
                                                    ),
                                                    dbc.DropdownMenuItem(
                                                        "Cyprus",
                                                        href="/cyp",
                                                        id="cyp-link",
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
                                        # dbc.NavItem(dbc.NavLink("About", href="/")),
                                        dbc.Col(
                                            [
                                                html.Img(
                                                    src="assets/zhaw.png",
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


def load_plots(zone: str):
    with open(path.join("figures", f"fig_jam_map_{zone}.pkl"), "rb") as handle:
        fig_jam_map = pickle.load(handle)
    with open(path.join("figures", f"fig_jam_normalized_{zone}.pkl"), "rb") as handle:
        fig_jam_normalized = pickle.load(handle)
    with open(path.join("figures", f"fig_traffic_map_{zone}.pkl"), "rb") as handle:
        fig_traffic_map = pickle.load(handle)
    with open(path.join("figures", f"hourly_hm_{zone}.pkl"), "rb") as handle:
        jam_git_hm = pickle.load(handle)
    with open(path.join("figures", f"fig_daily_jammed_{zone}.pkl"), "rb") as handle:
        fig_daily_jam = pickle.load(handle)
    with open(path.join("figures", f"fig_simult_ac_jammed_{zone}.pkl"), "rb") as handle:
        fig_simult_ac_jammed = pickle.load(handle)
    with open(path.join("figures", f"jammed_duration_box_{zone}.pkl"), "rb") as handle:
        jammed_duration_box = pickle.load(handle)
    with open(path.join("figures", f"hourly_hm_{zone}.pkl"), "rb") as handle:
        HM_30M = pickle.load(handle)
    return (
        fig_jam_map,
        fig_jam_normalized,
        fig_traffic_map,
        jam_git_hm,
        fig_daily_jam,
        fig_simult_ac_jammed,
        jammed_duration_box,
        HM_30M,
    )


def get_layout(zone: str, navbar):
    (
        fig_jam_map,
        fig_jam_normalized,
        fig_traffic_map,
        jam_git_hm,
        fig_daily_jam,
        fig_simult_ac_jammed,
        jammed_duration_box,
        HM_30M,
    ) = load_plots(zone)

    layout = html.Div(
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
                                        id=f"traffic_hex_{zone}",
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
                                        id=f"jamming_hex_{zone}",
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
                                        id=f"percentage_hex_{zone}",
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
                                        id=f"git_hm_{zone}",
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
                                        id=f"daily_jam_{zone}",
                                    )
                                ],
                                width=6,
                            ),
                            dbc.Col(
                                [
                                    drawFigure(
                                        fig_simult_ac_jammed,
                                        card_header="Simultaneous Aircraft Jammed:",
                                        id=f"simult_ac_{zone}",
                                    )
                                ],
                                width=3,
                            ),
                            dbc.Col(
                                [
                                    drawFigure(
                                        jammed_duration_box,
                                        card_header="Jammed duration per flight:",
                                        id=f"jam_duration_{zone}",
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
    return layout