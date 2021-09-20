import streamlit as st
import pandas as pd
import numpy as np
from pandas_datareader import data
import altair as alt
from streamlit_vega_lite import vega_lite_component, altair_component
import yfinance as yf
import statsmodels.api
import statsmodels as sm
from datetime import datetime, timedelta

st.set_page_config(  # Alternate names: setup_page, page, layout
    layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
    initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
    page_title=None,  # String or None. Strings get appended with "• Streamlit".
    page_icon=None,  # String, anything supported by st.image, or None.
)

# start = '2020-1-1'
# end = '2020-12-31'
# source = 'yahoo'

# stocks = data.DataReader("AAPL", start=start ,end=end, data_source=source).reset_index()[["Date", "Close"]]

# stocks.rename(columns={'Date': 'x'}, inplace = True)

# stocks['x'] = stocks['x'].dt.strftime('%Y-%m-%d')



@st.cache(allow_output_mutation=True)
def sazonalidade(ticker):
    precos = yf.download(ticker, start='2000-01-01', end='2020-12-31', progress=False)['Adj Close']
    precos = precos.fillna(method='bfill')
    decomposicao = sm.tsa.seasonal.seasonal_decompose(precos, model='additive', period=252) # Decomposição da Série de preços
    sazonalidade = pd.DataFrame(decomposicao.seasonal) # Cria um dataframe com a parte de sazonalidade
    #Montar a tabela pivot, separando os anos.
    df_pivot= pd.pivot_table(sazonalidade, values='seasonal',
                             index=[sazonalidade.index.month.rename('Mês'),
                                    sazonalidade.index.day.rename('Dia')], columns=sazonalidade.index.year)
    df_pivot = df_pivot.fillna(method='bfill')
    df_pivot['Sazonalidade'] = df_pivot.mean(axis=1) # Criar coluna com a média da sazonalidade dos anos/mês
    df_pivot.drop(columns=df_pivot.columns[:-1], inplace=True) # Apagar todos os anos e deixar apenas a coluna da Media
    df_pivot.reset_index(level=[0,1], inplace=True) # Resetar o Multi-Indice isolando o dia e mês em colunas separadas
    df_pivot['Dia'] = df_pivot['Dia'].astype(str) # Muda a coluna para String para poder concatenar depois
    df_pivot['Mês'] = df_pivot['Mês'].astype(str) # Muda a coluna para String para poder concatenar depois
    df_pivot['Data'] = df_pivot['Dia'] + '/' + df_pivot['Mês'] # Cria uma coluna com o Dia e Mês Concatenado
    df_pivot.drop(columns=['Dia', 'Mês'], inplace=True) # Apaga as colunas que não serão usadas
    df_pivot.set_index('Data', inplace=True) # Seta a coluna data como index
    df_pivot.drop('29/2', inplace=True) # Apaga o dia 29/02, pois dá problema nos calculos de data por só existir em alguns anos.
    # Loop para converter a coluna Data de String para Date Format
    count = 0
    df_pivot['x'] = ''
    for i in range(len(df_pivot)):
        df_pivot['x'][count] = datetime.strptime(df_pivot.index[count], '%d/%m')
        count +=1
    df_pivot['x']=pd.to_datetime(df_pivot.x)

    lista_dias=pd.Series(range(len(df_pivot['x'])))
    for i in range(len(df_pivot['x'])):
        # lista_dias[i]=df_pivot['DateTime'][i].strftime("%Y-%m-%d")
        lista_dias[i] = df_pivot['x'][i].strftime("%d/%b")

    # df_pivot.set_index('DateTime', inplace=True) # Seta a coluna Data como index
    df_pivot['x'] = df_pivot['x'].dt.strftime('%Y-%m-%d')
    return df_pivot, lista_dias


@st.cache
def linechart():
	brushed = alt.selection_interval(encodings=['x'], name="brushed")
	return (
			alt.Chart(stocks).mark_line().
			encode(
				alt.X('x', type='temporal'),
				alt.Y('Sazonalidade')
			).
			properties(height=300, width=800).
			add_selection(brushed)
	)


stocks, lista_dias = sazonalidade('VALE3.SA')

evento = altair_component(linechart())

selecao = evento.get('x')


if selecao:
    inicio = datetime(1970, 1, 1) + timedelta(seconds=(int(selecao[0])/1000)) #Calculo para converter o Timestamp negativo, pois o ano é 1900
    fim = datetime(1970, 1, 1) + timedelta(seconds=(int(selecao[1])/1000))
    st.write(inicio.strftime('%d/%b'), '-', fim.strftime('%d/%b'))

# if selecao:
# 	inicio = datetime.fromtimestamp(int(selecao[0])/1000)
# 	fim = datetime.fromtimestamp(int(selecao[1])/1000)


# 	st.write(inicio.strftime('%Y-%m-%d'), '-', fim.strftime('%Y-%m-%d'))


