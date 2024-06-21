import requests
import pandas as pd
import io
import yfinance as yf
import matplotlib.pyplot as plt
from decimal import Decimal, getcontext
from dash import Dash, html, dash_table, dcc,callback, Output, Input
#from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import pandas as pd
import plotly.express as px


nse_url = "https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv"

# create Session from 'real' browser
headers = {
    'User-Agent': 'Mozilla/5.0'
}

s = requests.Session()
s.headers.update(headers)

# do a get call now
url = 'https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv'
r = s.get(nse_url)
s.close()

# saving it to pd df for further preprocessing
df_nse = pd.read_csv(io.BytesIO(r.content))
df_nse['SYMBOLNSE']=df_nse['SYMBOL'].astype(str)+'.NS'



data = yf.download(df_nse['SYMBOLNSE'].iloc[1980], start='2019-06-19', end='2024-06-19')
data = data.reset_index()
# Initialize the app
# Initialize the app - incorporate css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(external_stylesheets=external_stylesheets)

app = Dash()

# # App layout
# app.layout = [
#     html.Div(children='NSE Equity Data     '+     df_nse['SYMBOLNSE'].iloc[1980]),
#     # dash_table.DataTable(data=data.to_dict('records'), page_size=10),
#     # dcc.Graph(figure=px.histogram(data, x='Date', y='Close', histfunc='avg'))


#     html.Hr(),
#     dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='controls-and-radio-item'),
#     dash_table.DataTable(data=df.to_dict('records'), page_size=6),
#     dcc.Graph(figure={}, id='controls-and-graph')



# ]





# app.layout = [
#     html.Div(children='NSE Equity Data     '+     df_nse['SYMBOLNSE'].iloc[1980]'),
#     html.Hr(),
#     dcc.RadioItems(options=['Open', 'High', 'Low','Close','Adj Close','Volume'], value='Close', id='controls-and-radio-item'),
#     dash_table.DataTable(data=data.to_dict('records'), page_size=6),
#     dcc.Graph(figure={}, id='controls-and-graph')
# ]



app.layout = [
    html.Div(className='row', children='NSE Equity Data     '+     df_nse['SYMBOL'].iloc[1980],
             style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),

    html.Div(className='row', children=[
        dcc.RadioItems(options=['Open', 'High', 'Low','Close','Adj Close','Volume'],
                       value='Close',
                       inline=True,
                       id='my-radio-buttons-final')
    ]),

    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dash_table.DataTable(data=data.to_dict('records'), page_size=11, style_table={'overflowX': 'auto'})
        ]),
        html.Div(className='six columns', children=[
            dcc.Graph(figure={}, id='histo-chart-final')
        ])
    ])
]

# Add controls to build the interaction
@callback(

    Output(component_id='histo-chart-final', component_property='figure'),
    Input(component_id='my-radio-buttons-final', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(data, x='Date', y=col_chosen, histfunc='avg')
    return fig


# # Add controls to build the interaction
# @callback(
#     Output(component_id='controls-and-graph', component_property='figure'),
#     Input(component_id='controls-and-radio-item', component_property='value')
# )
# def update_graph(col_chosen):
#     fig = px.histogram(data, x='Date', y=col_chosen, histfunc='avg')
#     return fig



# Run the app

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
