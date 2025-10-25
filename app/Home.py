import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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

st.subheader('Visão Cliente')

valor = df['Gasto-Cliente'].sum().item()

col1, col2 = st.columns(2)
col1.metric("Faturamento da Campanha", f"R${valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
col2.metric("Quantidade de Clientes", f"{df.shape[0]}")

col1, col2 = st.columns(2)
col3.metric("Ticket Médio", f"{round(df['Gasto-Cliente'].mean().item(), 2)}")
col4.metric("Média de Visitas no Site", f"{round(df['Visitas-Site-Mes'].mean().item(), 2)}")

# st.markdown('---')

st.subheader('Visão Produto')

valor = df['Gasto-Cliente'].sum().item()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Faturamento Médio com Doces", f"R${round(df['Qtde-Doces'].mean().item(), 2)}")
col2.metric("Faturamento Médio com Frutas", f"R${round(df['Qtde-Frutas'].mean().item(), 2)}")
col3.metric("Faturamento Médio com Carnes", f"R${round(df['Qtde-Carnes'].mean().item(), 2)}")
col4.metric("Faturamento Médio com Peixes", f"R${round(df['Qtde-Peixes'].mean().item(), 2)}")
col5.metric("Faturamento Médio com Vinhos", f"R${round(df['Qtde-Vinhos'].mean().item(), 2)}")

# Hipótese 5. Clientes que compram mais carne também compram mais vinho.
col_graf = st.container()

with col_graf:
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

        st.markdown('---')

    else:
        st.warning('Não foi possível exibir o gráfico da correlação carne-vinho')