import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
#import time
#import matplotlib.pyplot as plt
import plotly.express as px
#import seaborn as sns
#import cufflinks as cf
#import datetime
from datetime import date
import math


def raiox():
  st.header('Raio-X do Mercado')
  df_lista_bolsas = pd.read_csv('./Indices_Bolsas_Mundo.csv')
  count = 0
  df_lista_bolsas['%'] = ''
  for (pais, indice) in zip(df_lista_bolsas['País'], df_lista_bolsas['index_yf']):
      price = yf.download(indice, period='5d', progress=False)['Adj Close']
      change = (((price.iloc[-1] - price.iloc[-2]) / price.iloc[-2]) * 100).round(2)
      df_lista_bolsas['%'][count] = change
      count += 1
  fig = px.choropleth(df_lista_bolsas, locations="Sigla",
                      color='%',
                      range_color=[-50, 50],
                      hover_data=['País', 'Indice'],
                      color_continuous_scale=[(0.00, "red"), (0.50, "red"),
                                              (0.50, "green"), (1.00, "green")])
  fig.update_layout(coloraxis_showscale=False,
                    title_text='Comportamento das Bolsas Mundiais ' + str(date.today().strftime('%d/%m/%Y')))
  # data_final = date.today().strftime('%Y-%m-%d')
  # fig.update_traces(hovertemplate="Teste")
  st.plotly_chart(fig)
  st.markdown('Dados com delay de 15 min.')
  st.markdown('***Página em desenvolvimento e testes***')
