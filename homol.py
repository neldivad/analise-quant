import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

tickers = ['PETR4.SA', 'VALE3.SA', 'EQTL3.SA' , 'CSNA3.SA', 'EMBR3.SA']

ticker = st.selectbox('Ação', tickers)

periodos = ['1mo', '3mo', '1y', '5y', '10y']

periodo_sel = st.selectbox('Selecione o periodo', periodos)

preco = pd.DataFrame(yf.download(ticker, period= periodo_sel)['Adj Close'])

preco['MM20'] = preco['Adj Close'].rolling(20).mean()

# st.line_chart(preco)

fig = go.Figure()
fig.add_trace(go.Scatter(x=preco.index, y=preco['Adj Close'], name = 'Preço'))
fig.add_trace(go.Scatter(x=preco.index, y=preco['MM20'], name= 'MM20'))
fig.update_layout(title='GRAFICO DE PREÇOS')
st.plotly_chart(fig)
