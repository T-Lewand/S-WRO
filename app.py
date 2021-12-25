import datetime
import dateutil.parser
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, MATCH, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objs as go
import pandas as pd

import app_utilities
from Dataset import Dataset
import utilities as util
import app_utilities as app_util
"""
Skrypt aplikacji na frameworku dash
"""

app = dash.Dash(__name__)
# ------------------------------------------

dataset = Dataset()

dates = dataset.get_dates()
parameters_dict = [{'label': 'Temperatura', 'value': 'Temperature'},
                   {'label': 'Wilgotność', 'value': 'RH'},
                   {'label': 'Pm 1.0', 'value': 'Pm1.0'},
                   {'label': 'Pm 2.5', 'value': 'Pm2.5'},
                   {'label': 'Pm 10', 'value': 'Pm10'},
                   {'label': 'Formaldehyd', 'value': 'HCHO'},
                   {'label': 'Os X', 'value': 'd_aX'},
                   {'label': 'Os Y', 'value': 'd_aY'},
                   {'label': 'Os Z', 'value': 'd_aZ'}]

# -------------------------------------------

app.title = 'S-WRO'
app.layout = html.Div(children=[
    dcc.Store(id='data-holder-full'),
    dcc.Store(id='data-holder-slice'),
    html.Div(children=
    html.Img(src="/assets/images/logo.png", className="header-logo-img")),
    html.Div(children=[
        html.Tr(
                html.Td(["Opcja:", dcc.RadioItems(id='data-type', options=[{'label': 'Podstawowe', 'value': 'main'},
                                                                           {'label': 'Akcel', 'value': 'accel'}],
                                                  value='main')], className="radio")),
        html.Tr([
                html.Td(["Wybierz datę:", dcc.Dropdown(id='date_selector', options=dates, value=dates[-1]['value'])],
                        className="date-selector"),
                html.Td(["Wybierz parametr:", dcc.Dropdown(id='dropdown-data-map')],
                        className="date-selector"),

                html.Td(["Wybierz sposób wyświetlania:", dcc.Dropdown(id='dropdown-map-style',
                                                                      options=[{'label': 'Hex', 'value': 'Hex'},
                                                                               {'label': 'Heat map', 'value': 'Heatmap'}],
                                                                      value='Hex')],
                        className="date-selector"),

                html.Td(["Ilość HEX     :", dcc.Input(id='size', type='number', placeholder='Element size', value=20)],
                        className="hex-number"),
                html.Td(["Pokaż trasę:", dcc.Checklist(id='display-path', options=[{'label': '', 'value': 0}])],
                        className="checklist")]),

        dcc.Graph(id='map', figure={}, style={'height': 550}),

        html.Div(children=[
            html.Div(
                html.Tr([
                    html.Td(dcc.Textarea(id='start-time', value='00:00:00'), className="text-area"),
                    html.Td(dcc.Textarea(id='stop-time', value='24:00:00'), className="text-area")]),
                className="text-area-a"),
            dcc.RangeSlider(id='time-selector', min=0, max=23.999, step=1/60, value=[0, 23.999],
                            allowCross=False, tooltip={'placement': 'bottom', 'always_visible': False},
                            className="range-slider",
                            marks={str(h): str(h) for h in range(0, 24)}),
            ]),
    html.Div(children=[
        html.Button("+", id="add-button", n_clicks=None, className="show-button"),
        html.Div(id='graph-container', children=[]),
    ])]
    , className='without-header'),

    html.Div([
        "Created by Sensorowo-rowerowo          ",
        html.A([html.Img(src="/assets/images/icon-facebook.svg", )],
               href="https://www.facebook.com/SKNGeodetow", className="info-contact-social"),
        html.A([html.Img(src="/assets/images/icon-instagram.svg", )],
                href="https://www.instagram.com/skn_geodetow_upwr", className="info-contact-social"),
        html.Img(src="/assets/images/logoSKN_2020.png", className="info-contact-social")],
    className="info-contact")])

@app.callback(
    Output(component_id='dropdown-data-map', component_property='options'),
    Output(component_id='dropdown-data-map', component_property='value'),
    Input(component_id='data-type', component_property='value')
)
def setup(type):
    """
    Data type setup
    """
    if type == 'main':
        parameters_dict = [{'label': 'Temperatura', 'value': 'Temperature'},
                           {'label': 'Wilgotność', 'value': 'RH'},
                           {'label': 'Pm 1.0', 'value': 'Pm1.0'},
                           {'label': 'Pm 2.5', 'value': 'Pm2.5'},
                           {'label': 'Pm 10', 'value': 'Pm10'},
                           {'label': 'Formaldehyd', 'value': 'HCHO'},
                           {'label': 'Os X', 'value': 'd_aX'},
                           {'label': 'Os Y', 'value': 'd_aY'},
                           {'label': 'Os Z', 'value': 'd_aZ'}]

    elif type == 'accel':
        parameters_dict = [{'label': 'Os X', 'value': 'd_aX'},
                           {'label': 'Os Y', 'value': 'd_aY'},
                           {'label': 'Os Z', 'value': 'd_aZ'}]

    default = parameters_dict[0]['value']
    return parameters_dict, default

@app.callback(
    Output(component_id='data-holder-full', component_property='data'),
    Input(component_id='date_selector', component_property='value'),
    Input(component_id='data-type', component_property='value')
)
def load_data(date, type):
    """
    Data loader to page
    """
    if date is None:
        raise PreventUpdate
    data = dataset.read(date, type)
    data_json = data.to_json()
    return data_json

@app.callback(
    Output(component_id='data-holder-slice', component_property='data'),
    Output(component_id='start-time', component_property='value'),
    Output(component_id='stop-time', component_property='value'),
    Input(component_id='time-selector', component_property='value'),
    Input(component_id="date_selector", component_property='value'),
    Input(component_id='data-holder-full', component_property='data')
)
def slice_data(time, date, data):
    """
    Data slicing due time selection
    """
    if date is None:
        raise PreventUpdate
    while data is None:
        raise PreventUpdate

    date = '{}-{}-{}'.format(date[0:4], date[4:6], date[-2::])
    start = app_utilities.to_time(time[0], date)
    stop = app_utilities.to_time(time[1], date)
    data = pd.read_json(data, convert_dates=['Time'])
    data = data[(data["Time"] > start) & (data["Time"] < stop)]
    data = data.to_json()
    start_string = "Start: {}".format(str(start)[11:])
    stop_string = "Stop: {}".format(str(stop)[11:])
    return data, start_string, stop_string

@app.callback(
    Output(component_id='graph-container', component_property='children'),
    Input(component_id="add-button", component_property='n_clicks'),
    State(component_id='graph-container', component_property='children')
)
def add_graph(n_clicks, children):
    if n_clicks is None:
        raise PreventUpdate
    new_graph = html.Div(id={'type':'graph-frame', 'index': n_clicks},
        children=[
        dcc.Graph(id={'type':'graph', 'index': n_clicks}, figure={}),
        dcc.Dropdown(id={'type':'parameter-selector', 'index': n_clicks}, options=parameters_dict,
                     value=parameters_dict[0]['value'], style={'width':"75%", 'display': 'inline-block'}),
        html.Button('-', id={'type': 'remove-button', 'index': n_clicks}, n_clicks=None,
                    style={'width':"25%", 'display': 'inline-block'})
    ], style={'width':"50%", 'display': 'inline-block'})
    children.append(new_graph)
    return children

@app.callback(
    Output(component_id={'type':'graph-frame', 'index': MATCH}, component_property='children'),
    Input(component_id={'type': 'remove-button', 'index': MATCH}, component_property='n_clicks')
)
def remove_graph(n_clicks):
    if n_clicks is None:
        raise PreventUpdate

    return []


@app.callback(
    Output(component_id={'type': 'graph', 'index': MATCH}, component_property='figure'),
    Input(component_id={'type': 'parameter-selector', 'index': MATCH}, component_property='value'),
    State(component_id='data-holder-slice', component_property='data'))
def display(parameter, data):
    """
    Charts
    """
    if data is None:
        raise PreventUpdate

    data_df = pd.read_json(data, convert_dates=['Time'])
    graph = px.line(data_frame=data_df, x='Time', y=parameter)
    return graph

@app.callback(
    Output(component_id='map', component_property='figure'),
    Input(component_id="dropdown-data-map", component_property='value'),
    Input(component_id="dropdown-map-style", component_property='value'),
    Input(component_id='size', component_property='value'),
    Input(component_id='data-holder-slice', component_property='data'),
    Input('display-path', 'value'),
    State(component_id="date_selector", component_property='value')
)
def display_map(parameter, method, size, data, display_path, date):
    """
    Map setup
    """
    if date is None:
        raise PreventUpdate
    elif size < 1:
        raise PreventUpdate
    elif data is None:
        raise PreventUpdate

    data = pd.read_json(data)
    if method == 'Hex':
        map = ff.create_hexbin_mapbox(data_frame=data, lat='Latitude', lon='Longitude', color=parameter,
                                          labels={'color': str(parameter)},
                                          nx_hexagon=size, opacity=0.8, color_continuous_scale='sunsetdark')
    elif method == 'Heatmap':
        map = px.density_mapbox(data_frame=data, lat='Latitude', lon='Longitude', z=parameter, radius=size,
                                color_continuous_scale='sunsetdark')
    if display_path is not None:
        if display_path == [0]:
            path = go.Scattermapbox(mode='lines', lon=data['Longitude'].to_list(), lat=data['Latitude'].to_list(),
                                    name='Trasa', line={'color': 'blue', 'width': 3}, below=0)
            map.add_trace(path)

    center = dataset.data_center(data=data)
    zoom = app_utilities.calc_zoom(data)
    map.update_layout(mapbox_zoom=zoom, mapbox_center_lat=center[0], mapbox_center_lon=center[1],
                      margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      mapbox_style='open-street-map')
    map.update_coloraxes(colorbar={'x': 1, 'y': 0.5, 'xanchor': 'right', 'yanchor': 'middle', 'len': 1})

    return map




if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False)