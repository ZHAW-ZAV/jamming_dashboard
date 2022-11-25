import os
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly
import dash
from pages import page


try:
    debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True
except KeyError:
    print("No debug set, defaulting to debug=True")
    debug = True


anim_kali = plotly.io.read_json("assets/anim_kali.json")
anim_kali.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 200
anim_kali.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 100
anim_kali.update_layout(height=800)


# Build App
app = dash.Dash(
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.FLATLY],
)
app.config.suppress_callback_exceptions = True

server = app.server
# %% Index
# Navbar
navbar = page.get_navbar()

jumbotron = html.Div(
    dbc.Container(
        [
            html.H1("Impact of Jamming on Civil Aviation", className="display-3"),
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
            html.P(
                "",
            ),
            html.P(
                dbc.Button("OSN Symposium Paper", color="primary"), className="lead"
            ),
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 bg-default rounded-3",
)

index_page = html.Div(
    [
        navbar,
        jumbotron,
        html.Div([html.H3("GNSS RFI - Time Evolution")]),
        dcc.Graph(
            figure=anim_kali,
            id="anim_kali",
            style={"height": "80%", "width": "80%"},
            # config={
            #     "responsive": True,
            # },
        ),
    ]
)

# %% Pages Loading
buromo_layout = page.get_layout(zone="buromo", navbar=navbar)
try:
    kal_layout = page.get_layout(zone="kal", navbar=navbar)
    cyp_layout = page.get_layout(zone="cyp", navbar=navbar)
except:
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
    else:
        return index_page


@app.callback(Output("buromo-link", "active"), [Input("url", "pathname")])
def set_page_1_active(pathname):
    return pathname == "/buromo"


@app.callback(Output("kal-link", "active"), [Input("url", "pathname")])
def set_page_1_active(pathname):
    return pathname == "/kal"


@app.callback(Output("cyp-link", "active"), [Input("url", "pathname")])
def set_page_1_active(pathname):
    return pathname == "/cyp"


# %% Main
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8050", debug=debug)
