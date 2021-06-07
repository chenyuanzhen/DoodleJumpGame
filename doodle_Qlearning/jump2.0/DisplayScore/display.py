import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# connect to db and fetch data
import sqlite3

# stores x coordinates
xaxis = []
# stores y
scores = []
def fetch_data():
    # update score from database
    conn = sqlite3.connect('sco.sqlite')
    c = conn.cursor()
    maxid = -1
    cursor = c.execute("select id,score from info where is_added = 0;")
    for row in cursor:
        maxid = max(maxid,row[0])
        scores.append(row[1])
    sql_update = (f"update info set is_added = 1 where id <= {maxid}")
    
    if maxid != -1:
        cursor = c.execute(sql_update)
        conn.commit()
    
    # construct x axis coordinate
    i = len(xaxis)
    while i < len(scores):
        xaxis.append(i+1)
        i+=1


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('html demo'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ])
)

# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    
    fetch_data()
    # Create the graph with subplots
    fig = go.Figure(data=[go.Scatter(x=xaxis,y=scores)])

    return fig


if __name__ == '__main__':
    app.run_server(debug=False)