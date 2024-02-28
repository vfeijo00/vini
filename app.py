from dash import html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import dash
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from pandas import Period
from datetime import datetime, time
import dash_datetimepicker as ddtp
import smtplib                          
from email.message import EmailMessage
import dash_auth
import base64
import requests

load_figure_template("FLATLY")   

def send_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = 'lenildo.ss@gmail.com'
    msg['from'] = user
    password = 'dfqr jhik hozk idwp'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)
    server.quit()

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])
server = app.server

auth=dash_auth.BasicAuth(app, 
                         {'incra':'unb2024'})

df_root = pd.read_csv("dados_concatenados.txt", header=None, delimiter="\t")
df_root.columns = ['Tempo', 'Aceleração em X', 'Aceleração em Y', 'Aceleração em Z', 'Lugar']
df_root[['Dia', 'Hora']] = df_root['Tempo'].str.split(' ', expand=True)
df = df_root.drop(columns=['Tempo'], index=(0))

df['Dia'] = pd.to_datetime(df['Dia'], format='%Y-%m-%d')
df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S.%f').dt.time
df.sort_values(by=['Dia', 'Hora'])

valor_padrao_inicio = df['Dia'].min().strftime('%d/%m/%Y')
valor_padrao_fim = df['Dia'].max().strftime('%d/%m/%Y')
def image_url_to_base64(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        base64_data = base64.b64encode(response.content).decode('utf-8')
        return f"data:image/png;base64,{base64_data}"
    else:
        return None
        
# URLs das imagens no GitHub
logo_unb_url = "https://github.com/vfeijo00/vini/tree/main/asset/logo_unb.png"
logo_incra_url = "https://github.com/vfeijo00/vini/tree/main/assets/logo_incra_negativa.png"

# Convertendo as imagens em base64
base64_logo_unb = image_url_to_base64(logo_unb_url)
base64_logo_incra = image_url_to_base64(logo_incra_url)

# Layout Dash
app.layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Img(src=base64_logo_unb,
                            style={'textAlign': 'left','position': 'absolute', 'top': '15px', 'left': '20px', 'width': '15%'}),
                ], xs=2, sm=2, md=2, lg=2),
                dbc.Col([
                    html.Img(src=base64_logo_incra,
                            style={'position': 'absolute','top': '15px','width': '15%'}),
                ], xs=2, sm=2, md=2, lg=2),
                dbc.Col([
                    html.H1('Dashboard de Monitoramento Estrutural',
                            style={'textAlign': 'center', 'font-family': 'cambria', 'font-size': '35px',
                                   'margin': 'auto', 'color': 'white', 'display': 'flex', 'justify-content': 'center',
                                   'align-items': 'flex-end','height':'50%'}),
                    html.H2('SBN QD 01 Bloco D - Edifício Palácio do Desenvolvimento - Asa Norte, Brasília - DF ',
                            style={'textAlign': 'center', 'font-family': 'cambria', 'font-size': '20px', 'color': 'white','height':'40%'})
                ], xs=8, sm=8, md=6, lg=6),
                dbc.Col(sm=0, md=2, lg=2)

            ], style={'background-color': '#2C3E50','height': '20vh'}),
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.H2('Insira o período de análise:',
                                            style={'font-family': 'cambria', 'font-size': '20px', 'textAlign': 'center'}),
                                    dbc.Row([
                                        dbc.Col([
                                            html.H3('Data Inicial',
                                            style={'margin-right':'5px', 'font-family': 'cambria', 'font-size': '15px', 'textAlign': 'right'}),
                                            html.H3('Data Final',
                                            style={'padding-top':'2px','margin-right':'5px','font-family': 'cambria', 'font-size': '15px', 'textAlign': 'right'})
                                        ],xs=2, sm=2, md=4, lg=4),
                                        dbc.Col([
                                            dcc.Input(id='datetime-range', type='text', value=valor_padrao_inicio,
                                                    placeholder="DD/MM/YYYY", className="mx-auto"),
                                            dcc.Input(id='datetime-range-end', type='text', value=valor_padrao_fim,
                                                    placeholder="DD/MM/YYYY", className="mx-auto"),
                                        ],xs=10, sm=10, md=4, lg=4),
                                        dbc.Col([],xs=0, sm=0, md=4, lg=4)
                                    ], style={'align-items': 'center'}),
                                    dbc.Button('Atualizar Gráfico',
                                               id='update-button',
                                               color='primary',
                                               style={'margin':'5px'}),
                                    dbc.Button('Info',
                                               id='b_info',
                                               color='secondary',
                                               outline=True,
                                               style={'margin':'5px','height': '30px', 'width': '150px', 'display': 'flex',
                                                      'align-items': 'center', 'justify-content': 'center'})

                                ], width=12, style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'}),
                            ], style={'margin-top': '20px'}),
                            dbc.Row([
                                dbc.Col([
                                    html.H3('Digite o valor limite para aceleração em Z:',
                                            style={'font-family': 'cambria', 'font-size': '20px', 'textAlign': 'center'}),
                                    dcc.Input(id="max-aceleracao-z",
                                              type="number",
                                              value=12,
                                              placeholder="Valor Máximo de Aceleração em Z",
                                              style={'margin': 'auto', 'border-radius': '5px', 'textAlign': 'center', 'width': '50%'}),
                                ], sm=12, md=12, lg=12, align='center')
                            ])
                        ], style={'background-color': 'gray', 'height': '80vh', 'border_color': 'gray'})
                    ]),
                    html.P('Lenildo Santos - Contato: lenildo@unb.br', style={'margin':'1px'}),
                    html.P('Vinícius Feijó - Contato: viniciusfeijo360@gmail.com', style={'margin':'1px'}),
                ], sm=12, md=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(id='graph1', style={'width': '100%', 'height': '50vh'}),
                                ], width=12),
                                dbc.Col([
                                    dcc.Graph(id='graph2', style={'width': '100%', 'height': '50vh'}),
                                ], width=12),
                                dbc.Col([
                                    dcc.Graph(id='graph3', style={'width': '100%', 'height': '50vh'}),
                                ], width=12),
                            ], style={'height': '100%'}),

                        ], style={'background-color': 'gray', 'height': '155vh', 'border_color': 'gray'})
                    ])
                ], sm=12, md=9)
            ], style={'height': '160vh'})
        ])
    ], style={'background-color': 'rgba(180, 197, 214, 0.5)'})
], fluid=True)

@app.callback(
    [Output('graph1', 'figure'),
     Output('graph2', 'figure'),
     Output('graph3', 'figure')],
    [Input('update-button', 'n_clicks')],
    [State('datetime-range', 'value'),
     State('datetime-range-end', 'value'),
     State('max-aceleracao-z', 'value')]
)
def update_graph(n_clicks, start_date, end_date, max_aceleracao_z):
    if n_clicks is None:
        return dash.no_update

    start_datetime_obj = pd.to_datetime(start_date, format='%d/%m/%Y')
    end_datetime_obj = pd.to_datetime(end_date, format='%d/%m/%Y')

    filtered_df = df[(df['Dia'] >= start_datetime_obj) & (df['Dia'] <= end_datetime_obj)]

    figs = []
    for aceleracao in ['Aceleração em X', 'Aceleração em Y', 'Aceleração em Z']:
        fig = go.Figure()

        colors = px.colors.qualitative.Set1[:filtered_df['Lugar'].nunique()]
        color_map = dict(zip(filtered_df['Lugar'].unique(), colors))

        for lugar in filtered_df['Lugar'].unique():
            df_lugar = filtered_df[filtered_df['Lugar'] == lugar]
            df_lugar[aceleracao] = pd.to_numeric(df_lugar[aceleracao], errors='coerce')
            df_lugar['Data_Hora'] = df_lugar['Dia'].astype(str) + ' ' + df_lugar['Hora'].astype(str)
            fig.add_scatter(x=df_lugar['Data_Hora'], y=df_lugar[aceleracao], mode='lines', name=f'Lugar: {lugar}',
                            line=dict(color=color_map[lugar]))

        fig.update_layout(title_text=f'{aceleracao}', showlegend=True, template='simple_white',
                          xaxis=dict(title='Data e Hora', tickformat='%d/%m/%Y %H:%M:%S.%f'))
        figs.append(fig)

    # Verificar se a aceleração em Z ultrapassou o valor máximo
    max_aceleracao_z = float(max_aceleracao_z) if max_aceleracao_z else None
    if max_aceleracao_z is not None:
        filtered_df['Aceleração em Z'] = pd.to_numeric(filtered_df['Aceleração em Z'], errors='coerce')
        max_aceleracao_z_observed = filtered_df['Aceleração em Z'].max()
        if max_aceleracao_z_observed > max_aceleracao_z:
            # Encontrando o primeiro ponto onde o limite foi ultrapassado
            row_index = filtered_df[filtered_df['Aceleração em Z'] > max_aceleracao_z].index[0]
            # Extraindo a data, hora e valor da aceleração correspondentes a esse ponto
            event_date = filtered_df.loc[row_index, 'Dia']
            event_time = filtered_df.loc[row_index, 'Hora']
            event_acceleration = filtered_df.loc[row_index, 'Aceleração em Z']
            # Preparando a mensagem do email com os dados do evento
            email_body = f'O valor máximo de aceleração em Z foi ultrapassado (Máximo atingido: {max_aceleracao_z_observed}).\n\nPrimeiro ponto onde ocorreu a ultrapassagem:\nData: {event_date}\nHora: {event_time}\nValor da aceleração: {event_acceleration}'
            send_alert('Alerta de Aceleração em Z', email_body, 'viniciusfeijo360@gmail.com')

    return figs[0], figs[1], figs[2]

if __name__ == "__main__":
    app.run_server(port=8051, debug=True)
