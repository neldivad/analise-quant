import streamlit as st
from streamlit.hashing import _CodeHasher
import numpy as np
import pandas as pd
import yfinance as yf
import investpy as inv
import time
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import cufflinks as cf
import datetime
from datetime import date
import math
from st_aggrid import AgGrid

def correlacao(state):
  st.header('Análise de Correlação entre Ativos')
  with st.form(key='Correlacao_Inserir_Ativos'):
    state.tickers_sel = st.multiselect('Insira os Ativos para analisar as correlações', state.lista_tickers)
    if st.form_submit_button(label='Analisar Correlações'): 
      if len(state.tickers_sel) == 0:
        st.error('Lista Vazia. Insira ao menos 1 ativo!')

  if len(state.tickers_sel) != 0: # Se a lista estiver vazia, não mostra nada
    calcular_correlacoes(state)

def fix_col_names(df): # Função para tirar os .SA ou corrigir os simbolos
  return ['IBOV' if col =='^BVSP' else col.rstrip('.SA') for col in df.columns]

def calcular_correlacoes(state):
  tickers = [item + '.SA' for item in state.tickers_sel] # Adicionar o '.SA' nos tickers
  tickers += ['^BVSP', 'USDBRL=X']
  #state.tickers_corr = state.tickers_sel + ['^BVSP', 'USDBRL=X'] # Adiciona os Indices para comparação
  retornos = yf.download(tickers, period='1y', progress=False)["Adj Close"].pct_change()
  retornos = retornos.rename(columns={'^BVSP': 'IBOV', 'USDBRL=X': 'Dolar'}) # Renomeia as Colunas
  retornos = retornos.fillna(method='bfill')
  retornos = retornos[1:] # Apagar primeira linha
  retornos.columns = fix_col_names(retornos) # Corrigir as colunas
  correlacao_full = retornos.corr() # Calcula a correlação entre todo mundo com indices
  correlacao = correlacao_full.drop('IBOV',1) # Cria tabela retirando os Indices (Separar duas comparacoes)
  correlacao = correlacao.drop('IBOV',0)
  correlacao = correlacao.drop('Dolar',1)
  correlacao = correlacao.drop('Dolar',0)

  col1, col2, col3 = st.beta_columns([1,0.1,1])
  with col1:
    st.write('**Correlação dos Ativos com IBOV e Dolar**')
    corr_table_indices = pd.DataFrame(correlacao_full['IBOV'])
    corr_table_indices['Dolar'] = correlacao_full['Dolar']
    corr_table_indices = corr_table_indices.drop('IBOV',0)
    corr_table_indices = corr_table_indices.drop('Dolar',0)

    ordenar = st.selectbox('Ordenar por', ['IBOV', 'Dolar'])
    if ordenar == 'IBOV':
      corr_table_indices = corr_table_indices.sort_values("IBOV",ascending = False)
      corr_table_indices = corr_table_indices.style.background_gradient(cmap="Oranges").format({"IBOV": "{:.0%}", "Dolar": "{:.0%}"})
      st.table(corr_table_indices)
      #st.dataframe(corr_table_indices,width=800,height=400)
    if ordenar == 'Dolar':
      corr_table_indices = corr_table_indices.sort_values("Dolar",ascending = False)
      corr_table_indices = corr_table_indices.style.background_gradient(cmap="Oranges").format({"IBOV": "{:.0%}", "Dolar": "{:.0%}"})
      st.table(corr_table_indices)
      #st.dataframe(corr_table_indices, height=400)

  with col3:
    st.write('**Correlação entre os Ativos**')
    correlacao['Ação 1'] = correlacao.index
    correlacao = correlacao.melt(id_vars = 'Ação 1', var_name = "Ação 2",value_name='Correlação').reset_index(drop = True)
    correlacao = correlacao[correlacao['Ação 1'] < correlacao['Ação 2']].dropna()
    highest_corr = correlacao.sort_values("Correlação",ascending = False)
    highest_corr.reset_index(drop=True, inplace=True) # Reseta o indice
    highest_corr.index += 1 # Iniciar o index em 1 ao invés de 0

    def _color_red_or_green(val): # Função para o mapa de cores da tabela
      color = 'red' if val < 0 else 'green'
      #return 'color: %s' % color
      return 'background-color: %s' % color
              
    #highest_corr = highest_corr.style.applymap(_color_red_or_green, subset=['Correlação']).format({"Correlação": "{:.0%}"}) # Aplicar Cores
    highest_corr = highest_corr.style.background_gradient(cmap="Oranges").format({"Correlação": "{:.0%}"})
              
    st.table(highest_corr)
    #st.dataframe(highest_corr, height=600)
