import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import fundamentus

from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder
from st_aggrid.grid_options_builder import GridOptionsBuilder

# def fix_col_names(df): # Função para tirar os .SA ou corrigir os simbolos
#   return ['IBOV' if col =='^BVSP' else col.rstrip('.SA') for col in df.columns]

# tickers = ['PETR4.SA', 'VALE3.SA', 'CCRO3.SA', '^BVSP', 'USDBRL=X']
# carteira = yf.download(tickers, period='1y')["Adj Close"]#.pct_change()
# #carteira = carteira.rename(columns={'^BVSP': 'Bovespa', 'USDBRL=X': 'Dolar'})
# #carteira = carteira.fillna(method='bfill')
# carteira.columns = fix_col_names(carteira)
# df = pd.DataFrame(np.random.randint(0, 100, 100).reshape(-1, 5), columns=list("abcde"))

# AgGrid(carteira, editable=True, fit_columns_on_grid_load=True)
# # AgGrid(carteira)
# # AgGrid(df)
df = pd.DataFrame(np.random.randint(0, 50, 50).reshape(-1, 5), columns=list("abcde"))
# AgGrid(df, editable=True)


# df = fundamentus.get_resultado()
# df.reset_index(inplace=True)
# df.columns=['Papel', 'Cotação', 'P/L','P/VP', 'PSR' ,'Div Yield', 'P/Ativos', 'P/Cap Giro', 'P/EBIT', 'P/Ativ Circ Liq', 
#             'EV/EBIT','EV/EBITDA', 'Marg EBIT', 'Marg Liq', 'ROIC', 'ROE', 'Liq Corr', 'Vol $ méd (2m)', 'Patrim Liq', 'Div Br/ Patrim', 'Cres Rec (5a)']


gb = GridOptionsBuilder.from_dataframe(df)

gb.configure_pagination()
gb.configure_side_bar()
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
gridOptions = gb.build()

AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True)
