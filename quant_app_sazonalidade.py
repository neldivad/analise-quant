import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import investpy as inv
#import time
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
#import cufflinks as cf
import datetime
from datetime import date
import math
import statsmodels.api
import statsmodels as sm

retornos = ''
preco = ''
ticker=''
lista = ''
def sazonalidade():
    global retornos
    global preco
    global ticker
    st.header('Análise de Sazonalidade')
    st.write('Escolha o País')
    pais = st.radio('', ('Brasil', 'Estados Unidos'))

    st.write('Escolha entre Ações ou Indices')
    opcao = st.radio('', ('Ações', 'Indices'))

    if pais == 'Brasil' and opcao == 'Ações':
        #lista = inv.get_stocks_list(country='brazil')
        lista = st.session_state.lista_tickers
    if pais == 'Brasil' and opcao == 'Indices':
        lista = inv.get_indices_list(country='brazil')
    if pais == 'Estados Unidos' and opcao == 'Ações':
        lista = inv.get_stocks_list(country='united states')
    if pais == 'Estados Unidos' and opcao == 'Indices':
        lista = inv.get_indices_list(country='united states')

    with st.form(key='Analise_Sazonalidade'):
        ticker = st.selectbox('Selecione a Ação ou Indice desejado', lista)
        if st.form_submit_button(label='Analisar Sazonalidade'):


    # ticker = st.selectbox('Selecione a Ação ou Indice desejado', lista)
    #
    # if st.button('Analisar Sazonalidade'):

            try:
                data_inicial = '01/12/1999'
                data_final = date.today().strftime('%d/%m/%Y')

                # Dados do Investing - Pegar dados periodo Mensal
                if pais == 'Brasil' and opcao == 'Ações':
                    # retornos = \
                    # inv.get_stock_historical_data(ticker, country='brazil', from_date=data_inicial, to_date=data_final,
                    #                               interval='Monthly')['Close'].pct_change(1)
                    # preco = \
                    # inv.get_stock_historical_data(ticker, country='brazil', from_date=data_inicial, to_date=data_final,
                    #                               interval='Daily')['Close']
                    data_inicial = '1999-12-01'
                    data_final = date.today().strftime('%Y-%m-%d')
                    #retornos = yf.download(ticker + '.SA', start= data_inicial, end=data_final, interval='1mo', progress=False)["Adj Close"].pct_change(1)
                    preco = yf.download(ticker + '.SA', start= data_inicial, end=data_final, progress=False)["Adj Close"]
                    data_inicial = '01/12/1999'
                    data_final = date.today().strftime('%d/%m/%Y')
                    retornos = \
                    inv.get_stock_historical_data(ticker, country='brazil', from_date=data_inicial, to_date=data_final,
                                                  interval='Monthly')['Close'].pct_change()


                if pais == 'Brasil' and opcao == 'Indices':
                    retornos = \
                    inv.get_index_historical_data(ticker, country='brazil', from_date=data_inicial, to_date=data_final,
                                                  interval='Monthly')['Close'].pct_change(1)
                    preco = \
                    inv.get_index_historical_data(ticker, country='brazil', from_date=data_inicial, to_date=data_final,
                                                  interval='Daily')['Close']
                if pais == 'Estados Unidos' and opcao == 'Ações':
                    retornos = \
                        inv.get_stock_historical_data(ticker, country='united states', from_date=data_inicial,
                                                      to_date=data_final,
                                                      interval='Monthly')['Close'].pct_change(1)
                    preco = \
                        inv.get_stock_historical_data(ticker, country='united states', from_date=data_inicial,
                                                      to_date=data_final,
                                                      interval='Daily')['Close']
                if pais == 'Estados Unidos' and opcao == 'Indices':
                    retornos = \
                        inv.get_index_historical_data(ticker, country='united states', from_date=data_inicial,
                                                      to_date=data_final,
                                                      interval='Monthly')['Close'].pct_change(1)
                    preco = \
                        inv.get_index_historical_data(ticker, country='united states', from_date=data_inicial,
                                                      to_date=data_final,
                                                      interval='Daily')['Close']
                preco = preco.fillna(method='bfill')
            except:
                st.error('Algo errado com o ativo escolhido! Provavelmente seus dados históricos apresentaram algum problema. Escolha outro Ativo.')


    if len(retornos) != 0:
        analise_sazonalidade()

def analise_sazonalidade():
    with st.beta_expander("Retornos Mensais", expanded=True):
        if st.checkbox('Mapa Retornos Mensais', help='Analisar os retornos mensais do ativo escolhido', value=True):
            # Separar e agrupar os anos e meses
            retorno_mensal = retornos.groupby([retornos.index.year.rename('Year'), retornos.index.month.rename('Month')]).mean()
            # Criar e formatar a tabela pivot table
            tabela_retornos = pd.DataFrame(retorno_mensal)
            try:
                tabela_retornos = pd.pivot_table(tabela_retornos, values='Close', index='Year', columns='Month')
            except:
                tabela_retornos = pd.pivot_table(tabela_retornos, values='Adj Close', index='Year', columns='Month')
            tabela_retornos.columns = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

            # HeatMap Seaborn
            fig, ax = plt.subplots(figsize=(12, 9))
            cmap = sns.color_palette('RdYlGn', 50)
            sns.heatmap(tabela_retornos, cmap=cmap, annot=True, fmt='.2%', center=0, vmax=0.02, vmin=-0.02, cbar=False,
                        linewidths=1, xticklabels=True, yticklabels=True, ax=ax)
            ax.set_title(ticker, fontsize=18)
            ax.set_yticklabels(ax.get_yticklabels(), rotation=0, verticalalignment='center', fontsize='12')
            ax.set_xticklabels(ax.get_xticklabels(), fontsize='12')
            ax.xaxis.tick_top()  # x axis on top
            plt.ylabel('')
            st.pyplot()

            # Media das rentabilidades
            media = pd.DataFrame(tabela_retornos.mean())
            media.columns = ['Média']
            media = media.transpose()
            fig, ax = plt.subplots(figsize=(12, 0.5))
            sns.heatmap(media, cmap=cmap, annot=True, fmt='.2%', center=0, vmax=0.02, vmin=-0.02, cbar=False,
                        linewidths=1, xticklabels=True, yticklabels=True, ax=ax)
            ax.set_yticklabels(ax.get_yticklabels(), rotation=0, verticalalignment='center', fontsize='11')
            st.pyplot()

    with st.beta_expander("Sazonalidade Anual", expanded=True):
        if st.checkbox('Gráfico de Sazonalidade', help='Analisar o comportamento da sazonalidade ao longo dos meses do ano', value=True):
            st.subheader('Sazonalidade Anual')
            mostrar_anos = st.checkbox('Mostrar Anos')


            decomposicao = sm.tsa.seasonal.seasonal_decompose(preco, model='additive', period=251)

            Monthly_seasonal = pd.DataFrame(decomposicao.seasonal.groupby([decomposicao.seasonal.index.year.rename('year'),
                                                                           decomposicao.seasonal.index.month.rename(
                                                                               'month')]).mean())
            Monthly_seasonal = pd.pivot_table(Monthly_seasonal, values='seasonal', index='year', columns='month')
            Monthly_seasonal.columns = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
            Monthly_seasonal = Monthly_seasonal.transpose()
            Monthly_seasonal['Media'] = Monthly_seasonal.mean(axis=1)

            if mostrar_anos :
                fig = Monthly_seasonal.iplot(asFigure=True, xTitle='Meses', yTitle='Sazonalidade',
                                                      title='Sazonalidade Anual - ' + ticker, dimensions = [710,500])
                fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", legend_bgcolor="white")
                st.plotly_chart(fig)
            else:
                fig = Monthly_seasonal['Media'].iplot(asFigure=True, xTitle='Meses', yTitle='Sazonalidade',
                                                      title='Sazonalidade Anual - ' + ticker, dimensions=[725, 500])
                fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", legend_bgcolor="white")
                st.plotly_chart(fig)

            # # Gráfico de Ranking dos Meses
            # tabela_rank_anos = tabela_retornos.rank(axis=1)
            # tabela_rank_meses = tabela_rank_anos.transpose()
            # tabela_descricao = tabela_rank_anos.describe()
            # tabela_descricao = tabela_descricao.transpose()
            # tabela_rank_meses['Media'] = tabela_descricao['mean']
            # fig = tabela_rank_meses.iplot(asFigure=True, xTitle='Meses', yTitle='Ranking', dimensions=(1000, 600),
            #                               title='Ranking dos meses por ano - ' + ticker)
            # st.write(
            #     'Gráfico - Rankings dos meses (Classificação dos meses do menor para o maior rendimento naquele ano) - Clique 2x no item da Legenda para selecionar')
            # st.plotly_chart(fig)


