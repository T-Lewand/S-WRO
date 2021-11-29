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
graphs_id = [1,2,3,4,5,6]
graphs_id1 = [1, 2, 3]
graphs_id2 = [4, 5, 6]
# -------------------------------------------

app.layout = html.Div(children=[
    html.H1(children='Sensorowo-roWeRowO'),

    html.Div(children=[
            dcc.Dropdown(id='date_selector',
                        options=dates,
                        value='20211006'),
            dcc.Input(id="start_time", type="text", placeholder="HH:MM:SS", value=None),
            dcc.Input(id="end_time", type="text", placeholder="HH:MM:SS", value=None),
            html.Br()]),
    html.Div(children=[dcc.Dropdown(id='data_selector_{}'.format(i), options=parameters_dict) for i in graphs_id1],
             style={'width':"50%", 'display': 'inline-block'}),
    html.Div(children=[dcc.Dropdown(id='data_selector_{}'.format(i), options=parameters_dict) for i in graphs_id2],
             style={'width':"50%", 'display': 'inline-block'}),
    html.Br(),
    html.Div(children=[dcc.Graph(id='graph_{}'.format(i), figure={}) for i in graphs_id1],
             style={'width':"50%", 'display': 'inline-block'}),
    html.Div(children=[dcc.Graph(id='graph_{}'.format(i), figure={}) for i in graphs_id2],
             style={'width':"50%", 'display': 'inline-block'})
            ])



for i in graphs_id:
    @app.callback(
        Output(component_id='graph_{}'.format(i), component_property='figure'),
        [Input(component_id='data_selector_{}'.format(i), component_property='value'),
         Input(component_id='date_selector', component_property='value'),
         Input(component_id='start_time', component_property='value'),
         Input(component_id='end_time', component_property='value')]
    )
    def func(parameter, date, start_time, end_time):
        data = dataset.read(date, start_time=start_time, end_time=end_time)

        graph = px.line(data_frame=data, x='Time', y=parameter)
        return graph


if __name__ == '__main__':
    app.run_server(debug=True)