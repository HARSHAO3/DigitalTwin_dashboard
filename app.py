import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Live Digital Twin Dashboard"),
    dcc.Interval(id='interval-update', interval=5000, n_intervals=0),
    html.Div(id='live-table'),
    dcc.Graph(id='voltage-graph'),
    dcc.Graph(id='current-graph'),
    dcc.Graph(id='temperature-graph')
])

@app.callback(
    [Output('live-table', 'children'),
     Output('voltage-graph', 'figure'),
     Output('current-graph', 'figure'),
     Output('temperature-graph', 'figure')],
    Input('interval-update', 'n_intervals')
)
def update_live(n):
    try:
        res = requests.get("http://localhost:5001/latest").json()
        df = pd.DataFrame(res)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        table = html.Table([
            html.Tr([html.Th(col) for col in df.columns])
        ] + [
            html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
            for i in range(len(df))
        ])

        fig1 = px.line(df, x='timestamp', y='voltage', title='Voltage Over Time')
        fig2 = px.line(df, x='timestamp', y='current', title='Current Over Time')
        fig3 = px.line(df, x='timestamp', y='temperature', title='Temperature Over Time')

        return table, fig1, fig2, fig3
    except Exception as e:
        return html.Div(f"Error: {e}"), {}, {}, {}

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
