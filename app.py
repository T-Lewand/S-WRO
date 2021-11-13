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
#rover1_data = dataset.read_data('20211006', '1')
dates = dataset.get_dates(as_dict=True)
rover1_data = dataset.read_data('20211006', '1')

# -------------------------------------------

app.layout = html.Div(children=[
    html.H1(children='Sensorowo-roWeRowO'),

    html.Div(children=[
        dcc.Dropdown(id='rover_selector',
                     options=[{'label': 'Rower 1', 'value': '1'},
                              {'label': 'Rower 2', 'value': '2'}],
                     value='1', multi=True),
        dcc.Dropdown(id='date_selector',
                     options=dates,
                     value='20211006'),

        dcc.Dropdown(id='data_selector_1',
                     options=[{'label': 'Temperatura', 'value': 'temp'},
                              {'label': 'Ciśnienie', 'value': 'pressure'},
                              {'label': 'Wilgotność', 'value': 'humidity'},
                              {'label': 'Pmy1', 'value': 'pmy1'},
                              {'label': 'Pmy2', 'value': 'pmy2'},
                              {'label': 'Pmy3', 'value': 'pmy3'},
                              {'label': 'Pmy4', 'value': 'pmy4'},
                              {'label': 'Pmy5', 'value': 'pmy5'}]),
        html.Br(),
        dcc.Graph(id='graph_1', figure={})
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Div(children=[
        dcc.Dropdown(id='data_selector_2',
                     options=[{'label': 'Temperatura', 'value': 'temp'},
                              {'label': 'Ciśnienie', 'value': 'pressure'},
                              {'label': 'Wilgotność', 'value': 'humidity'},
                              {'label': 'Pmy1', 'value': 'pmy1'},
                              {'label': 'Pmy2', 'value': 'pmy2'},
                              {'label': 'Pmy3', 'value': 'pmy3'},
                              {'label': 'Pmy4', 'value': 'pmy4'},
                              {'label': 'Pmy5', 'value': 'pmy5'}]),
        html.Br(),
        dcc.Graph(id='graph_2', figure={})
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Div(children=[
        dcc.Dropdown(id='data_selector_3',
                     options=[{'label': 'Temperatura', 'value': 'temp'},
                              {'label': 'Ciśnienie', 'value': 'pressure'},
                              {'label': 'Wilgotność', 'value': 'humidity'},
                              {'label': 'Pmy1', 'value': 'pmy1'},
                              {'label': 'Pmy2', 'value': 'pmy2'},
                              {'label': 'Pmy3', 'value': 'pmy3'},
                              {'label': 'Pmy4', 'value': 'pmy4'},
                              {'label': 'Pmy5', 'value': 'pmy5'}]),
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
        data = dataset.read_data(date, rover[0])
    else:
        data = dataset.read_data(date, rover)

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
        data = dataset.read_data(date, rover[0])
    else:
        data = dataset.read_data(date, rover)

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
        data = dataset.read_data(date, rover[0])

        for i in range(len(rover)):
            try:
                data = pd.concat([data, dataset.read_data(date, rover[i+1])], axis=0)
            except:
                pass
    else:
        print(rover)
        print(isinstance(rover, list))
        data = dataset.read_data(date, rover)

    hex_map = ff.create_hexbin_mapbox(data_frame=data, lat='B', lon='L', color=parameter,
                                      labels={'color': str(parameter)},
                                      nx_hexagon=20, opacity=0.9, color_continuous_scale='sunsetdark',
                                      mapbox_style='open-street-map')
    return hex_map


if __name__ == '__main__':
    app.run_server(debug=True)