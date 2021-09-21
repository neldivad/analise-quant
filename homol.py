import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import investpy as inv
import ffn
import matplotlib.pyplot as plt
# import plotly.express as px
import altair as alt
from streamlit_vega_lite import vega_lite_component, altair_component
import seaborn as sns
# import cufflinks as cf
# import datetime
from datetime import datetime
# import math
import statsmodels.api
import statsmodels as sm
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

st.set_page_config(  # Alternate names: setup_page, page, layout
    layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
    initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
    page_title=None,  # String or None. Strings get appended with "• Streamlit".
    page_icon=None,  # String, anything supported by st.image, or None.
)

def backtest_sazonalidade():
    st.header('Backtesting de Sazonalidade')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('Escolha o País')
        pais = st.radio('', ('Brasil', 'Estados Unidos'))
    with col2:
        st.write('Escolha entre Ações ou Indices')
        opcao = st.radio('', ('Ações', 'Indices'))

    st.session_state.lista_tickers = ['WEGE3', 'VALE3', 'PETR4', 'BBDC4', 'ITUB4']

    if pais == 'Brasil' and opcao == 'Ações':
        # lista = st.session_state.lista_tickers
        lista = inv.get_stocks_list(country='brazil')
    if pais == 'Brasil' and opcao == 'Indices':
        lista = inv.get_indices_list(country='brazil')
    if pais == 'Estados Unidos' and opcao == 'Ações':
        lista = inv.get_stocks_list(country='united states')
    if pais == 'Estados Unidos' and opcao == 'Indices':
        lista = inv.get_indices_list(country='united states')
    
    ticker = st.selectbox('Selecione a Ação ou Indice desejado', lista)
    if st.button('Mostrar Sazonalidade'):
        try:
            data_inicial = '01/12/1999'
            data_final = datetime.today().strftime('%d/%m/%Y')

            if pais == 'Brasil' and opcao == 'Ações':
                data_inicial = '1999-12-01'
                data_final = datetime.today().strftime('%Y-%m-%d')
                st.session_state.preco = yf.download(ticker + '.SA', start= data_inicial, end=data_final, progress=False)["Adj Close"]
                st.session_state.ticker_ffn = str(ticker + '.SA')

            if pais == 'Brasil' and opcao == 'Indices':
                st.session_state.retornos = \
                st.session_state.preco = \
                inv.get_index_historical_data(ticker, country='brazil', from_date=data_inicial, to_date=data_final,
                                                interval='Daily')['Close']
            if pais == 'Estados Unidos' and opcao == 'Ações':
                st.session_state.preco = \
                    inv.get_stock_historical_data(ticker, country='united states', from_date=data_inicial,
                                                    to_date=data_final,
                                                    interval='Daily')['Close']
            if pais == 'Estados Unidos' and opcao == 'Indices':
                st.session_state.preco = \
                    inv.get_index_historical_data(ticker, country='united states', from_date=data_inicial,
                                                    to_date=data_final,
                                                    interval='Daily')['Close']
            st.session_state.preco = st.session_state.preco.fillna(method='bfill')

        except:
            st.error('Algo errado com o ativo escolhido! Provavelmente seus dados históricos apresentaram algum problema. Escolha outro Ativo.')
    if len(st.session_state.preco) != 0:
        sazonalidade = calc_sazonalidade(st.session_state.preco)
        with st.expander("", expanded=True):
            evento = altair_component(grafico_selecao(sazonalidade, ticker))
            st.markdown('Selecione com o mouse o periodo para verificar a performance. Arraste o periodo para mudar. Clique fora da seleção para selecionar um novo período.')

        selecao = evento.get('x')

        if selecao:
            inicio = datetime(1970, 1, 1) + timedelta(seconds=(int(selecao[0])/1000)) #Calculo para converter o Timestamp negativo, pois o ano é 1900
            fim = datetime(1970, 1, 1) + timedelta(seconds=(int(selecao[1])/1000))
            st.write(inicio.strftime('%d/%b'), '-', fim.strftime('%d/%b'))
            with st.expander("Performance", expanded=True):
                backtest(selecao, st.session_state.ticker_ffn)



@st.cache(suppress_st_warning=True)
def calc_sazonalidade(preco):
    decomposicao = sm.tsa.seasonal.seasonal_decompose(preco, model='additive', period=252) # Decomposição da Série de preços
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
    return df_pivot

@st.cache
def grafico_selecao(sazonalidade, ticker):
	brushed = alt.selection_interval(encodings=['x'], name="brushed")
	return (
			alt.Chart(sazonalidade).mark_line().
			encode(
				alt.X('x', type='temporal', title=''),
				alt.Y('Sazonalidade')
			).
			properties(title='Sazonalidade Aual - ' + ticker,height=300, width=800).
			add_selection(brushed)
	)

def backtest(selecao, ticker):
    st.write(ticker)
    data = ffn.get(ticker, start='2000-01-01', end='2020-12-31')
    data = data.fillna(method='bfill')
    perf = data.calc_stats()

    start_dt = datetime(1970, 1, 1) + timedelta(seconds=(int(selecao[0])/1000)) #Calculo para converter o Timestamp negativo, pois o ano é 1900
    end_dt = datetime(1970, 1, 1) + timedelta(seconds=(int(selecao[1])/1000))

    data_inicio = start_dt.strftime("-%m-%d")
    data_fim = end_dt.strftime("-%m-%d")

    ret = pd.DataFrame()

    for ano in range(data.index.year[0],2021,1):
        inicio = str(ano) + data_inicio
        fim = str(ano) + data_fim
        perf.set_date_range(start=inicio, end=fim)
        stat = perf.stats
        ret = ret.append({'Ano': ano, '%': stat.iloc[3].values, 'DrawDown':stat.iloc[5].values}, ignore_index=True)

    gain = (sum(ret['%'] > 0))
    loss = (sum(ret['%'] < 0))
    gain_pct = (sum(ret['%'] > 0)) / len(ret)
    loss_pct = (sum(ret['%'] < 0)) / len(ret)

    col1, col2, col3, col4, col5 = st.columns(5)
    # col1.metric('Inicio', inicio)
    # col2.metric('Fim', fim)
    col1.metric('Qtde de Trades', len(ret))
    col2.metric('Gain', value=gain)
    col3.metric('Loss', value=loss)
    col4.metric('Gain', value="{0:.0%}".format(gain_pct))
    col5.metric('Loss', value="{0:.0%}".format(loss_pct))

    # ret['Ano'] = ret['Ano'].astype('string')
    # ret.info()c
    ret['%'] = ret['%'].astype('float64')
    # fig = px.bar(ret, x='Ano', y='%', color='%' )

    ## here I'm adding a column with colors
    ret["Color"] = np.where(ret["%"] < 0, 'red', 'green')

    # Plot
    fig = go.Figure()
    fig.add_trace(
        go.Bar(name='Net',
            x=ret['Ano'],
            y=ret['%'],
            marker_color=ret['Color']))
    fig.update_layout(title = 'Retornos por Ano/Trade', barmode='stack', yaxis_tickformat = ',.0%', width=800, height=500)
    st.plotly_chart(fig)

    st.dataframe(ret)
    # return ret, inicio, fim

backtest_sazonalidade()