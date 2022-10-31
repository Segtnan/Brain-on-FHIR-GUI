from dash import Dash, html, dcc, dash_table, Input, Output, State
import plotly.express as px
import pandas as pd
import jaydebeapi as jdbc
import plotly.express as px

conn = jdbc.connect("org.apache.derby.jdbc.ClientDriver", "jdbc:derby://18.195.167.178:6414/gaiandb", ["gaiandb", "passw0rd"], "./derbyclient.jar")
curs = conn.cursor()


app = Dash(__name__)


print(app.get_asset_url('logo.jpg'))
app.layout = html.Div(children=[
    html.Img(src=app.get_asset_url('logo.svg')),

    #background-repeat: no-repeat;
#   background-attachment: fixed;
#background-position: center;
    dcc.Textarea(
        id='query',
        placeholder='Put your SQL query here..',
        value='',
        style={'width': '100%',
               'height': 300,
               'background-image':f'url({app.get_asset_url("logo2.gif")})',
               'background-repeat':'no-repeat',
               'background-attachment':'fixed',
               'background-position':'right top 82px',

               },
    ),
    html.Button('Submit', id='submit-val'),
    html.Button('Location', id='location'),
    dcc.Graph(id="graph"),
    html.Div(id='tbl-div', children=[

    ])

])


@app.callback(
    Output('graph','figure'),
    Input('location','n_clicks'),
    State('query', 'value')
)
def update_location_graph(n_clicks, value):
    if n_clicks:
        curs.execute(value)
        columns = [a[0] for a in curs.description]
        rec = curs.fetchall()

        df = pd.DataFrame(rec, columns = columns)
        fig = px.histogram(df, x="LOCATION")
        return fig
    return {}



@app.callback(
    Output('tbl-div', 'children'),
    Input('submit-val', 'n_clicks'),
    State('query', 'value')
)
def update_output(n_clicks, value):
    if n_clicks:
        curs.execute(value)
        columns = [a[0] for a in curs.description]
        rec = curs.fetchall()

        df = pd.DataFrame(rec, columns = columns)

        return dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
    else:
        return ""
if __name__ == '__main__':
    app.run_server(debug=False)#host= '0.0.0.0',
