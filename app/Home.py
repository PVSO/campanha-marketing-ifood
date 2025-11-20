import os
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pycountry
import streamlit as st

caminho_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
caminho_arquivo = os.path.join(caminho_base, 'data', 'processed', 'iFood.parquet')
df = pd.read_parquet(caminho_arquivo)

st.set_page_config(
    page_title='Dashboard da análise de campanha de Marketing do iFood',
    page_icon='📚',
    layout='wide',
    initial_sidebar_state='collapsed'
)

st.title("🎲 Dashboard de Análise de campanha de Marketing do iFood")

st.markdown('---')

st.subheader('Visão geral da Campanha')

valor = df['Gasto-Cliente'].sum().item()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Faturamento da Campanha", f"R${valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
col2.metric("Quantidade de Clientes", f"{df.shape[0]}")
col3.metric("Ticket Médio", f"{round(df['Gasto-Cliente'].mean().item(), 2)}")
col4.metric("Média de Visitas no Site", f"{round(df['Visitas-Site-Mes'].mean().item(), 2)}")

st.markdown('---')

st.subheader('Visão Clientes')

col_graf_container = st.container()

# Hipótese 3. Clientes solteiros abaixo dos 30 anos gastam mais com produtos do iFood
# do que as outras faixas etárias.
with col_graf_container:
    if not df.empty:
        gasto_etario_civil = df.pivot_table(
            index='Faixa-Etaria',
            columns='Estado_Civil',
            values='Gasto-Cliente',
            aggfunc='sum',
            observed=True
        )

        gasto_etario_civil['Total'] = gasto_etario_civil.sum(axis=1)

        ordem = ['Solteiro', 'Namorando', 'Casado', 'Divorciado', 'Viúvo(a)', 'Total']

        gasto_etario_civil = gasto_etario_civil[ordem]

        gasto_etario_civil_reset = gasto_etario_civil.reset_index().melt(
            id_vars='Faixa-Etaria',
            var_name='Estado_Civil',
            value_name='Gasto-Cliente'
        )

        # Remover Total
        gasto_etario_civil_reset = gasto_etario_civil_reset[gasto_etario_civil_reset['Estado_Civil'] != 'Total']

        # Criar o gráfico
        fig = px.bar(
            gasto_etario_civil_reset,
            x='Faixa-Etaria',
            y='Gasto-Cliente',
            color='Estado_Civil',
            barmode='group',
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        fig.update_layout(
            title={
                'text': 'Clientes solteiros abaixo dos 30 anos gastam mais com produtos do iFood do que as outras faixas etárias.',
                'x': 0
            },
            xaxis_title='Faixa Etária',
            yaxis_title='SUM de Gasto-Cliente',
            yaxis_tickprefix='R$ ',
            yaxis_tickformat=',.0f',
            plot_bgcolor='white',
            bargap=0.15,
            yaxis=dict(
                showgrid=True,
                gridcolor='black',
                gridwidth=1,
                range=[0, gasto_etario_civil_reset['Gasto-Cliente'].max() * 1.2],
                tick0=0,
                dtick= gasto_etario_civil_reset['Gasto-Cliente'].max() / 8,
                zeroline=True,             # <-- mostra a linha do eixo 0
                zerolinecolor='black',     # <-- define a cor
                zerolinewidth=1.5,
            )
        )

        st.plotly_chart(fig, key='Hipótese 3. Clientes solteiros abaixo dos 30 anos gastam mais com produtos do iFood.')
        st.markdown(
            """
                **Conclusão**: O melhor segmento da campanha foram os clientes casados com idade entre 41 e 50 anos, sem filhos e com graduação completa.  
                O pior segmento de clientes foi o de viúvos de todas as faixas-etárias, com idade abaixo dos 30 anos em todos os estados-civis, com 2 ou mais crianças e somente com ensino fundamental.  
                Para maximizar o lucro da próxima campanha, é necessário direcionar as ações ao melhor segmento apresentado e reduzir os investimentos nos outros segmentos, especialmente o mencionado.
            """
        )

    else:
        st.warning('Não foi possível exibir o gráfico da correlação carne-vinho')

st.markdown('---')

col_graf1, col_graf2 = st.columns(2)

# st.markdown("<br><br><br>", unsafe_allow_html=True)

# Hipótese 1. Clientes abaixo dos 30 anos gastam mais com produtos do iFood do que as outras
# faixas etárias.

with col_graf1:
    if not df.empty:
        gasto_etario = pd.pivot_table(
            df,
            index='Faixa-Etaria',
            values='Gasto-Cliente',
            aggfunc='sum',
            observed=True
        ).reset_index()

        gasto_etario['Percentual'] = (gasto_etario['Gasto-Cliente'] / gasto_etario['Gasto-Cliente'].sum()) * 100

        gasto_etario['Percentual'] = gasto_etario['Percentual'].apply(lambda x: f"{x:.2f}%")

        fig = px.bar(
            gasto_etario,
            x='Faixa-Etaria',
            y='Gasto-Cliente',
            text=gasto_etario['Gasto-Cliente'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")),
            color_discrete_sequence=['royalblue']
        )

        fig.update_layout(
            title={
                'text': 'Clientes abaixo dos 30 anos gastam menos com produtos do iFood <br>do que as outras faixas etárias.',
                'x': 0,
                'y': 0.96
            },
            xaxis_title='Faixa-Etaria',
            yaxis_title='SUM de Gasto-Cliente',
            yaxis_tickprefix='R$ ',
            yaxis_tickformat=',.0f',
            plot_bgcolor='white',
            showlegend=False,
            yaxis=dict(
                showgrid=True,
                gridcolor='black',
                gridwidth=1,
                range=[0, gasto_etario['Gasto-Cliente'].max() * 1.2],
                zeroline=True,             # <-- mostra a linha do eixo 0
                zerolinecolor='black',     # <-- define a cor
                zerolinewidth=1.5,
            )
        )

        st.plotly_chart(fig, key='Hipótese 1. Clientes que compram mais carne também compram mais vinho.')
        st.markdown(
            'Para a próxima campanha, priorizar o público entre 41 a 50 anos de idade'
        )

    else:
        st.warning('Não foi possível exibir o gráfico do gasto-etário')

# Hipótese 2. Clientes solteiros gastam menos do que os outros segmentos de clientes.
with col_graf2:
    if not df.empty:
        gasto_civil = pd.pivot_table(
            df,
            index='Estado_Civil',
            values='Gasto-Cliente',
            aggfunc='sum'
        ).reset_index()

        gasto_civil['Percentual'] = (gasto_civil['Gasto-Cliente'] / gasto_civil['Gasto-Cliente'].sum()) * 100

        gasto_civil['Percentual'] = gasto_civil['Percentual'].apply(lambda x: f"{x:.2f}%")

        fig = px.bar(
            gasto_civil,
            x='Estado_Civil',
            y='Gasto-Cliente',
            text=gasto_civil['Gasto-Cliente'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")),
            color_discrete_sequence=['royalblue'],
            category_orders={'Estado_Civil': ['Solteiro', 'Namorando', 'Casado', 'Divorciado', 'Viúvo(a)', 'Total']},
        )

        fig.update_layout(
            title={
                'text': 'Clientes solteiros gastam menos do que os outros segmentos de clientes.',
                'x': 0
            },
            xaxis_title='Estado Civil',
            yaxis_title='SUM de Gasto-Cliente',
            yaxis_tickprefix='R$ ',
            yaxis_tickformat=',.0f',
            plot_bgcolor='white',
            showlegend=False,
            yaxis=dict(
                showgrid=True,
                gridcolor='black',
                gridwidth=1,
                range=[0, gasto_civil['Gasto-Cliente'].max() * 1.2],
                tick0=0,
                dtick= gasto_civil['Gasto-Cliente'].max() / 8,
                zeroline=True,             # <-- mostra a linha do eixo 0
                zerolinecolor='black',     # <-- define a cor
                zerolinewidth=1.5,
            )
        )

        st.plotly_chart(fig, key='Hipótese 2. Clientes solteiros gastam menos do que os outros segmentos de clientes.')
        st.markdown(
            'Públicos **Casados** devem ser priorizados e Viúvos devem ser removidos da próxima campanha.'
        )

    else:
        st.warning('Não foi possível exibir o gráfico do gasto-civil')

col_graf3, col_graf4 = st.columns(2)

# st.markdown("<br><br><br>", unsafe_allow_html=True)

# Hipótese 4. Clientes com crianças em casa compram mais pelo ifood.
with col_graf3:
    if not df.empty:

        gasto_criancas = pd.pivot_table(
            df,
            index='Criancas-Casa',
            values='Gasto-Cliente',
            aggfunc='sum'
        )
        gasto_criancas_reset = gasto_criancas.reset_index()

        fig = px.pie(
            gasto_criancas_reset,
            names='Criancas-Casa',
            values='Gasto-Cliente',
            color_discrete_sequence=px.colors.qualitative.Set1
        )

        fig.update_traces(
            # textposition='inside',
            # textinfo='percent+label',
            hovertemplate='Crianças em Casa: %{label}<br>Gasto: R$ %{value:,.0f}<extra></extra>'
        )

        fig.update_layout(
            legend_title_text='Qtde de Crianças em Casa',
            title={
                'text': 'Clientes com crianças em casa compram mais pelo iFood.',
                'x': 0.5
            },
            title_x=0,
        )

        st.plotly_chart(fig, key='Hipótese 3. Clientes que compram mais carne também compram mais vinho.')
        st.markdown(
            'Clientes sem filhos representam 86% de todo o faturamento da campanha.'
        )

    else:
        st.warning('Não foi possível exibir o gráfico do gasto-etário-civil')

# Faturamento por Formação.
with col_graf4:
    if not df.empty:        
        gasto_formacao = pd.pivot_table(
            df,
            index='Formação',
            values='Gasto-Cliente',
            aggfunc='sum'
        ).reset_index()

        fig = px.bar(
            gasto_formacao,
            x='Formação',
            y='Gasto-Cliente',
            text=gasto_formacao['Gasto-Cliente'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")),
            color_discrete_sequence=['royalblue'],
            category_orders={'Formação': ['Fundamental', 'Medio', 'Graduação', 'Mestrado', 'Doutorado']},
        )

        fig.update_traces(
            textposition='outside',
            textfont_color='black'
        )

        fig.update_layout(
            title={
                'text': 'Faturamento por Formação',
                'x': 0
            },
            xaxis_title='Formação',
            yaxis_title='SUM de Gasto-Cliente',
            yaxis_tickprefix='R$ ',
            yaxis_tickformat=',.0f',
            plot_bgcolor='white',
            # showlegend=False,margin=dict(l=60, r=60, t=60, b=60),
            yaxis=dict(
                showgrid=True,
                gridcolor='black',
                gridwidth=1,
                range=[0, gasto_formacao['Gasto-Cliente'].max() * 1.2],
                zeroline=True,             # <-- mostra a linha do eixo 0
                zerolinecolor='black',     # <-- define a cor
                zerolinewidth=1.5,
            )
        )
        st.plotly_chart(fig, key='Hipótese 4. Clientes que compram mais carne também compram mais vinho.')
        st.markdown(
            'Clientes com **Graduação** representam 52% do faturamento da campanha, trazendo R$ 635 mil.'
        )

    else:
        st.warning('Não foi possível exibir o gráfico do gasto-etário')

st.markdown('---')
st.subheader('Visão Produto')

valor = df['Gasto-Cliente'].sum().item()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Faturamento Médio com Doces", f"R${round(df['Qtde-Doces'].mean().item(), 2)}")
col2.metric("Faturamento Médio com Frutas", f"R${round(df['Qtde-Frutas'].mean().item(), 2)}")
col3.metric("Faturamento Médio com Carnes", f"R${round(df['Qtde-Carnes'].mean().item(), 2)}")
col4.metric("Faturamento Médio com Peixes", f"R${round(df['Qtde-Peixes'].mean().item(), 2)}")
col5.metric("Faturamento Médio com Vinhos", f"R${round(df['Qtde-Vinhos'].mean().item(), 2)}")

st.markdown('---')
# Hipótese 5. Clientes que compram mais carne também compram mais vinho.
col_graf_container_1 = st.container()

with col_graf_container_1:
    if not df.empty:
        gasto_carne_vinho = df.groupby('ID')[['Qtde-Carnes','Qtde-Vinhos']].sum()

        fig = px.scatter(
            gasto_carne_vinho.reset_index(),
            x='Qtde-Carnes',
            y='Qtde-Vinhos',
            title='Clientes que compram mais carne também compram mais vinho.',
            labels={
                'Qtde-Carnes': 'Quantidade de Carne',
                'Qtde-Vinhos': 'Quantidade de Vinho'
            },
            trendline='ols'
        )

        fig.data[1].update(
            line=dict(color='red', width=3)
        )

        st.plotly_chart(fig, use_container_width=True, key='Hipótese 5. Clientes que compram mais carne também compram mais vinho.')
        st.markdown(
            """
                **Conclusão**: O produto Carnes possui o maior faturamento médio, com R$ 565 por compra.
                Além disso, existe uma correlação positiva entre os produtos Vinhos e Carnes com os maiores faturamentos médios.  
                O foco da próxima campanha deve ser na venda desses dois produtos juntos, com ofertas de desconto na compra conjunta.
            """
        )
        st.markdown('---')

    else:
        st.warning('Não foi possível exibir o gráfico da correlação carne-vinho')
