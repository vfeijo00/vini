from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd

import numpy as np
import dash


 
import plotly.express as px
import plotly.graph_objects as go

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

load_figure_template("solar")   #importando template que será utlizado nos gráficos plotly

app = dash.Dash(external_stylesheets = [dbc.themes.DARKLY])    #importando tema "darkly" do bootstrap que será usado no layout

server = app.server

df_data = pd.read_csv("supermarket_sales.csv")
df_data["Date"] = pd.to_datetime(df_data["Date"])

# =========  Layout  =========== #
app.layout = html.Div(children=[
    dbc.Row([   
        dbc.Col([
            dbc.Card([
                html.H3("PIMENTA DE ÁVILA", style={"margin-bottom":"2px","color":"cyan","font-family":"Times New Roman", "font-size":"24px"}),
                html.Hr(style={"margin":"2px"}),
                html.H3("CONSULTORIA LTDA.", style={"margin-top":"4px","color":"cyan","font-family":"Times New Roman", "font-size":"22px"}),
                html.H4("Dashboard Interativo Teste", style={"font-size":"15px"}),
                html.H5("Cidades:"),
                dcc.Checklist(df_data["City"].value_counts().index,              #pega o índice de cada cidade na coluna "cidade", retirando-se os valores repetidos
                            value = df_data["City"].value_counts().index, 
                            id = 'chk1',
                            inputStyle={"margin-right":"5px", "margin-left":"20px"}),

                html.H5("Variável de análise",style={"margin-top":"10px"}),
                dcc.RadioItems(["gross income", 'Rating'],    #lista com esses dois nomes
                            value = "gross income", 
                            id = 'main_variable',
                            inputStyle={"margin-right":"5px", "margin-left":"20px"}),

            ], style={"height":"90vh", "margin":"20px", "margin-right":"5px","padding":"20px"})
        ], sm=2, md=2),

        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id = 'city_fig'),
                ], sm=4, md=4),

                dbc.Col([
                    dcc.Graph(id = 'pay_fig'),
                ], sm=4, md=4),

                dbc.Col([
                    dcc.Graph(id = 'gender_fig'),
                ],sm=4, md=4)
            ]),

            dbc.Row([
                dcc.Graph(id = 'income_per_date_fig'),
            ]),
            dbc.Row([
                dcc.Graph(id = 'income_per_product_fig'),
            ])  
        ], sm=10, md=10)    
    ]),
])

# =========  Callbacks  =========== #
@app.callback([
            Output('city_fig', 'figure'),
            Output('pay_fig', 'figure'),
            Output('gender_fig', 'figure'),
            Output('income_per_product_fig', 'figure'),
            Output('income_per_date_fig', 'figure')],
            [
            Input('chk1', 'value'), 
            Input('main_variable', 'value')]
)
def apresentar_graficos(cities, main_variable):
    operation = np.sum if main_variable == "gross income" else np.mean

    df_filtered = df_data[df_data["City"].isin(cities)]  #isin = apenas se o df_data[city] estiver contido na lista de cidades passada na funçao
    df_city = df_filtered.groupby("City")[main_variable].apply(operation).to_frame().reset_index()
    df_payment = df_filtered.groupby("Payment")[main_variable].apply(operation).to_frame().reset_index()
    df_product_income = df_filtered.groupby(['Product line', 'City'])[main_variable].apply(operation).to_frame().reset_index()
    df_gender = df_filtered.groupby(["Gender", "City"])[main_variable].apply(operation).to_frame().reset_index()
    df_income_time = df_filtered.groupby('Date')[main_variable].apply(operation).to_frame().reset_index()
    
    fig_city = px.bar(df_city, x='City', y=main_variable)
    fig_payment = px.bar(df_payment, x=main_variable, y='Payment', orientation = 'h')
    fig_product_income = px.bar(df_product_income, x=main_variable, y='Product line', color='City', orientation='h')
    fig_gender = px.bar(df_gender, x='Gender', y=main_variable, color="City")
    fig_income_date = px.bar(df_income_time, x="Date", y=main_variable,)


    for fig in [fig_city,fig_payment,fig_gender,fig_income_date]:
        fig.update_layout(margin=dict(l=0, r=0, t=20, b=20), height = 200, template="solar") #dicionário contendo margens E TEMPLATE DARK do PLOTLY
    
    fig_product_income.update_layout(margin=dict(l=0, r=0, t=20, b=20), height = 500, template="solar")
    return fig_city, fig_payment, fig_gender, fig_product_income, fig_income_date

if __name__ == "__main__":
    app.run_server(port=8051, debug=False)