from pandas.core.frame import DataFrame
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import math

st.set_page_config(  # Alternate names: setup_page, page, layout
    layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
    initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
    page_title=None,  # String or None. Strings get appended with "• Streamlit".
    page_icon=None,  # String, anything supported by st.image, or None.
)
############################
############################
# RETIRAR ESSE BLOCO QDO MIGRAR PARA A PAGINA
############################
############################

@st.cache
def puxar_tickers_grafbolsa():
    url = 'http://www.grafbolsa.com/index.html'
    tabela = pd.read_html(url)[1][3:]  # Pega a 2º tabela, da 3º linha para baixo
    tabela = tabela.sort_values(9)  # Classifica em ordem alfabetica pela coluna do código
    lista_tickers = tabela[9].to_list()  # Transforma a Serie em lista, para ser usada nos widgets
    return lista_tickers

############################
############################
# RETIRAR ESSE BLOCO QDO MIGRAR PARA A PAGINA
############################
############################

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

@st.cache
def backtest_ifr(ticker, nivel_ifr, capital, data_inicio, data_fim, stop_tempo, dias_stop):
    # Coleta dos dados
    df = yf.download(ticker + ".SA", start=data_inicio, end=data_fim, progress=False).copy()[["Open", "High", "Close", "Adj Close"]]
    # Montar o Dataframe com as informações, IFR, Target, BuyPrice e SellPrice
    # Criar a coluna com o IFR2
    df["IFR2"] = rsi(df, column="Adj Close")

    # Criar a coluna com as máximas dos dois ultimos dias
    df["Target1"] = df["High"].shift(1)
    df["Target2"] = df["High"].shift(2)
    df["Target"] = df[["Target1", "Target2"]].max(axis=1)

    # We don't need them anymore
    df.drop(columns=["Target1", "Target2"], inplace=True)

    # Define exact buy price
    df["Buy Price"] = np.where(df["IFR2"] <= nivel_ifr, df["Close"], np.nan)

    # Define exact sell price
    df["Sell Price"] = np.where(
        df["High"] > df['Target'], 
        np.where(df['Open'] > df['Target'], df['Open'], df['Target']),
        np.nan)

    # Create a function to round any number to the smalles multiple of 100
    def round_down(x):
        return int(math.floor(x / 100.0)) * 100

    saldos = [capital] # list with the total capital after every operation
    all_profits = [] # list with profits for every operation
    days_in_operation = 0
    gains_total_days = 0
    gains_total_operations = 0
    losses_total_days = 0
    losses_total_operations = 0
    max_days = dias_stop # Dias para Stop no tempo

    ongoing = False 

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

    # Calcular o Drawdown

    def get_drawdown(data, column):
        data["Max"] = data[column].cummax()
        data["Delta"] = data['Max'] - data[column]
        data["Drawdown"] = 100 * (data["Delta"] / data["Max"])
        max_drawdown = data["Drawdown"].max()
        return max_drawdown

    saldos_df = pd.DataFrame(data=saldos, columns=["Saldos"])
    drawdown = get_drawdown(data=saldos_df, column="Saldos")

    # Define total number of days and the total number of operations during the period
    total_days = gains_total_days + losses_total_days
    total_operations = gains_total_operations + losses_total_operations

    media_dias_total = total_days / total_operations
    media_dias_gain = gains_total_days / gains_total_operations
    media_dias_loss = losses_total_days / losses_total_operations

    return capital, all_profits, saldos, drawdown, media_dias_total, media_dias_gain, media_dias_loss

# @st.cache
def strategy_test(capital, all_profits, drawdown, media_dias_total, media_dias_gain, media_dias_loss):
    num_operations = len(all_profits)
    gains = sum(x >= 0 for x in all_profits)
    valor_gains = 0
    valor_loss = 0
    for x in all_profits:
        if x > 0:
            valor_gains = valor_gains + x 
        else:
            valor_loss = valor_loss + x
    pct_gains = 100 * (gains / num_operations)
    losses = num_operations - gains
    pct_losses = 100 - pct_gains

    # st.markdown('**Backtesting de 5 Anos**')
    # st.write("Numero de Operações =", num_operations)
    # st.write("Gains =", gains, "ou", pct_gains.round(), "%", ' -> ', f'Lucro Bruto R$ {valor_gains:.2f}')
    # st.write("Loss =", losses, "ou", pct_losses.round(), "%", ' -> ', f'Prejuízo Bruto R$ {valor_loss:.2f}')
    # lucro_total = sum(all_profits)
    # st.write("Lucro Líquido =", f'R$ {lucro_total:.2f}', ' / ', ((lucro_total/capital)*100).round(), "%") 
    # st.write("Capital Final =", f'R$ {capital + lucro_total:.2f}') 

    lucro_total = sum(all_profits)
    # col1, col2, col3, col4 = st.columns([0.4,0.7,0.7,0.7])
    # col1.metric('Operações', value=num_operations)
    # col2.metric('Capital Inicial', value = f'R$ {capital:.2f}')
    # col3.metric('Lucro Liquido', value=f'R$ {lucro_total:.2f}', delta=str(((lucro_total/capital)*100).round()) + '%')
    # col4.metric('Capital Final', value=f'R$ {capital + lucro_total:.2f}')

    # col1, col2, col3, col4 = st.columns([0.4,0.4,0.7,0.7])
    # col1.metric('Gains', value=int(gains), delta=str(pct_gains.round()) + '%')
    # col2.metric('Loss', value=int(losses), delta=str(-pct_losses.round()) + '%')
    # col3.metric('Lucro Bruto', value=f'R$ {valor_gains:.2f}')
    # col4.metric('Prejuízo Bruto', value=f'R$ {valor_loss:.2f}')

    num_operations = str(num_operations)
    lucro_total = str(f'R$ {lucro_total:.2f}') + ' (' + str(((lucro_total/capital)*100).round()) + '%' + ')'
    capital = f'R$ {capital:.2f}'
    gains = str(gains) + ' (' + str(pct_gains.round()) + '%' + ')'
    losses = str(losses) + ' (' + str(pct_losses.round()) + '%' + ')'
    valor_gains = f'R$ {valor_gains:.2f}'
    valor_loss = f'R$ {valor_loss:.2f}'
    drawdown = str(drawdown.round()) + '%'
    media_dias_total = f'{media_dias_total:.2f}'
    media_dias_gain = f'{media_dias_gain:.2f}'
    media_dias_loss = f'{media_dias_loss:.2f}'

    estatisticas = pd.DataFrame({'ITENS': ['Intervalo','Capital Inicial','Núm. de Operações', 'Gains', 'Loss', 'Lucro Bruto', 
                                            'Prejuízo Bruto', ' Drawdown','Dias em Operações', 'Dias Op. Vencedoras', 'Dias Op. Perdedoras', 'Lucro Líquido'],
                        'ESTATÍSTICAS': ['5 anos',capital, num_operations, gains, losses, valor_gains, valor_loss, drawdown, media_dias_total, media_dias_gain, media_dias_loss, lucro_total]})
    estatisticas.set_index('ITENS', drop=True, inplace=True)
                            
    col1, col2, col3  = st.columns([0.6, 0.03, 1])
    # st.dataframe(estatisticas)
    col1.table(estatisticas)
    with col3:
        capital_plot(saldos, lucros)

def capital_plot(saldos, lucros):
    lucros = [0] + lucros # make sure both lists are the same size
    cap_evolution = pd.DataFrame({'Capital': saldos, 'Profit': lucros})
    # st.markdown('**Curva de Capital**')
    # st.area_chart(cap_evolution['Capital'])
    # st.markdown('**Lucros / Trade**')
    # st.bar_chart(cap_evolution['Profit'])
    cap_evolution.reset_index(inplace=True)
    
    # import altair as alt
    # cap_evolution.reset_index(inplace=True)
    # base = alt.Chart(cap_evolution).encode(x='index')
    # bar = base.mark_bar().encode(y='Profit')
    # line =  base.mark_line(color='red').encode(y='Capital')
    # st.altair_chart(bar + line)

    # import altair as alt
     # graph = alt.Chart(cap_evolution). mark_line().encode(x='index', y='Capital')
    # st.altair_chart(graph)

    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces

    fig.add_trace(
        go.Scatter(x=cap_evolution['index'], y=cap_evolution['Capital'], name="Capital"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Bar(x=cap_evolution['index'], y=cap_evolution['Profit'], name="Lucros/Trade",visible='legendonly'),
        secondary_y=True,
    )
    fig.update_layout(showlegend=True, hovermode="x unified",
                    width=650,
                    height=550,
                    margin=dict(l=0, r=0, b=0, t=50, pad=4),
                    title_text='Curva Capital / Lucros por Trade',
                    legend=dict(yanchor="top",y=0.99, xanchor="left", x=0.01)
                    )
    # Add images
    fig.add_layout_image(
            dict(
                # source="https://images.plot.ly/language-icons/api-home/python-logo.png",
                source="https://analisequant-mh2ir.ondigitalocean.app/media/b25913f6835e74fc51249994ddecaf68599311449505c3a07b1c49c4.png",
                xref="x domain",
                yref="y domain",
                x=0.25,
                y=0.55,
                sizex=0.5,
                sizey=0.5,
                opacity=0.3,
                layer="below"
    )
    )
    fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
    fig.update_yaxes(showgrid=False)
    st.plotly_chart(fig)




st.header('Backtesting IFR2')

with st.expander('Detalhes do Setup IFR2'):
    st.write("""
         O Setup IFR2 utiliza o IFR de 2 períodos como sinal de entrada. Grafico diário, se o IFR de 2 períodos atingir um determindado valor
         (Originalmente 30 ou 25), é feita a compra no fechamento do dia. A saída é feita na máxima dos 2 últimos dias. O Stop é no tempo, 
         7 dias após a entrada, se o preço não atingir a máxima dos 2 ultimos dias como alvo.
    """)


lista_tickers = puxar_tickers_grafbolsa()
col1, col2, col3 = st.columns(3)
with col1:
    ticker = st.selectbox('Selecione o Papel', lista_tickers)
with col2: 
    nivel_ifr = st.number_input('Nível de IFR para compra',min_value=5, max_value=50, value=25)
with col3:
    capital = st.number_input('Capital inicial',min_value=1000, value=10000)
with col1:
    st.write('Definir "Stop no Tempo" ou "Sem Stop"')
    stop_tempo = st.checkbox('Stop do Tempo')
with col2:
    if stop_tempo:
        dias_stop = st.number_input('Dias para Stop no Tempo',min_value=1, max_value=25, value=7)
    else:
        dias_stop=None
data_inicio = "2015-01-01"
data_fim = "2020-12-30"


capital, lucros, saldos, drawdown, media_dias_total, media_dias_gain, media_dias_loss  = backtest_ifr(ticker, nivel_ifr, capital, data_inicio, data_fim, stop_tempo, dias_stop)
st.markdown('***')
strategy_test(capital, lucros, drawdown, media_dias_total, media_dias_gain, media_dias_loss)
st.markdown('***')
# capital_plot(saldos, lucros)