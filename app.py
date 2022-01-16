import os
import json
import dash
from dash import dcc, html
from dash.dependencies import Output, Input, State, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from pyleetspeak import LeetSpeaker

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.FLATLY,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
    ],
    suppress_callback_exceptions=True,
)
app.title = "PyLeetSpeak"
app._favicon = "./assets/favicon.ico"

server = app.server

pyleetspeak_img = html.Img(
    src="./assets/favicon.ico",
    alt="pyLeetSpeak Logo",
    # width="5",
    style={
        # "display": "inline-block",
        "width": "1em",
        "height": "1em",
        # "border-color": "black",
        # "border-style": "solid",
        "padding-top": 0,
        "margin-bottom": "0.3em",
    },
)

aida_img = html.Img(
    src="./assets/aida_logo.png",
    alt="AI+DA Logo",
    # width="5",
    style={
        # "display": "inline-block",
        "width": "2.2em",
        "height": "1em",
        # "border-color": "black",
        # "border-style": "solid",
        "padding-top": 0,
        "margin-bottom": "0.3em",
        "margin-left": "0.2em"
    },
)

header = html.Div(
    [
        dbc.Row(
            [
                html.H1(
                    [
                        "Welcome to pyLeetSpeak ",
                        html.Span(children=[pyleetspeak_img, aida_img ]),
                    ],
                    # style={"border-color": "black", "border-style": "solid"},
                    className="display-1",
                ),
            ],
        ),
        html.P(
            "Developed in Applied Intelligence and Data Analysis (AI+DA) group at Polytech University of Madrid",
            className="lead",
        ),
        html.P(
            [
                "You can use this tool in your code installing the PyPi package ",
                html.Span(
                    html.A(
                        children=[html.I(className="fa fa-external-link")],
                        href="https://pypi.org/project/pyleetspeak/",
                    )
                ),
                ".",
            ],
            # className="lead",
        ),
    ],
    className="card-header",  # "toast-header" "modal-header" "offcanvas-header" "card-header"
)

radioitems = html.Div(
    [
        dbc.Label("Choose one"),
        dbc.RadioItems(
            options=[
                {"label": "Random Change", "value": 1},
                {"label": "Get all possible changes", "value": 2},
            ],
            value=1,
            id="radioitems-input",
        ),
    ]
)


dropdown_mode_selection = html.Div(
    [
        dbc.Label("Select a leetspeak mode"),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Mode"),
                dbc.Select(
                    id="dropdown-mode",
                    options=[{"label": i, "value": i} for i in ["Basic"]],
                    value="Basic",
                ),
            ],
            className="mb-3",
        ),
    ]
)

change_prb_slider = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Label(
                        "Select the probability of applying each substitution type ",
                        html_for="slider",
                    ),
                    width={
                        "size": 4,
                        "offset": 0,  # left-margin
                    },
                    style={
                        "margin-right": "-2em"  # the right-element will be attracted if negative
                    },
                    align="center",
                ),
                dbc.Col(
                    dbc.Button(
                        children=[
                            "More info",
                            html.I(
                                className="fa fa-info-circle",
                                style={"margin-left": "0.5em"},
                            ),
                        ],
                        id="popover-change-prb",
                        color="info",
                        outline=True,
                    ),
                    width={"offset": 0},  # X-axis
                    style={"margin-bottom": "1em", "height": "1.8em"},  # Y-axis
                    align="center",
                ),
                dbc.Popover(
                    """For each possible substitution, pyLeetSpeak will randomly choose a number between [0, 1]. 
                    If the random number is equal or lower to the probability of change specified, the substitution type is applied. 
                    Otherwise, the substitution is not used. 
                    Thus, if the selected value = 1, all possible substitutions will occur. If value = 0, text will not be modified""",
                    body=True,
                    target="popover-change-prb",
                    trigger="hover",
                    style={"max-width": "50em"},
                ),
            ],
            # align="start",
            className="g-0",
        ),
        dbc.Row(
            dcc.Slider(
                id={"type": "change-slider", "index": 1},
                min=0,
                max=1,
                step=0.05,
                value=0.5,
                tooltip={"placement": "bottom", "always_visible": True},
                marks={
                    0: {"label": "0", "style": {"font-size": "150%"}},
                    1: {"label": "1", "style": {"font-size": "150%"}},
                },
            ),
        ),
    ]
)


change_frq_slider = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Label(
                        "Select how frequently substitution is applied",
                        html_for="slider",
                    ),
                    width={
                        "size": 4,
                        "offset": 0,  # left-margin
                    },
                    style={
                        "margin-right": "-7em"  # the right-element will be attracted if negative
                    },
                    align="center",
                ),
                dbc.Col(
                    dbc.Button(
                        children=[
                            "More info",
                            html.I(
                                className="fa fa-info-circle",
                                style={"margin-left": "0.5em"},
                            ),
                        ],
                        id="popover-change-frq",
                        outline=True,
                        color="info",
                    ),
                    width={"offset": 0},  # X-axis
                    style={"margin-bottom": "1.2em", "height": "1.8em"},  # Y-axis
                    align="center",
                ),
                dbc.Popover(
                    """
                    For each substitution type applied, this parameter tells pyLeetSpeak how frequently apply the change in the original text.
                    If value = 1, all potential positions will be changed. If value = 0, any change will occur. If value is between (0, 1), pyLeetSpeak calculates the ratio of changes and randomly select the positions where the change will be applied.
                    """,
                    body=True,
                    target="popover-change-frq",
                    trigger="hover",
                    style={"max-width": "50em"},
                ),
            ],
            # align="start",
            className="g-0",
        ),
        dbc.Row(
            dcc.Slider(
                id={"type": "change-slider", "index": 2},
                min=0,
                max=1,
                step=0.05,
                value=0.5,
                tooltip={"placement": "bottom", "always_visible": True},
                marks={
                    0: {"label": "0", "style": {"font-size": "150%"}},
                    1: {"label": "1", "style": {"font-size": "150%"}},
                },
            ),
        ),
    ]
)

input_text = html.Div(
    [
        dbc.Textarea(
            id="leet-input",
            # type= "text",
            size="lg",
            placeholder="Introduce text to leet",
            value=None,
            # style={'width': '100%', 'height': 100},
        ),
        html.Br(),
        dbc.Button("Submit", id="submit-button", type="submit"),
    ]
)

form = dbc.Form(
    [
        html.H3("Parameter selection"),
        radioitems,
        html.Br(),
        dropdown_mode_selection,
        # It will show sliders depending on the radioitem selection
        dbc.Row([dbc.Col(id="sliders_selection", children=[])]),
    ]
)

footer = html.Footer(
    [
        html.P("Author: Álvaro Huertas García"),
        html.P(
            [
                html.I(
                    className="fa fa-envelope",
                    style={"margin-right": "0.5em"},
                ),
                "Email: ",
            ]
            + [
                html.A(
                    "alvaro.huertas.garcia@alumnos.upm.es",
                    href="mailto:alvaro.huertas.garcia@alumnos.upm.es",
                )
            ]
        ),
        html.P(
            [
                html.I(
                    className="fa fa-github",
                    style={"margin-right": "0.5em"},
                ),
                "GitHub: ",
            ]
            + [
                html.A(
                    "Huertas97",
                    href="https://github.com/Huertas97",
                )
            ]
        ),
        html.P(
            [
                html.I(
                    className="fa fa-twitter",
                    style={"margin-right": "0.5em"},
                ),
                "Twitter: ",
            ]
            + [
                html.A(
                    "Huertaspedia",
                    href="https://mobile.twitter.com/huertaspedia",
                )
            ]
        ),
        # fa-linkedin-square
        html.P(
            [
                html.I(
                    className="fa fa-linkedin-square",
                    style={"margin-right": "0.5em"},
                ),
                "LinkedIn: ",
            ]
            + [
                html.A(
                    "Profile",
                    href="https://www.linkedin.com/in/alvaro-huertas-garcia/",
                )
            ]
        ),
    ],
    # style={
    #     # "position": "fixed",
    #     # "background-color": "bs-dark",
    #     # "height": 100,
    #     # "bottom": 0,
    #     # "width": "100%",
    # },
    className="card-footer",
)


body = html.Div(
    [
        form,
        html.Section(),
        html.H3("Leet your text"),
        input_text,
        html.Div(id="leetspeak-output"),
    ],
    # className="card-body",
)
# card-body
layout = dbc.Container(
    children=[
        header,
        html.Br(),
        # form,
        # html.Section(),
        # html.H3("Leet your text"),
        # input_text,
        # html.Div(id="leetspeak-output"),
        body,
        dcc.Store(id="all-output"),
        dcc.Store(id="input-text"),
        dbc.Container(
            footer,
            style={
                # "position": "fixed",
                # "background-color": "black",
                "height": 100,
                "bottom": 0,
                "width": "100%",
            },
            tag="navbar",
        ),
    ],
)

app.layout = layout


@app.callback(
    Output("sliders_selection", "children"), Input("radioitems-input", "value")
)
def display_sliders(radioitems_value):
    # Check if sentiment analysis has been selected to display langauges available
    if (
        radioitems_value != None and radioitems_value == 1
    ):  # if random change has been selected
        sliders = (
            dbc.Form(
                [change_prb_slider, change_frq_slider, html.Hr(), html.Br()],
                # row=True,
            ),
        )
        return sliders
    return html.Div([html.Hr(), html.Br()])


@app.callback(
    [
        Output("leetspeak-output", "children"),
        Output("all-output", "data"),  # Store results
        Output("input-text", "data"),  # Store input text
    ],
    [Input("submit-button", "n_clicks")],
    [
        State("leet-input", "value"),
        State("dropdown-mode", "value"),
        State({"type": "change-slider", "index": ALL}, "value"),
    ],
)
def leeter(n_clicks, text_in, mode, sliders_values):

    if text_in is None:
        raise PreventUpdate

    # Si introducen valores en los sliders estamos en modo cmabio aleatorio
    elif sliders_values:
        change_prb, change_frq = sliders_values
        res = LeetSpeaker(
            text_in=text_in,
            change_prb=change_prb,
            change_frq=change_frq,
            mode=mode.lower(),
            get_all_combs=False,
        ).text2leet()
        return (
            html.Div([html.Br(), html.H4(f"{res}")]),
            json.dumps(res),
            json.dumps(text_in),
        )

    # Si no introdujeron sliders values es modo get all
    else:
        res = LeetSpeaker(
            text_in=text_in,
            mode=mode.lower(),
            get_all_combs=True,
        ).text2leet()

        # pasamos a json type para poder guardarlo con dcc.Store en la sesion y poder trabajar coon elr esultado
        total_number_results = len(list(set(res)))
        res = str(list(set(res)))
        dict_results = {"Input": text_in, "Output": res}
        dict_results = json.dumps(dict_results)
        limit_char_display = 500
        if len(res) >= limit_char_display:  # limiting the number of printed characterd
            display_result = html.Div(
                [
                    html.Br(),
                    dbc.Button(
                        children=[
                            html.I(
                                className="fa fa-download",
                                style={"margin-right": "0.5em"},
                            ),
                            " Download",
                        ],
                        id="download-result-button",
                        color="info",
                        outline=True,
                        className="mt-1",
                    ),
                    dcc.Download(
                        id="result-file",
                        # dict(content="Hello world!", filename="hello.txt") #dict(content=str(res), filename=f"{text_in}_leet_results.txt"),
                    ),
                    html.P(
                        f"WARNING! - Truncated output. You can download the {total_number_results} results clicking on the 'Download' button."
                    ),
                    html.P(f"{res[:limit_char_display]} ... "),
                ]
            )
        else:
            display_result = html.Div(
                [
                    html.Br(),
                    dbc.Button(
                        children=[
                            html.I(
                                className="fa fa-download",
                                style={"margin-right": "0.5em"},
                            ),
                            " Download",
                        ],
                        id="download-result-button",
                        color="info",
                        outline=True,
                        className="mt-1",
                    ),
                    dcc.Download(
                        id="result-file",
                    ),
                    html.H4(f"Total leetspeak resuls: {total_number_results}"),
                    html.H4(f"{res}"),
                ]
            )
        return display_result, dict_results, json.dumps(text_in)


@app.callback(
    Output("result-file", "data"),
    [
        Input("download-result-button", "n_clicks"),
        Input("all-output", "data"),
        Input("input-text", "data"),
    ],
    prevent_initial_call=True,
)
def download(n_cliks, dict_results, text_in):
    if n_cliks:
        if len(text_in.split()) == 1:
            return dict(content=dict_results, filename=f"{text_in}_results.txt")
        else:
            return dict(content=dict_results, filename=f"pyleetspeak_results.txt")


if __name__ == "__main__":
    app.run_server(debug=True)
