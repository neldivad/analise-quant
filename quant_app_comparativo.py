import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api
import statsmodels as sm
import cufflinks as cf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import plotly.express as px
import quant_funcao_dados as fd

# tickers = ['PETR4.SA', 'ITUB4.SA', 'VALE3.SA']
tickers = ['^BVSP', 'USDBRL=X','^VIX', '^GSPC', '^DJI','^IXIC', '^RUT', '^FTSE','^N100','^N225', '^HSI', '000001.SS']

precos = fd.precos(tickers, '1y', False)
retornos = precos.pct_change()
variacao = pd.DataFrame()
for ativo in precos.columns:
  variacao[ativo] = ((precos[ativo] / precos[ativo].iloc[0]) - 1) * 100

fig = variacao.iplot(asFigure=True, xTitle='Data', yTitle='%', title='Variação Percentual')
# fig.update_layout(showlegend=True, hovermode="x unified",
#                 #width=650, height=550,
#                 margin=dict(l=0, r=20, b=50, t=50, pad=4),
#                 legend=dict(yanchor="top",y=0.99, xanchor="left", x=0.01)
#                 )
fig.add_layout_image(
        dict(source="https://analisequant-mh2ir.ondigitalocean.app/media/b25913f6835e74fc51249994ddecaf68599311449505c3a07b1c49c4.png",
            xref="x domain", yref="y domain",
            x=0.25, y=0.6,
            sizex=0.5, sizey=0.5,
            opacity=0.2, layer="below")
)
fig.show()
