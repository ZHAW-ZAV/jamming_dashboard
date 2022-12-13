import os

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly
import plotly.express as px
import plotly.io as pio
from dash import dcc, html
from dash.dependencies import Input, Output

from pages import page

try:
    debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True
except KeyError:
    print("No debug set, defaulting to debug=True")
    debug = True


jam_map_anim = pio.read_json(
    os.path.join("figures", "fig_jam_normalized_anim_all.json")
)
jam_map_anim.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 200
jam_map_anim.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 0
jam_map_anim.update_layout(
    height=800, margin={"l": 20, "r": 20, "t": 20, "b": 20}, mapbox=dict(zoom=3)
)


# Build App
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.FLATLY, dbc.icons.BOOTSTRAP],
)
app.config.suppress_callback_exceptions = True
app.title = "GNSS-RFI"
# zhaw_logo = app.get_asset_url("zhaw.png")
server = app.server

# %% Index
# Navbar
navbar = page.get_navbar()

jumbotron = html.Div(
    dbc.Container(
        [
            html.H1("Impact of GNSS-RFI on Civil Aviation", className="display-3"),
            html.P(
                "This dashboard shows an analysis of effect of GNSS RFI on civil "
                "aviation between February and end of August 22 for different zones in "
                "Europe. ",
                className="lead",
            ),
            html.P(
                "Use the navigation bar to select a zone for more details about the "
                "impact of GNSS RFI on civil aviation.",
                className="lead",
            ),
            html.Hr(className="my-2"),
            html.P(
                "ADS-B data from the OpenSky Network has been used to detect flights "
                "impacted by jamming."
            ),
            html.P(
                "A flight has been considered as jammed if its transmitted "
                "Navigation Accuracy Position indicator has a value:"
            ),
            html.Ul(
                id="my-list",
                children=[
                    html.Li("of 0 for more than 60 seconds in total, and"),
                    html.Li("greater than 7 for more than 60 seconds in total."),
                ],
            ),
            html.Hr(className="my-2"),
            html.P("This research was funded by Armasuisse."),
            # html.P(
            #     "",
            # ),
            # html.P(
            #     dbc.Button("OSN Symposium Paper", color="primary"), className="lead"
            # ),
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 bg-default rounded-3",
)

index_page = html.Div(
    [
        navbar,
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [jumbotron],
                            lg=6,
                            md=12,
                            xs=12,
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        dcc.Graph(
                                            figure=jam_map_anim,
                                            id="jam_map_anim",
                                            style={"height": "70%", "width": "100%"},
                                            # config={
                                            #     "responsive": True,
                                            # },
                                        ),
                                    ],
                                    # className="h-100",
                                ),
                            ],
                            lg=6,
                            md=12,
                            xs=12,
                        ),
                    ],
                    style={
                        "max-width": 2000,
                        " margin-left": "auto",
                        " margin-right": "auto",
                    },
                    justify="center",
                    align="center",
                ),
            ],
            fluid=True,
            style={
                "max-width": 2000,
                " margin-left": "auto",
                " margin-right": "auto",
            },
        ),
    ],
)

# %% Pages Loading
buromo_layout = page.get_layout(zone="buromo", navbar=navbar)
try:
    kal_layout = page.get_layout(zone="kal", navbar=navbar)

except Exception as e:
    print("yyyyy", e)
    pass
try:
    cyp_layout = page.get_layout(zone="cyp", navbar=navbar)
except Exception as e:
    print(e)
    pass
try:
    ch_layout = page.get_layout(zone="ch", navbar=navbar)
except Exception as e:
    print(e)
    pass
# %% App Layout
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# %% Callbacks
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/buromo":
        return buromo_layout
    elif pathname == "/kal":
        return kal_layout
    elif pathname == "/cyp":
        return cyp_layout
    elif pathname == "/ch":
        return ch_layout
    else:
        return index_page


@app.callback(Output("buromo-link", "active"), [Input("url", "pathname")])
def set_page_1_active(pathname):
    app.title = "GNSS-RFI - Bu/Ro/Mo"
    return pathname == "/buromo"


@app.callback(Output("kal-link", "active"), [Input("url", "pathname")])
def set_page_1_active(pathname):
    app.title = "GNSS-RFI - Kaliningrad"
    return pathname == "/kal"


@app.callback(Output("cyp-link", "active"), [Input("url", "pathname")])
def set_page_1_active(pathname):
    app.title = "GNSS-RFI - Cyprus"
    return pathname == "/cyp"


@app.callback(Output("ch-link", "active"), [Input("url", "pathname")])
def set_page_1_active(pathname):
    app.title = "GNSS-RFI - Switzerland"
    return pathname == "/ch"


# bit of boilerplate code but doesnt work in for loop...
@app.callback(Output(f"git_hm_kal", "figure"), Input(f"git_hm_kal_radio", "value"))
def select_git_style(selected):
    if len(selected) > 0:
        return pio.read_json(os.path.join("figures", f"git_hm_pct_kal.json"))
    else:
        return pio.read_json(os.path.join("figures", f"git_hm_kal.json"))


@app.callback(
    Output(f"git_hm_buromo", "figure"), Input(f"git_hm_buromo_radio", "value")
)
def select_git_style(selected):
    if len(selected) > 0:
        return pio.read_json(os.path.join("figures", f"git_hm_pct_buromo.json"))
    else:
        return pio.read_json(os.path.join("figures", f"git_hm_buromo.json"))


@app.callback(Output(f"git_hm_cyp", "figure"), Input(f"git_hm_cyp_radio", "value"))
def select_git_style(selected):
    if len(selected) > 0:
        return pio.read_json(os.path.join("figures", f"git_hm_pct_cyp.json"))
    else:
        return pio.read_json(os.path.join("figures", f"git_hm_cyp.json"))


@app.callback(Output(f"git_hm_ch", "figure"), Input(f"git_hm_ch_radio", "value"))
def select_git_style(selected):
    if len(selected) > 0:
        return pio.read_json(os.path.join("figures", f"git_hm_pct_ch.json"))
    else:
        return pio.read_json(os.path.join("figures", f"git_hm_ch.json"))


@app.callback(
    Output("anim_cyp", "figure"),
    Input("git_hm_cyp", "clickData"),
)
def display_click_data(clickData):
    from datetime import timedelta

    t = clickData["points"][0]["x"] + " " + clickData["points"][0]["y"]
    fname = f"{t}.json"
    fig = pio.read_json(os.path.join("animations", "cyp", fname))
    fig.update_layout(
        margin=dict(t=0, r=0, b=0, l=0),
        autosize=True,
    )
    return fig


@app.callback(
    Output("anim_ch", "figure"),
    Input("git_hm_ch", "clickData"),
)
def display_click_data(clickData):
    from datetime import timedelta

    t = clickData["points"][0]["x"] + " " + clickData["points"][0]["y"]
    fname = f"{t}.json"
    fig = pio.read_json(os.path.join("animations", "ch", fname))
    fig.update_layout(
        margin=dict(t=0, r=0, b=0, l=0),
        autosize=True,
    )
    return fig


@app.callback(
    Output("anim_kal", "figure"),
    Input("git_hm_kal", "clickData"),
)
def display_click_data(clickData):
    from datetime import timedelta

    t = clickData["points"][0]["x"] + " " + clickData["points"][0]["y"]
    fname = f"{t}.json"
    fig = pio.read_json(os.path.join("animations", "kal", fname))
    fig.update_layout(
        margin=dict(t=0, r=0, b=0, l=0),
        autosize=True,
    )
    return fig


@app.callback(
    Output("anim_buromo", "figure"),
    Input("git_hm_buromo", "clickData"),
)
def display_click_data(clickData):
    from datetime import timedelta

    t = clickData["points"][0]["x"] + " " + clickData["points"][0]["y"]
    fname = f"{t}.json"
    fig = pio.read_json(os.path.join("animations", "buromo", fname))
    fig.update_layout(
        margin=dict(t=0, r=0, b=0, l=0),
        autosize=True,
    )
    return fig


# %% Main
if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8050)), debug=debug)
