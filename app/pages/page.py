from os import path

import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from dash import dcc, html
from dash.dependencies import Input, Output

fig_anim = px.scatter_3d().add_annotation(
    text="Click on any cell on the left to replay scenario.",
    showarrow=False,
    font={"size": 16},
)


def get_navbar():
    return dbc.Navbar(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
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
                                                html.A([
                                                html.Img(
                                                    src=dash.get_asset_url("zhaw.png"),
                                                    # src="assets/zhaw.png",
                                                    height="50px",
                                                ),
                                                 ], 
                                                 href='https://www.zhaw.ch/en/engineering/institutes-centres/zav/'),
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
    fig_jam_map = pio.read_json(path.join("figures", f"fig_jam_map_{zone}.json"))
    fig_traffic_map = pio.read_json(
        path.join("figures", f"fig_traffic_map_{zone}.json")
    )
    fig_jam_normalized = pio.read_json(
        path.join("figures", f"fig_jam_normalized_{zone}.json")
    )
    fig_simult_jammed = pio.read_json(
        path.join("figures", f"fig_simult_jammed_v_{zone}.json")
    )
    fig_git_hm = pio.read_json(path.join("figures", f"git_hm_{zone}.json"))
    fig_daily_jammed = pio.read_json(
        path.join("figures", f"fig_daily_jammed_{zone}.json")
    )
    fig_jam_duration = pio.read_json(
        path.join("figures", f"fig_jam_duration_v_{zone}.json")
    )
    fig_jammed_w_GNSS_only = pio.read_json(
        path.join("figures", f"fig_jammed_w_GNSS_only_{zone}.json")
    )
    fig_jammed_w_GNSS_only.update_layout(
        margin=dict(t=0, r=0, b=0, l=0),
    )
    fig_typecodes = pio.read_json(
        path.join("figures", f"fig_typecodes_{zone}.json")
    )

    return (
        fig_jam_map,
        fig_jam_normalized,
        fig_traffic_map,
        fig_git_hm,
        fig_daily_jammed,
        fig_simult_jammed,
        fig_jam_duration,
        fig_jammed_w_GNSS_only,
        fig_typecodes,
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
        fig_jammed_w_GNSS_only,
        fig_typecodes,
    ) = load_plots(zone)
    styles = {"pre": {"border": "thin lightgrey solid", "overflowX": "scroll"}}
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
                                lg=8,
                                md=12,
                            ),
                            dbc.Col(
                                [
                                    drawFigure(
                                        fig_anim,
                                        card_header="Scenario Replay:",
                                        id=f"anim_{zone}",
                                    )
                                ],
                                lg=4,
                                md=12,
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
                                lg=6,
                                md=12,
                            ),
                            dbc.Col(
                                [
                                    drawFigure(
                                        fig_simult_ac_jammed,
                                        card_header="Simultaneous Aircraft Jammed:",
                                        id=f"simult_ac_{zone}",
                                    )
                                ],
                                lg=3,
                                md=6,
                                xs=12,
                            ),
                            dbc.Col(
                                [
                                    drawFigure(
                                        jammed_duration_box,
                                        card_header="Jammed duration per flight:",
                                        id=f"jam_duration_{zone}",
                                    )
                                ],
                                lg=3,
                                md=6,
                                xs=12,
                            ),
                        ],
                        align="center",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    drawFigure(
                                        fig_typecodes,
                                        card_header="Most common aircraft types:",
                                        id=f"fig_typecodes_{zone}",
                                    )
                                ],
                                lg=6,
                                md=12,
                            ),
                            dbc.Col(
                                [
                                    drawFigure(
                                        fig_jammed_w_GNSS_only,
                                        card_header="Jammed flights having GNSS only:",
                                        id=f"fig_jammed_w_GNSS_only_{zone}",
                                    )
                                ],
                                lg=6,
                                md=12,
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
