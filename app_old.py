import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
from Dataset import Dataset
import utilities as util
"""
Skrypt aplikacji na frameworku dash
"""

app = dash.Dash(__name__)
# ------------------------------------------

dataset = Dataset()

dates = dataset.get_dates()
data = dataset.read('20211127', 'main')

parameters_dict = [{'label': 'Temperatura', 'value': 'Temperature'},
                    {'label': 'Wilgotność', 'value': 'RH'},
                    {'label': 'Pm 1.0', 'value': 'Pm1.0'},
                    {'label': 'Pm 2.5', 'value': 'Pm2.5'},
                    {'label': 'Pm 10', 'value': 'Pm10'},
                    {'label': 'Formaldehyd', 'value': 'HCHO'}]

# -------------------------------------------

app.layout = html.Div(children=[
    html.H1(children='Sensorowo-roWeRowO'),

    html.Div(children=[
#        dcc.Dropdown(id='rover_selector',              To be inplemented in future
#                     options=[{'label': 'Rower 1', 'value': '1'},
#                              {'label': 'Rower 2', 'value': '2'}],
#                     value='1', multi=True),
        dcc.Dropdown(id='date_selector',
                     options=dates,
                     value='20211006'),

        dcc.Dropdown(id='data_selector_1',
                     options=parameters_dict),
        html.Br(),
        dcc.Graph(id='graph_1', figure={})
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Div(children=[
        dcc.Dropdown(id='data_selector_2',
                     options=parameters_dict),
        html.Br(),
        dcc.Graph(id='graph_2', figure={})
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Div(children=[
        dcc.Dropdown(id='data_selector_3',
                     options=parameters_dict),
        html.Br(),
        dcc.Graph(id='map', figure={})], style={'width': '50%', 'display': 'inline-block', 'padding-left': '25%'})
    ])

@app.callback(
    Output(component_id='graph_1', component_property='figure'),
    [Input(component_id='data_selector_1', component_property='value'),
     Input(component_id='rover_selector', component_property='value'),
     Input(component_id='date_selector', component_property='value')]
)
def func(parameter, rover, date):
    if isinstance(rover, list):
        data = dataset.read(date)
    else:
        data = dataset.read(date)

    graph = px.line(data_frame=data, x='time', y=parameter)
    return graph


@app.callback(
    Output(component_id='graph_2', component_property='figure'),
    [Input(component_id='data_selector_2', component_property='value'),
     Input(component_id='rover_selector', component_property='value'),
     Input(component_id='date_selector', component_property='value')]
)
def func(parameter, rover, date):
    if isinstance(rover, list):
        data = dataset.read(date)
    else:
        data = dataset.read(date)

    graph = px.line(data_frame=data, x='time', y=parameter)
    return graph

@app.callback(
    Output(component_id='map', component_property='figure'),
    [Input(component_id='data_selector_3', component_property='value'),
     Input(component_id='rover_selector', component_property='value'),
     Input(component_id='date_selector', component_property='value')]
)
def func_map(parameter, rover, date):
    if isinstance(rover, list):
        print('----------')
        data = dataset.read(date)

        for i in range(len(rover)):
            try:
                data = pd.concat([data, dataset.read(date)], axis=0)
            except:
                pass
    else:
        print(rover)
        print(isinstance(rover, list))
        data = dataset.read(date)

    hex_map = ff.create_hexbin_mapbox(data_frame=data, lat='B', lon='L', color=parameter,
                                      labels={'color': str(parameter)},
                                      nx_hexagon=20, opacity=0.8, color_continuous_scale='sunsetdark',
                                      mapbox_style='open-street-map')
    return hex_map


if __name__ == '__main__':
    app.run_server(debug=True)