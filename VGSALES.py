import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
from dash import dash_table
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py
from plotly.subplots import make_subplots
from dash.dash_table.Format import Group

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# css para o dash
colors = {
    'background': '#182D3E',
    'text': '#7FDBFF'
}

# lista de colunas usadas no dash
cols = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Year', 'Name', 'Genre', 'Platform', 'Publisher']

df = pd.read_csv('vgsales.csv', usecols=cols)
df = df[:100:]


# listagens
def remove_repetidos(year):
    y = []
    for i in year:
        if i not in y:
            y.append(i)
    y.sort()
    return y


year = [2006, 1985, 2008, 2009, 1996, 1989, 1984, 2005, 1999, 2007, 2007, 2010, 2013, 2004, 1990, 1988, 1988, 2002,
        2001, 2011, 1988, 1988]

year = remove_repetidos(year)


def remove_repetidos_platform(platform):
    p = []
    for j in platform:
        if j not in p:
            p.append(j)
    p.sort()
    return p


platform = ["Wii", "NES", "GB", "DS", "X360", "PS3", "PS2", "SNES", "GBA", "3DS", "PS4", "N64", "PS", "XB", "PC",
            "2600", "PSP"]

platform = remove_repetidos_platform(platform)

# Subgrupo 1
fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=df["Year"],  # eixo x do grafico
    y=df["NA_Sales"],  # eixo y do grafico
    text=df["Name"],  # nome dos jogos
    name='Vendas América do Norte',  # referencia
    marker_color='blue'  # cor do gráfico
))

fig1.add_trace(go.Bar(
    x=df["Year"],  # eixo x do grafico
    y=df["EU_Sales"],  # eixo y do gráfico
    text=df["Name"],  # nome dos jogos
    name='Vendas Europa',  # referência
    marker_color='green'  # cor
))

fig1.add_trace(go.Bar(
    x=df["Year"],  # eixo x do grafico
    y=df["JP_Sales"],  # eixo y do gráfico
    text=df["Name"],  # nome dos jogos
    name='Vendas Japão',  # referência
    marker_color='red'  # cor
))

fig1.add_trace(
    go.Bar(
        x=df["Year"],  # eixo x do grafico
        y=df["Other_Sales"],  # eixo y do gráfico
        text=df["Name"],  # nome dos jogos
        name='Vendas Outras regiões',  # referência
        marker_color='yellow'  # cor
    ))

fig1.update_layout(barmode='group', xaxis_tickangle=-45, title="Vendas a cada 5 anos", template='plotly_dark')

# Subgrupo 3
# Gráficos
# vendas por gêneros jogos
# NA_Sales
fig3 = go.Figure()

fig3.add_trace(go.Bar(
    y=df["Genre"],
    x=df["NA_Sales"],
    name='Vendas Norte America',
    orientation='h',
    marker_color='blue'))

# EU_Sales
fig3.add_trace(go.Bar(
    y=df["Genre"],
    x=df["EU_Sales"],
    name='Vendas Europa',
    orientation='h',
    marker_color='green'))

# JP_Sales
fig3.add_trace(go.Bar(
    y=df["Genre"],
    x=df["JP_Sales"],
    name='Vendas Japão',
    orientation='h',
    marker_color='red'))

# Other_Sales
fig3.add_trace(go.Bar(
    y=df["Genre"],
    x=df["Other_Sales"],
    name='Vendas Outras Regiões',
    orientation='h',
    marker_color='yellow'))

# mostrando o gráfico
fig3.update_layout(barmode='group', xaxis_tickangle=-45, template='plotly_dark')

# layout do dash
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[

    # primeiro título
    html.Div([
        html.H1(
            children='DashBoard Game Sales',
            style={
                'textAlign': 'center',
                'color': '#91B0CF'
            }),
    ]),

    # segundo título
    html.Div(html.H2(
        children='Vendas de Jogos no Mundo',
        style={
            'textAlign': 'center',
            'color': '#91B0CF'
        })),

    # graficos
    html.Div([
        html.Div([
            html.Div(html.H4(
                children='Vendas no mundo a cada 5 anos',
                style={
                    'width': '60%', 'display': 'inline-block', 'padding': '0 20',
                    'color': '#C6DAE9'
                })),
            dcc.Graph(
                id='example-graph2',
                figure=fig1
            )
        ]),

        # grafico por ano Eu,Na,Other,JP por ano
        html.Div([
            html.Div(html.H4(
                children='Vendas por Ano',
                style={
                    'width': '60%', 'display': 'inline-block', 'padding': '0 20',
                    'color': '#C6DAE9'
                })),

            dcc.Dropdown(
                id='vendas-dropdown',
                # estrutura de repetição para percorrer a listagem feita em year
                options=[{'label': i, 'value': i} for i in year]
            ),
            dcc.Graph(
                id='line-result'
            ),
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),

        # graficos vendas por plataforma
        html.Div([
            html.Div(html.H4(
                children='Vendas por Plataforma',
                style={
                    'width': '60%', 'display': 'inline-block', 'padding': '0 20',
                    'color': '#C6DAE9'
                })),

            dcc.Dropdown(
                id='platform-dropdown',
                # estrutura de repetição para percorrer a listagem feita em platform
                options=[{'label': i, 'value': i} for i in platform]
            ),
            dcc.Graph(
                id='line-result3'
            )
        ], style={'width': '49%', 'float': 'left', 'display': 'inline-block'}),

        html.Div([
            # painel de vendas gênero
            html.Div(html.H4(
                children='Painel de Vendas por Gênero',
                style={
                    'width': '60%', 'display': 'inline-block', 'padding': '0 20',
                    'color': '#C6DAE9'
                })),
            dcc.Graph(
                id='example-graph3',
                figure=fig3
            )
        ]),

        html.Div([
            html.Div(html.H4(
                children='Comparação de Vendas por Publicadora',
                style={
                    'width': '60%', 'display': 'inline-block', 'padding': '0 20',
                    'color': '#C6DAE9'
                })),
            dcc.Slider(
                id='eu_na-slider',
                min=df['Year'].min(),
                max=df['Year'].max(),
                value=df['Year'].min(),
                marks={str(year2): str(year2) for year2 in year},
                step=None
            ),
            dcc.Graph(id='eu_na-with-slider'),
        ]),

        html.Div([
            dcc.Slider(
                id='jp_other-slider',
                min=df['Year'].min(),
                max=df['Year'].max(),
                value=df['Year'].min(),
                marks={str(year3): str(year3) for year3 in year},
                step=None
            ),
            dcc.Graph(id='jp_other-with-slider'),
        ]),

        html.Div([
            html.Div(html.H4(
                children='Tabela Informativa',
                style={
                    'width': '60%', 'display': 'inline-block', 'padding': '0 20',
                    'color': '#C6DAE9'
                })),

            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i}
                         for i in df.columns],
                data=df.to_dict('records'),
                style_cell=dict(textAlign='left'),
                style_header=dict(backgroundColor="paleturquoise"),
                style_data=dict(backgroundColor="lavender")
            )
        ])

    ]),
])


# subgrupo 1
@app.callback(
    Output('line-result', 'figure'),
    [Input('vendas-dropdown', 'value')])
def update_output(value):
    # dados filtrados do NA_Sales
    df_filtered = df[df.Year == value]
    fig_slider = go.Figure()
    fig_slider.add_trace(go.Bar(
        x=df_filtered["Year"],  # eixo x do grafico
        y=df_filtered["NA_Sales"],  # eixo y do gráfico
        text=df["Name"],  # nome dos jogos
        name='Vendas em Norte America',  # referência
        marker_color='blue'  # cor
    ))

    fig_slider.add_trace(go.Bar(
        x=df_filtered["Year"],  # eixo x do grafico
        y=df_filtered["EU_Sales"],  # eixo y do gráfico
        text=df["Name"],  # nome dos jogos
        name='Vendas Europa',  # referência
        marker_color='green'  # cor
    ))
    fig_slider.add_trace(go.Bar(
        x=df_filtered["Year"],  # eixo x do grafico
        y=df_filtered["JP_Sales"],  # eixo y do gráfico
        # text = df_filtered["Name"], # nome dos jogos
        name='Vendas no Japão',  # referência
        marker_color='red'  # cor
    ))

    fig_slider.add_trace(go.Bar(
        x=df_filtered["Year"],  # eixo x do grafico
        y=df_filtered["Other_Sales"],  # eixo y do gráfico
        # text =df_filtered["Name"], # nome dos jogos
        name='Vendas em Outras regiões',  # referência
        marker_color='yellow'  # cor
    ))

    fig_slider.update_layout(transition_duration=500, title="Vendas por Ano no mundo", template='plotly_dark')

    return fig_slider


@app.callback(
    Output('line-result3', 'figure'),
    [Input('platform-dropdown', 'value')])
def update_output(value):
    # o resultado será agrupado pela data de pagamento utilizando a soma dos valores
    # ao final, resetamos o índice para a geração do gráfico
    df_filtered2 = df[df.Platform == value]

    fig_platform = go.Figure()
    fig_platform.add_trace(go.Bar(
        x=df_filtered2["Platform"],  # eixo x do grafico
        y=df_filtered2["NA_Sales"],  # eixo y do gráfico
        name='Vendas nos Estados Unidos',
        marker_color='blue'  # cor
    ))

    fig_platform.add_trace(go.Bar(
        x=df_filtered2["Platform"],  # eixo x do grafico
        y=df_filtered2["EU_Sales"],  # eixo y do gráfico
        name='Vendas na Europa',  # referência
        marker_color='green'  # cor
    ))

    fig_platform.add_trace(go.Bar(
        x=df_filtered2["Platform"],  # eixo x do grafico
        y=df_filtered2["JP_Sales"],  # eixo y do gráfico
        name='Vendas no Japão',  # referência
        marker_color='red'  # cor
    ))

    fig_platform.add_trace(go.Bar(
        x=df_filtered2["Platform"],  # eixo x do grafico
        y=df_filtered2["Other_Sales"],  # eixo y do gráfico
        name='Vendas em Outras regiões',  # referência
        marker_color='yellow'  # cor
    ))

    fig_platform.update_layout(transition_duration=500, title="Vendas por Plataforma", template='plotly_dark')

    return fig_platform


@app.callback(
    Output('eu_na-with-slider', 'figure'),
    Input('eu_na-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[df.Year == selected_year]

    fig_publisher = px.scatter(filtered_df,
                               x="NA_Sales", y="EU_Sales",
                               color="Publisher", hover_name="Name", size="Year",
                               log_x=True, size_max=55
                               )

    fig_publisher.update_layout(transition_duration=500, template="plotly_dark",
                                title="Vendas por Publicadora em Norte América e Europa")

    return fig_publisher


@app.callback(
    Output('jp_other-with-slider', 'figure'),
    Input('jp_other-slider', 'value'))
def update_figure(selected_year):
    filtered_df2 = df[df.Year == selected_year]

    fig_publisher2 = px.scatter(filtered_df2,
                                x="JP_Sales", y="Other_Sales",
                                color="Publisher", hover_name="Name", size="Year",
                                log_x=True, size_max=55
                                )

    fig_publisher2.update_layout(transition_duration=500, template="plotly_dark",
                                 title="Vendas por Publicadora em Japão e Outras Regiões")

    return fig_publisher2


if __name__ == '__main__':
    app.run_server(debug=True)