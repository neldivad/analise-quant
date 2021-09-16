import streamlit as st
import investpy as inv
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import cufflinks as cf
#import plotly.graph_objects as go
from datetime import datetime
import statsmodels.api
import statsmodels as sm
import ffn
import seaborn as sns
#import locale

st.set_page_config(  # Alternate names: setup_page, page, layout
	layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
	page_title=None,  # String or None. Strings get appended with "• Streamlit".
	page_icon=None,  # String, anything supported by st.image, or None.
)

@st.cache
def puxar_dados(ticker):
    precos = yf.download(ticker, start='2000-01-01', end='2020-12-31', progress=False)['Adj Close']
    precos = precos.fillna(method='bfill')
    return precos

@st.cache
def sazonalidade(precos):
    decomposicao = sm.tsa.seasonal.seasonal_decompose(precos, model='additive', period=252) # Decomposição da Série de preços
    sazonalidade = pd.DataFrame(decomposicao.seasonal) # Cria um dataframe com a parte de sazonalidade
    #Montar a tabela pivot, separando os anos.
    df_pivot= pd.pivot_table(sazonalidade, values='seasonal', index=[sazonalidade.index.month.rename('Mês'), sazonalidade.index.day.rename('Dia')], columns=sazonalidade.index.year)
    df_pivot = df_pivot.fillna(method='bfill')
    df_pivot['Sazonalidade'] = df_pivot.mean(axis=1) # Criar coluna com a média da sazonalidade dos anos/mês
    df_pivot.drop(columns=df_pivot.columns[:-1], inplace=True) # Apagar todos os anos e deixar apenas a coluna da Media
    df_pivot.reset_index(level=[0,1], inplace=True) # Resetar o Multi-Indice isolando o dia e mês em colunas separadas
    df_pivot['Dia'] = df_pivot['Dia'].astype(str) # Muda a coluna para String para poder concatenar depois
    df_pivot['Mês'] = df_pivot['Mês'].astype(str) # Muda a coluna para String para poder concatenar depois
    df_pivot['Data'] = df_pivot['Dia'] + '/' + df_pivot['Mês'] # Cria uma coluna com o Dia e Mês Concatenado
    df_pivot.drop(columns=['Dia', 'Mês'], inplace=True) # Apaga as colunas que não serão usadas
    df_pivot.set_index('Data', inplace=True) # Seta a coluna Data como index
    df_pivot.drop('29/2', inplace=True) # Apaga o dia 29/02, pois dá problema nos calculos de data por só existir em alguns anos.
    # Loop para converter a coluna Data de String para Date Format
    count = 0
    df_pivot['DateTime'] = ''
    for i in range(len(df_pivot)):
        df_pivot['DateTime'][count] = datetime.strptime(df_pivot.index[count], '%d/%m')
        count += 1
    df_pivot.set_index('DateTime', inplace=True)
    return df_pivot

def gerar_grafico():
    hoje = '1900-' + str(datetime.today().strftime(
        '%m-%d'))  # Pega data Atual e coloca no tipo do dataframe (1900 ano que não será utilizado)
    # Gerar o Grafico
    fig = px.line(df_pivot, title='Sazonalidade Anual - ' + ticker, width=1700, height=800)
    if st.checkbox('Mostrar Data Atual'):
        fig.add_vline(hoje)
    fig.update_layout(xaxis_tickformatstops=[dict(dtickrange=[None, 'M1'], value='%b'),
                                             dict(dtickrange=['M1', None], value="%d")],
                      xaxis=dict(tickvals=['1900-01-02', '1900-02-01', '1900-03-01', '1900-04-02', '1900-05-01',
                                           '1900-06-01', '1900-07-02', '1900-08-01', '1900-09-01', '1900-10-02',
                                           '1900-11-01', '1900-12-01']),
                      showlegend=False, hovermode="x unified"
                      )
    fig.update_traces(hovertemplate="<b>%{x|%d/%b}</b>")
    fig.update_yaxes(title_text='Sazonalidade')
    fig.update_xaxes(fixedrange=True, title=None)
    fig.update_yaxes(fixedrange=True)
    st.plotly_chart(fig)



# ticker = 'VALE3.sa'

ticker=st.selectbox("Ticker",['VALE3.SA','DIS'])

precos = puxar_dados(ticker)

df_pivot = sazonalidade(precos)

gerar_grafico()
