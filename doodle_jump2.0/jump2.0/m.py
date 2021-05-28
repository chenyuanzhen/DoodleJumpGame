"""
    file name: m.py
    effect: 项目的主函数，表示软件的开始
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
import numpy as np



from dash.dependencies import Input, Output

import multiprocessing

# class Singleton(object):
#     _instance = None
#     def __new__(class_, *args, **kwargs):
#         if not isinstance(class_._instance, class_):
#             class_._instance = object.__new__(class_, *args, **kwargs)
#         return class_._instance

resolution = 20
t = np.linspace(0, np.pi * 2, resolution)
x, y = np.cos(t), np.sin(t)
# Example app.
figure = dict(data=[{'x': [], 'y': []}], layout=dict(xaxis=dict(range=[-1, 1]), yaxis=dict(range=[-1, 1])))
app = dash.Dash(__name__, update_title=None)  # remove "Updating..." from title
app.layout = html.Div([dcc.Graph(id='graph', figure=figure), dcc.Interval(id="interval")])

@app.callback(Output('graph', 'extendData'), [Input('interval', 'n_intervals')])
def update_data(self, n_intervals):
    index = n_intervals % self.resolution
    # tuple is (dict of new data, target trace index, number of points to keep)
    return dict(x=[[self.x[index]]], y=[[self.y[index]]]), [0], 10





