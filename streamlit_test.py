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
#
# # locale.setlocale(locale.LC_TIME, 'pt_BR.utf-8')
# #locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
#
# ticker = 'VALE3.sa'
# preco = yf.download(ticker, start='2000-01-01', end='2020-12-31', progress = False)['Adj Close']
# preco = preco.fillna(method='bfill')
#
# decomposicao = sm.tsa.seasonal.seasonal_decompose(preco, model='additive', period=252)
#
# sazonalidade = pd.DataFrame(decomposicao.seasonal)
#
# df_pivot= pd.pivot_table(sazonalidade, values='seasonal', index=[sazonalidade.index.month.rename('Mês'), sazonalidade.index.day.rename('Dia')], columns=sazonalidade.index.year)
# df_pivot = df_pivot.fillna(method='bfill')
# df_pivot['Media'] = df_pivot.mean(axis=1)
#
# df_teste = df_pivot['Media']
# df_teste = df_teste.reset_index(level=[0,1])
#
# #meses=['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
# meses=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# count =1
# for mes in meses:
#     df_teste['Mês'].replace(count,mes, inplace=True)
#     count += 1
# df_teste['Dia'] = df_teste['Dia'].astype(str)
# df_teste['Data'] = df_teste['Dia'] + '/' + df_teste['Mês']
#
# df = pd.DataFrame(columns=['Data','Sazonalidade'])
# df['Data'] = df_teste['Data']
# df['Sazonalidade'] = df_teste['Media']
# df.set_index('Data', inplace=True)
#
# df.drop('29/Feb', inplace=True)
#
#
# count =0
# df['DT_Object'] = ''
# for i in range(len(df)):
#     df['DT_Object'][count] = datetime.strptime(df.index[count], '%d/%b')
#     count +=1
#
# df_novo = pd.DataFrame(columns=['Data','Sazonalidade'])
# df_novo['Data']=df['DT_Object']
# df_novo['Sazonalidade']=df['Sazonalidade']
# df_novo.set_index('Data', inplace=True)
#
#
#
# # fig = pivot.iplot(asFigure=True, xTitle='Meses', yTitle='Sazonalidade', title='Sazonalidade Anual - ' + ticker, dimensions=[1000, 500])
# # fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", legend_bgcolor="white")
# # #fig.add_vrect(x0=start_dt, x1=end_dt, fillcolor="green", opacity=0.25, line_width=0)
# # st.plotly_chart(fig)
#
# hoje = '1900-' + str(datetime.today().strftime('%m-%d'))
#
# fig = px.line(df_novo, title='Sazonalidade Anual - ' + ticker, width=1700, height = 800)
# config = {'staticPlot': True}
# if st.checkbox('Mostrar Data Atual'):
#     fig.add_vline(hoje)
# fig.update_layout(xaxis_tickformatstops = [dict(dtickrange=[None, 'M1'], value='%b'),
#                                            dict(dtickrange=['M1', None], value="%d")],
#                   xaxis = dict(tickvals = ['1900-01-02','1900-02-01','1900-03-01','1900-04-02','1900-05-01',
#                                            '1900-06-01','1900-07-02','1900-08-01','1900-09-01','1900-10-02',
#                                            '1900-11-01','1900-12-01']),
#                   showlegend=False, hovermode="x unified"
#     )
# fig.update_traces(hovertemplate="<b>%{x|%d/%b}</b>")
# # fig.update_traces(hovertemplate="Data:<b>%{x|%d/%b}</b><br>Sazonalidade: %{y}")
#
# st.plotly_chart(fig)

#fig.data[0].x



#
# fig = px.line(df_novo, title='Sazonalidade Anual - ' + ticker, width=1700, height = 800)
# config = {'staticPlot': True}
# fig.update_layout(xaxis_tickformat = '%d/%b')
# if st.checkbox('Mostrar Hoje'):
#     fig.add_vline(hoje)
# fig.update_layout(
#     xaxis_tickformatstops = [
#         dict(dtickrange=[None, 'M1'], value='%d/%b'),
#         dict(dtickrange=['M1', None], value="%b")
#     #     dict(dtickrange=[None, 1000], value='%d/%b'),
#     #     dict(dtickrange=[1000, 60000], value="%H:%M:%S s"),
#     #     dict(dtickrange=[60000, 3600000], value="%H:%M m"),
#     #     dict(dtickrange=[3600000, 86400000], value="%H:%M h"),
#     #     dict(dtickrange=[86400000, 604800000], value="%e. %b d"),
#     #     dict(dtickrange=[604800000, "M1"], value="%e. %b w"),
#     #     dict(dtickrange=["M1", "M12"], value='%b'),
#     #     dict(dtickrange=["M12", None], value="%Y Y")
#     ]
# )
# # fig.update_layout(
# #     xaxis = dict(
# #         #tickmode = 'linear',
# #         tick0 = '1900-01-02'
# #         #dtick = 21*24*60*60*1000 # 7 days
# #     ),
# #     xaxis_tickformatstops = [
# #         dict(dtickrange=[None, 'M1'], value='%b'),
# #         dict(dtickrange=['M1', None], value='%b')]
# # )
#
#
# fig.update_layout(
#     xaxis = dict(tickvals = ['1900-01-02','1900-02-01','1900-03-01','1900-04-02','1900-05-01','1900-06-01','1900-07-02',
#                              '1900-08-01','1900-09-01','1900-10-02','1900-11-01','1900-12-01']),
#     xaxis_tickformatstops = [dict(dtickrange=[None, 'M1'], value='%b'),dict(dtickrange=['M1', None], value='%b')],
#     showlegend=False, hovermode="x unified")
# st.plotly_chart(fig)


# st.line_chart(decomposicao.observed)
# st.line_chart(decomposicao.trend)
# st.line_chart(decomposicao.seasonal)
# st.line_chart(decomposicao.resid)






# @st.cache(suppress_st_warning=True)
# def sazonalidade():
#     ticker = 'VALE3.SA'
#     preco = yf.download(ticker,start='2000-01-01', end='2020-12-31')['Adj Close']
#     preco = preco.fillna(method='bfill')
#
#     decomposicao = sm.tsa.seasonal.seasonal_decompose(preco, model='additive', period=251)
#
#     st.line_chart(decomposicao.observed)
#
#     Monthly_seasonal = pd.DataFrame(decomposicao.seasonal.groupby([decomposicao.seasonal.index.year.rename('year'),
#                                                                    decomposicao.seasonal.index.month.rename(
#                                                                        'month')]).mean())
#     Monthly_seasonal = pd.pivot_table(Monthly_seasonal, values='seasonal', index='year', columns='month')
#     Monthly_seasonal.columns = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
#     Monthly_seasonal = Monthly_seasonal.transpose()
#     Monthly_seasonal['Media'] = Monthly_seasonal.mean(axis=1)
#
#
#     return Monthly_seasonal, ticker
#
#
# Monthly_seasonal, ticker = sazonalidade()
#
# st.subheader('Sazonalidade Anual')
#
# start_dt, end_dt = st.select_slider("Selecione o Período", options=Monthly_seasonal.index, value=['Jan' , 'Dez'])
#
# fig = Monthly_seasonal['Media'].iplot(asFigure=True, xTitle='Meses', yTitle='Sazonalidade',
#                                       title='Sazonalidade Anual - ', dimensions=[725, 500])
# fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", legend_bgcolor="white")
# fig.add_vrect(x0=start_dt, x1=end_dt, fillcolor="green", opacity=0.25, line_width=0)
# st.plotly_chart(fig)
#
#
#
# ############BackTest##############
# data = ffn.get(ticker, start='2000-01-01', end='2020-12-31')
# data = data.fillna(method='bfill')
# perf = data.calc_stats()
# mes_inicio = {'Jan': '-01-01','Fev':'-02-01','Mar':'-03-01','Abr':'-04-01','Mai':'-05-01','Jun':'-06-01','Jul':'-07-01', 'Ago': '-08-01','Set': '-09-01','Out':'-10-01','Nov':'-11-01','Dez':'-12-01'}
# mes_fim = {'Jan': '-01-31','Fev':'-02-28','Mar':'-03-31','Abr':'-04-30','Mai':'-05-31','Jun':'-06-30','Jul':'-07-31', 'Ago': '-08-31','Set': '-09-30','Out':'-10-31','Nov':'-11-30','Dez':'-12-31'}
#
# ret = pd.DataFrame()
#
# for ano in range(data.index.year[0],2021,1):
#     inicio = str(ano) + str(mes_inicio[start_dt])
#     fim = str(ano) + str(mes_fim[end_dt])
#     perf.set_date_range(start=inicio, end=fim)
#     stat = perf.stats
#     ret = ret.append({'%': stat.iloc[3].values, 'Ano': ano}, ignore_index=True)
#
# gain = (sum(ret['%'] > 0))
# loss = (sum(ret['%'] < 0))
#
# col1, col2, col3, col4, col5 = st.columns(5)
# col1.metric('Inicio', start_dt)
# col2.metric('Fim', end_dt)
# col3.metric('Qtde de Trades',len(ret))
# col4.metric('Gain', gain)
# col5.metric('Loss', loss)

















