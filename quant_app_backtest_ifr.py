from pandas.core.frame import DataFrame
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import math
import plotly.graph_objects as go
from datetime import datetime, timedelta

def backtest_ifr():
    st.header('Backtest IFR2')

    with st.expander('Detalhes do Setup IFR2', expanded= True):
        st.write("""
            O Setup IFR2 utiliza o IFR de 2 períodos como sinal de entrada. Grafico diário, se o IFR de 2 períodos atingir um determindado valor
            (Originalmente 30 ou 25), é feita a compra no fechamento do dia. A saída é feita na máxima dos 2 últimos dias. O Stop é no tempo, 
            7 dias após a entrada, se o preço não atingir a máxima dos 2 ultimos dias como alvo.
        """)

    with st.form(key='Parametros_Backtest'):
        col1, col2, col3 = st.columns(3)
        with col1:
            ticker = st.selectbox('Selecione o Papel', st.session_state.tabela_papeis['Ticker'])
            # ticker = st.selectbox('Selecione o Papel', ['EQTL3', 'BBDC4', 'PSSA3'])
        with col2: 
            nivel_ifr = st.number_input('Nível de IFR para compra',min_value=5, max_value=50, value=25)
        with col3:
            capital = st.number_input('Capital inicial',min_value=1000, value=10000)
        with col1:
            data_inicio = st.date_input("Inicio do Teste", value=pd.to_datetime("2010-01-01", format="%Y-%m-%d"))
        with col2:
            data_fim = st.date_input("Fim do Teste", value=pd.to_datetime("today", format="%Y-%m-%d"))
        with col1:
            st.write('Definir "Stop no Tempo" ou "Sem Stop"')
            stop_tempo = st.checkbox('Stop do Tempo')
        with col2:
            if stop_tempo:
                dias_stop = st.number_input('Dias para Stop no Tempo',min_value=1, max_value=25, value=7)
            else:
                dias_stop=None
        st.form_submit_button('Backtest')

    executa_backtest(ticker, nivel_ifr, dias_stop, capital, data_inicio, data_fim, stop_tempo)

def executa_backtest(ticker, nivel_ifr, dias_stop, capital, data_inicio, data_fim,stop_tempo):
    # Coleta dos dados
    df = yf.download(ticker + ".SA", start = data_inicio, end =  data_fim, progress=False).copy()[["Open", "High", "Close", "Adj Close"]]

    # Montar o Dataframe com as informações, IFR, Target, BuyPrice e SellPrice
    # Criar a coluna com o IFR2
    df["IFR2"] = rsi(df, column="Adj Close")
    # Criar a coluna com as máximas dos dois ultimos dias
    df["Target1"] = df["High"].shift(1)
    df["Target2"] = df["High"].shift(2)
    df["Target"] = df[["Target1", "Target2"]].max(axis=1)
    # Apagar colunas de apoio
    df.drop(columns=["Target1", "Target2"], inplace=True)
    # Define o preco de compra
    df["Buy Price"] = np.where(df["IFR2"] <= nivel_ifr, df["Close"], np.nan)
    # Define o preço de venda
    df["Sell Price"] = np.where(df["High"] > df['Target'], np.where(df['Open'] > df['Target'], df['Open'], df['Target']), np.nan) 

    # Inicialização das variáveis
    saldos = [capital] # list with the total capital after every operation
    all_profits = [] # list with profits for every operation
    days_in_operation = 0
    gains_total_days = 0
    gains_total_operations = 0
    losses_total_days = 0
    losses_total_operations = 0
    max_days = dias_stop # Dias para Stop no tempo
    ongoing = False 
    datas_operacoes = []

    # Create a function to round any number to the smalles multiple of 100
    def round_down(x):
        return int(math.floor(x / 100.0)) * 100

    # Loop de execução do Backtest
    if stop_tempo:
        for i in range(0,len(df)):
            if ongoing == True:
                days_in_operation += 1
                # Condições de saída do trade, ou no tempo ou na max dos dois ultimos dias
                if days_in_operation == max_days or ~(np.isnan(df['Sell Price'][i])):
                    # Define exit point and total profit
                    exit = np.where(~(np.isnan(df['Sell Price'][i])), 
                                    df['Sell Price'][i], 
                                    df['Close'][i])
                    profit = shares * (exit - entry)
                    # Append profit to list and create a new entry with the capital
                    # after the operation is complete
                    all_profits += [profit]
                    current_capital = saldos[-1] # current capital is the last entry in the list
                    saldos += [current_capital + profit]
                    datas_operacoes += [df.index[i]]
                    # Calcular os dias  de operação

                    # If profit is positive we increment the gains' variables
                    # Else, we increment the losses' variables
                    if profit > 0: 
                        gains_total_days += days_in_operation
                        gains_total_operations += 1
                    else: 
                        losses_total_days += days_in_operation
                        losses_total_operations += 1
                    ongoing = False
            else:
                if ~(np.isnan(df['Buy Price'][i])):
                    entry = df['Buy Price'][i]
                    shares = round_down(capital / entry)
                    # Operation has started, initialize count of days until it ends
                    days_in_operation = 0
                    ongoing = True
    else:
        for i in range(0,len(df)):
            if ongoing == True:
                days_in_operation += 1
                if ~(np.isnan(df['Sell Price'][i])):
                    # Define exit point and total profit
                    exit = df['Sell Price'][i]
                    profit = shares * (exit - entry)
                    # Append profit to list and create a new entry with the capital
                    # after the operation is complete
                    all_profits += [profit]
                    current_capital = saldos[-1] # current capital is the last entry in the list
                    saldos += [current_capital + profit]
                    ongoing = False
                    datas_operacoes += [df.index[i]]
                    # Calcular os dias  de operação
                    is_positive = exit > entry
                    # If profit is positive we increment the gains' variables
                    # Else, we increment the losses' variables
                    if is_positive > 0: 
                        gains_total_days += days_in_operation
                        gains_total_operations += 1
                    else: 
                        losses_total_days += days_in_operation
                        losses_total_operations += 1
            else:
                if ~(np.isnan(df['Buy Price'][i])):
                    entry = df['Buy Price'][i]
                    shares = round_down(capital / entry)
                    ongoing = True
                    # Operation has started, initialize count of days until it ends
                    days_in_operation = 0

    saldos_df = pd.DataFrame(saldos, columns=["Saldos"]) # Analisar para unificar com o df operacoes

    lucros =  all_profits.copy()
    lucros.insert(0,0) # Adicionar o 0 no inicio da lista para equalizar o tamanho com saldos_df
    # datas_operacoes.insert(0, str((datas_operacoes[0].year)-0) + datas_operacoes[0].strftime("-%m-%d")) # Adicionar uma data inicial, com ano anterior ao primeiro ano de operação, para gerar as estatisticas depois. Data somente para apoio
    datas_operacoes.insert(0, datas_operacoes[0].strftime("%Y-") + str((datas_operacoes[0].month)-1) + datas_operacoes[0].strftime("-%d"))# Adicionar uma data inicial, com mes anterior à primeira operação, para gerar as estatisticas depois. Data somente para apoio
    operacoes = pd.DataFrame()
    operacoes['Data'] = datas_operacoes
    operacoes['Lucro'] = lucros
    operacoes['Lucro Acumulado'] = operacoes['Lucro'].cumsum()
    operacoes['Saldo'] = saldos
    operacoes.set_index('Data', inplace=True)

    # Definir estatisticas dos dias de operação
    total_days = gains_total_days + losses_total_days
    total_operations = gains_total_operations + losses_total_operations
    media_dias_total = total_days / total_operations
    media_dias_gain = gains_total_days / gains_total_operations
    media_dias_loss = losses_total_days / losses_total_operations

    # Função para o calculo do Drawdown
    def get_drawdown(data, column):
        data["Max"] = data[column].cummax()
        data["Delta"] = data['Max'] - data[column]
        data["Drawdown"] = (data["Delta"] / data["Max"])
        max_drawdown = data["Drawdown"].max()
        #st.write(data)
        return max_drawdown

    # Estatisticas
    drawdown = get_drawdown(data=saldos_df, column="Saldos")
    num_operations = len(all_profits)
    gains = sum(x >= 0 for x in all_profits)
    valor_gains = 0
    valor_loss = 0
    for x in all_profits:
        if x > 0:
            valor_gains = valor_gains + x 
        else:
            valor_loss = valor_loss + x
    pct_gains = gains / num_operations
    losses = num_operations - gains
    pct_losses = 100 - pct_gains
    lucro_total = sum(all_profits)
    num_operations = str(num_operations)

    lucro_total_mostrar = str(f'R$ {lucro_total:.2f}') + ' (' + str(((lucro_total/capital)*100).round()) + '%' + ')'
    capital_inicial = f'R$ {capital:.2f}'
    gains = str(gains) + ' (' + str(pct_gains.round()) + '%' + ')'
    losses = str(losses) + ' (' + str(pct_losses.round()) + '%' + ')'
    valor_gains = f'R$ {valor_gains:.2f}'
    valor_loss = f'R$ {valor_loss:.2f}'
    # drawdown = str(drawdown.round(0)) + '%'
    drawdown = f'{drawdown:.0%}'
    media_dias_total = f'{media_dias_total:.2f}'
    media_dias_gain = f'{media_dias_gain:.2f}'
    media_dias_loss = f'{media_dias_loss:.2f}'

    #Calculo Payoff e Exp Matematica
    media_gains = operacoes[operacoes['Lucro']>0]['Lucro'].mean()
    media_loss = abs(operacoes[operacoes['Lucro']<0]['Lucro'].mean())
    payoff = media_gains/media_loss
    exp_mat = ((1+(media_gains/media_loss))*pct_gains)-1

    # Calculo Retornos por ano
    # lista_anos = list(dict.fromkeys(operacoes.index.year[1:])) # Obter os valores unicos dos anos do dataframe
    # df_stat_anos = pd.DataFrame(columns=['Ano', 'Num_Oper', 'Lucro_Ano','Retorno', 'Pct_Gain', 'Payoff', 'Exp_Mat', 'Drawdown'])
    # count = 0
    # for ano in lista_anos: 
    #     num_oper_ano = len(operacoes[operacoes.index.year == ano])
    #     # lucro_ano = sum(operacoes[operacoes.index.year == ano]['Lucro'])
    #     lucro_ano = (operacoes[operacoes.index.year == ano].iloc[-1][2]) - (operacoes[operacoes.index.year == ano-1].iloc[-1][2])
    #     ret_ano = (operacoes[operacoes.index.year == ano].iloc[-1][2]/operacoes[operacoes.index.year == ano-1].iloc[-1][2])-1
    #     pct_gain_ano = len(operacoes[(operacoes.index.year == ano) & (operacoes['Lucro']>0)]) / len(operacoes[operacoes.index.year == ano])
    #     media_gains_ano = operacoes[(operacoes.index.year == ano) & (operacoes['Lucro']>0)]['Lucro'].mean()
    #     media_loss_ano = abs(operacoes[(operacoes.index.year == ano) & (operacoes['Lucro']<0)]['Lucro'].mean())
    #     payoff_ano = media_gains_ano/media_loss_ano
    #     exp_mat_ano = ((1+(media_gains_ano/media_loss_ano))*pct_gain_ano)-1
    #     drawdown_ano = get_drawdown(data=operacoes[(operacoes.index.year == ano)] , column="Saldo")
    #     df_stat_anos.loc[count] = [ano, num_oper_ano, lucro_ano, ret_ano, pct_gain_ano, payoff_ano, exp_mat_ano, drawdown_ano]
    #     count += 1

    # df_stat_anos = df_stat_anos.astype({"Ano": int, "Num_Oper":int})
    # df_stat_anos.set_index('Ano', inplace=True)
    # df_stat_anos = df_stat_anos.transpose()
    # st.write(df_stat_anos)
    
    estatisticas = pd.DataFrame({'ITENS': ['Intervalo','Capital Inicial','Núm. de Operações', 'Gains', 'Loss', 'Lucro Bruto', 
                                            'Prejuízo Bruto', ' Drawdown','Dias em Operações', 'Dias Op. Vencedoras', 'Dias Op. Perdedoras', 'Lucro Líquido'],
                        'ESTATÍSTICAS': ['5 anos',capital_inicial, num_operations, gains, losses, valor_gains, valor_loss, drawdown, media_dias_total, media_dias_gain, media_dias_loss, lucro_total_mostrar]})
    estatisticas.set_index('ITENS', drop=True, inplace=True)

    # with st.expander('ESTATÍSTICAS', expanded=True):
    #     col1, col2, col3, col4,col5 = st.columns([0.5,2,2,1,0.5])
    #     col2.metric('Operações', value=num_operations)
    #     col3.metric('Taxa Acerto', value=f'{pct_gains:.0%}')
    #     col4.metric('Lucro',value=f'{lucro_total/capital:.0%}',)

    #     col1, col2, col3, col4,col5 = st.columns([0.5,2,2,1,0.5])
    #     col2.metric('PayOff', value=f'{payoff:.2f}')
    #     col3.metric('Exp. Matemática', value=f'{exp_mat:.2f}')
    #     col4.metric('DrawDown',value=drawdown)

    #     col1, col2, col3, col4,col5 = st.columns([0.7,2,1,2,0.7])
    #     capital_final = f'R$ {capital+lucro_total:_.2f}'
    #     capital = f'R$ {capital:_.2f}'
    #     capital = capital.replace('.', ',').replace('_','.')
    #     col2.metric('Capital Inicial', value=capital)
    #     capital_final = capital_final.replace('.', ',').replace('_','.')
    #     col4.metric('Capital Final', value=capital_final)
    #     st.markdown('***')
    #     st.line_chart(operacoes['Lucro Acumulado'], width=500, height=500)

    with st.expander('ESTATÍSTICAS', expanded=True):

        col1, col2, col3, col4,col5, col6 = st.columns(6)
        col1.metric('Operações', value=num_operations)
        col2.metric('Lucro',value=f'{lucro_total/capital:.0%}',)
        col3.metric('Taxa Acerto', value=f'{pct_gains:.0%}')
        col4.metric('PayOff', value=f'{payoff:.2f}')
        col5.metric('Exp. Matemática', value=f'{exp_mat:.2f}')
        col6.metric('DrawDown',value=drawdown)

        col1, col2, col3 = st.columns([0.4, 1, 1])
        capital_mostrar = f'R$ {capital:_.2f}'
        capital_mostrar = capital_mostrar.replace('.', ',').replace('_','.')
        capital_final_mostrar = f'R$ {capital + lucro_total:_.2f}'
        capital_final_mostrar = capital_final_mostrar.replace('.', ',').replace('_','.')
        col2.metric('Capital Inicial', value=capital_mostrar)
        col3.metric('Capital Final', value=capital_final_mostrar, delta=f'{lucro_total/capital:.0%}')
        st.markdown('***')

        #Gráficos
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=operacoes.index, y=operacoes['Saldo']))
        fig.update_layout(title_text = 'Evolução do Capital', yaxis_tickformat = '$', width=1000, height=500)
        fig.update_xaxes(showline=False, showgrid=False)
        fig.update_yaxes(showline=False, showgrid=False)
        fig.add_layout_image(
                # dict(
                #     source='https://analise-quant.herokuapp.com/media/b25913f6835e74fc51249994ddecaf68599311449505c3a07b1c49c4.png',
                #             xref="paper", yref="paper",
                #             x=1.10, y=1.12,
                #             sizex=0.2, sizey=0.2,
                #             xanchor="right", yanchor="bottom"
                #         )
                dict(source="https://analise-quant.herokuapp.com/media/b25913f6835e74fc51249994ddecaf68599311449505c3a07b1c49c4.png",
                    xref="x domain", yref="y domain",
                    x=0.25, y=0.6,
                    sizex=0.5, sizey=0.5,
                    opacity=0.3, layer="below")
        )
        st.plotly_chart(fig)

        # ret_anos["Color"] = np.where(ret_anos['Retorno'] < 0, 'red', 'green')
        # fig = go.Figure()
        # fig.add_trace(go.Bar(name='Net', x=ret_anos.index, y=ret_anos['Retorno'], marker_color=ret_anos['Color']))
        # fig.update_layout(title = 'Retorno por Ano' , barmode='stack', yaxis_tickformat = ',.0%', width=900, height=400, xaxis=dict(tickmode='linear'))
        # st.plotly_chart(fig)

    # st.dataframe(operacoes)
    # st.dataframe(estatisticas)


#Função para calculo do IFR2
def rsi(data, column, window=2):   
    
    data = data.copy()
    
    # Establish gains and losses for each day
    data["Variation"] = data[column].diff()
    data = data[1:]
    data["Gain"] = np.where(data["Variation"] > 0, data["Variation"], 0)
    data["Loss"] = np.where(data["Variation"] < 0, data["Variation"], 0)

    # Calculate simple averages so we can initialize the classic averages
    simple_avg_gain = data["Gain"].rolling(window).mean()
    simple_avg_loss = data["Loss"].abs().rolling(window).mean()
    classic_avg_gain = simple_avg_gain.copy()
    classic_avg_loss = simple_avg_loss.copy()

    for i in range(window, len(classic_avg_gain)):
        classic_avg_gain[i] = (classic_avg_gain[i - 1] * (window - 1) + data["Gain"].iloc[i]) / window
        classic_avg_loss[i] = (classic_avg_loss[i - 1] * (window - 1) + data["Loss"].abs().iloc[i]) / window
    
    # Calculate the RSI
    RS = classic_avg_gain / classic_avg_loss
    RSI = 100 - (100 / (1 + RS))
    return RSI

# backtest_ifr()