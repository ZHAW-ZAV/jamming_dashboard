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
                                                    dbc.DropdownMenuItem(
                                                        "Switzerland",
                                                        href="/ch",
                                                        id="ch-link",
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
                                                html.A(
                                                    [
                                                        html.Img(
                                                            src=dash.get_asset_url(
                                                                "zhaw.png"
                                                            ),
                                                            # src="assets/zhaw.png",
                                                            height="50px",
                                                        ),
                                                    ],
                                                    href="https://www.zhaw.ch/en/engineering/institutes-centres/zav/",
                                                ),
                                            ],
                                            width={"size": "auto"},
                                        ),
                                        dbc.Col(
                                            [
                                                html.A(
                                                    [
                                                        html.Img(
                                                            src=dash.get_asset_url(
                                                                "cyd.png"
                                                            ),
                                                            # src="assets/zhaw.png",
                                                            height="50px",
                                                        ),
                                                    ],
                                                    href="https://www.ar.admin.ch/en/armasuisse-wissenschaft-und-technologie-w-t/cyber-defence_campus.html",
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


def drawFigure(fig, card_header=None, id=None, radio_txt=None, infos=""):
    fig.update_layout(
        autosize=True,
    )
    if radio_txt is None:
        return dbc.Card(
            [
                dbc.CardHeader(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(card_header),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.I(
                                                    className="bi bi-info-circle-fill me-2"
                                                ),
                                            ],
                                            id=f"info_{id}",
                                        ),
                                        dbc.Tooltip(
                                            infos,
                                            target=f"info_{id}",
                                            placement="top",
                                        ),
                                    ],
                                    width="auto",
                                ),
                            ]
                        ),
                    ]
                ),
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
    else:
        return dbc.Card(
            [
                dbc.CardHeader(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(card_header),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        dbc.Checklist(
                                            options=[
                                                {"label": radio_txt, "value": 1},
                                            ],
                                            value=[],
                                            id=id + "_radio",
                                            switch=True,
                                        ),
                                    ],
                                    width="auto",
                                ),
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.I(
                                                    className="bi bi-info-circle-fill me-2"
                                                ),
                                            ],
                                            id=f"info_{id}",
                                        ),
                                        # dbc.Button(
                                        #     "\u2139",
                                        #     id=f"info_{id}",
                                        #     className="mx-2",
                                        #     n_clicks=0,
                                        #     size="sm",
                                        # ),
                                        dbc.Tooltip(
                                            infos,
                                            target=f"info_{id}",
                                            placement="top",
                                        ),
                                    ],
                                    width="auto",
                                ),
                            ]
                        ),
                    ]
                ),
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
    fig_typecodes = pio.read_json(path.join("figures", f"fig_typecodes_{zone}.json"))
    jam_map_norm_anim = pio.read_json(
        path.join("figures", f"fig_jam_normalized_anim_{zone}.json")
    )
    jam_map_norm_anim.update_layout(margin={"l": 0, "b": 0, "t": 0, "r": 0})
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
        jam_map_norm_anim,
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
        jam_map_norm_anim,
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
                                        infos="""The color corresponds 
                                        to the number of observed samples in each
                                        hexadecimal bin.""",
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
                                        card_header="RFI Impacted Flights (absolute):",
                                        id=f"jamming_hex_{zone}",
                                        infos="""Number of received aircraft positions 
                                        reporting a NACp of 0 within each hexadecimal 
                                        bin.""",
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
                                        card_header="RFI Impacted Flights (percentage):",
                                        id=f"percentage_hex_{zone}",
                                        infos="""Percentage of aircraft
                                            affected by RFI per hexadecimal bin.
                                        """,
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
                                        card_header="RFI Intensity:",
                                        id=f"git_hm_{zone}",
                                        radio_txt=["Percentage"],
                                        infos="""Number / Percentage of flights 
                                        influenced by RFI activities per 30-min interval
                                         over the entire observation period. The 
                                         colour varies as a function of the number of 
                                         flights affected by RFI for the corresponding 
                                        30-min interval.
                                        """,
                                    )
                                ],
                                lg=8,
                                md=12,
                            ),
                            dbc.Col(
                                [
                                    drawFigure(
                                        jam_map_norm_anim,
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
                                        card_header="Daily Number of Impacted Flights:",
                                        id=f"daily_jam_{zone}",
                                        infos="Number (blue) and percentage (red) of aircraft affected by RFI per day.",
                                    )
                                ],
                                lg=6,
                                md=12,
                            ),
                            dbc.Col(
                                [
                                    drawFigure(
                                        fig_simult_ac_jammed,
                                        card_header="Simultaneous Jammed Aircraft:",
                                        id=f"simult_ac_{zone}",
                                        infos="""Box plot of the number of aircraft 
                                        simultaneously affected by RFI. \n
                                        The number of aircraft that are affected 
                                        simultaneously by RFI activities in AoI-1 was 
                                        obtained by counting the number of aircraft 
                                        transmitting a NACp value of 0 for each
                                        timestamp.\n This is an important metric because
                                         the more aircraft that are simultaneously 
                                        affected by RFI, the greater the chance that one
                                         or more aircraft will require ATC support.""",
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
                                        card_header="Jammed Duration per Flight:",
                                        id=f"jam_duration_{zone}",
                                        infos="""Box plot of the duration during which 
                                        aircraft affected by RFI in AoI-1 had a NACp 
                                        value of 0.\n Inertial navigation systems (INS) 
                                        drift over time and therefore can only be used 
                                        as a sole source of navigation for a limited 
                                        amount of time. Alternatively, aircraft affected
                                         by RFI will need to revert to other means of 
                                        navigation, such as terrestrial radio navigation
                                         provided they are adequately equipped. 
                                        Consequently, the duration for which an aircraft
                                         is affected by RFI is an important metric to 
                                         monitor. """,
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
                                        card_header="Aircraft Types:",
                                        id=f"fig_typecodes_{zone}",
                                        infos="""Comparison of aircraft type share 
                                        between the whole traffic and the RFI impacted 
                                        flights. """,
                                    )
                                ],
                                lg=6,
                                md=12,
                            ),
                            dbc.Col(
                                [
                                    drawFigure(
                                        fig_jammed_w_GNSS_only,
                                        card_header="Jammed Flights with GNSS Nav Only:",
                                        id=f"fig_jammed_w_GNSS_only_{zone}",
                                        infos="""Occurrence of flights 
                                        affected by RFI for which no inertial nor 
                                        terrestrial navigation capabilities have been 
                                        reported.""",
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
