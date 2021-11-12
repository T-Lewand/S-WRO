import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
from Dataset import Dataset

app = dash.Dash(__name__)

# ------------------------------------------

dataset = Dataset()
rover1_data = dataset.read_data('20211006', '1')

temp = px.line(rover1_data, x='time', y='temp')
pressure = px.line(rover1_data, x='time', y='pressure')

hex_map = ff.create_hexbin_mapbox(data_frame=rover1_data, lat='B', lon='L', color='temp',
                                  nx_hexagon=20, opacity=0.9,  color_continuous_scale='sunsetdark',
                                  mapbox_style='open-street-map')

# -------------------------------------------

app.layout = html.Div(children=[
    html.H1(children='Sensorowo-roWeRowO'),

    html.Div(children=[
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
        dcc.Graph(id='graph_1', figure=temp)
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
        dcc.Graph(id='graph_2', figure=pressure)
    ], style={'width': '49%', 'display': 'inline-block'}),
    dcc.Graph(
            id='map',
            figure=hex_map
        )
])

@app.callback(
    Output(component_id='graph_1', component_property='figure'),
    Input(component_id='data_selector_1', component_property='value')
)
def func(parameter):
    print(parameter)
    graph = px.line(data_frame=rover1_data, x='time', y=parameter)
    return graph


@app.callback(
    Output(component_id='graph_2', component_property='figure'),
    Input(component_id='data_selector_2', component_property='value')
)
def func(parameter):
    print(parameter)
    graph = px.line(data_frame=rover1_data, x='time', y=parameter)
    return graph


if __name__ == '__main__':
    app.run_server(debug=True)