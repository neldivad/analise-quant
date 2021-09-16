import streamlit as st
import investpy as inv
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
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
    df_pivot['DateTime'] = ''
    for i in range(len(df_pivot)):
        df_pivot['DateTime'][count] = datetime.strptime(df_pivot.index[count], '%d/%m')
        count +=1

    lista_dias=pd.Series(range(len(df_pivot['DateTime'])))
    for i in range(len(df_pivot['DateTime'])):
        # lista_dias[i]=df_pivot['DateTime'][i].strftime("%Y-%m-%d")
        lista_dias[i] = df_pivot['DateTime'][i].strftime("%d/%b")

    df_pivot.set_index('DateTime', inplace=True) # Seta a coluna Data como index
    return df_pivot, lista_dias

def gerar_grafico():
    start_dt, end_dt = st.select_slider("Selecione o Período", options=lista_dias, value=['02/Jan', '31/Dec'])
    start_dt = datetime.strptime(start_dt, '%d/%b')
    end_dt = datetime.strptime(end_dt, '%d/%b')

    hoje = '1900-' + str(datetime.today().strftime(
        '%m-%d'))  # Pega data Atual e coloca no tipo do dataframe (1900 ano que não será utilizado)
    # Gerar o Grafico
    fig = px.line(df_pivot, title='Sazonalidade Anual - ' + ticker, width=1500, height=600)
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
    fig.add_vrect(x0=start_dt, x1=end_dt, fillcolor="green", opacity=0.25, line_width=0)
    st.plotly_chart(fig)
    return start_dt, end_dt

@st.cache#(suppress_st_warning=True)
def backtest(start_dt, end_dt):
    data = ffn.get(ticker, start='2000-01-01', end='2020-12-31')
    data = data.fillna(method='bfill')
    perf = data.calc_stats()
    # mes_inicio = {'Jan': '-01-01','Fev':'-02-01','Mar':'-03-01','Abr':'-04-01','Mai':'-05-01','Jun':'-06-01','Jul':'-07-01', 'Ago': '-08-01','Set': '-09-01','Out':'-10-01','Nov':'-11-01','Dez':'-12-01'}
    # mes_fim = {'Jan': '-01-31','Fev':'-02-28','Mar':'-03-31','Abr':'-04-30','Mai':'-05-31','Jun':'-06-30','Jul':'-07-31', 'Ago': '-08-31','Set': '-09-30','Out':'-10-31','Nov':'-11-30','Dez':'-12-31'}

    # start_dt = '30/Aug'
    # end_dt = '31/Dec'
    # start_dt = datetime.strptime(start_dt, '%d/%b')
    # end_dt = datetime.strptime(end_dt, '%d/%b')
    # ano='2000'
    data_inicio = start_dt.strftime("-%m-%d")
    data_fim = end_dt.strftime("-%m-%d")

    ret = pd.DataFrame()

    for ano in range(data.index.year[0],2021,1):
        inicio = str(ano) + data_inicio
        fim = str(ano) + data_fim
        perf.set_date_range(start=inicio, end=fim)
        stat = perf.stats
        ret = ret.append({'Ano': ano, '%': stat.iloc[3].values, 'DrawDown':stat.iloc[5].values}, ignore_index=True)
    return ret, inicio, fim

# ticker = 'PETR4'

ticker=st.selectbox("Ticker",['VALE3.SA','PETR4.SA', 'DIS', 'ALV', 'EBAY', 'BTCUSD' ])

df_pivot, lista_dias = sazonalidade(ticker)

start_dt, end_dt = gerar_grafico()

ret, inicio, fim = backtest(start_dt, end_dt)

gain = (sum(ret['%'] > 0))
loss = (sum(ret['%'] < 0))
gain_pct = (sum(ret['%'] > 0)) / len(ret)
loss_pct = (sum(ret['%'] < 0)) / len(ret)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric('Inicio', inicio)
col2.metric('Fim', fim)
col3.metric('Qtde de Trades', len(ret))
col4.metric('Gain', value=gain)
col4.metric('Gain', value="{0:.0%}".format(gain_pct))
col5.metric('Loss', value=loss)
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





