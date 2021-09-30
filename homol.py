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

@st.cache
def puxar_tickers_grafbolsa():
    url = 'http://www.grafbolsa.com/index.html'
    tabela = pd.read_html(url)[1][3:]  # Pega a 2º tabela, da 3º linha para baixo
    tabela = tabela.sort_values(9)  # Classifica em ordem alfabetica pela coluna do código
    lista_tickers = tabela[9].to_list()  # Transforma a Serie em lista, para ser usada nos widgets
    return lista_tickers

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
def backtest_ifr(ticker, nivel_ifr, capital, data_inicio, data_fim):
    # Coleta dos dados
    df = yf.download(ticker + ".SA", start=data_inicio, end=data_fim).copy()[["Open", "High", "Close", "Adj Close"]]
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
    ongoing = False 

    for i in range(0,len(df)):
        if ongoing == True:

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
        else:
            if ~(np.isnan(df['Buy Price'][i])):
                entry = df['Buy Price'][i]
                shares = round_down(capital / entry)
                ongoing = True

    return capital, all_profits, saldos

# @st.cache
def strategy_test(capital, all_profits):
    num_operations = len(all_profits)
    gains = sum(x >= 0 for x in all_profits)
    pct_gains = 100 * (gains / num_operations)
    losses = num_operations - gains
    pct_losses = 100 - pct_gains
    st.markdown('***')
    st.write('Backtesting de 5 Anos')
    st.write("Numero de Operações =", num_operations)
    st.write("Taxa de acerto =", pct_gains.round(), "%")
    # st.write("Gains =", gains, "or", pct_gains.round(), "%")
    # st.write("Loss =", losses, "or", pct_losses.round(), "%")
    lucro_total = sum(all_profits)
    st.write("Lucro =", f'R$ {lucro_total:.2f}', ' - ', ((lucro_total/capital)*100).round(), "%") 
    st.write("Capital Final =", f'R$ {capital + lucro_total:.2f}') 

def capital_plot(saldos, lucros):
    lucros = [0] + lucros # make sure both lists are the same size
    cap_evolution = pd.DataFrame({'Capital': saldos, 'Profit': lucros})
    st.markdown('***')
    st.markdown('**Curva de Capital**')
    st.area_chart(cap_evolution['Capital'])
    st.markdown('**Lucros / Trade**')
    st.area_chart(cap_evolution['Profit'])

st.header('Backtesting IFR2')
lista_tickers = puxar_tickers_grafbolsa()
ticker = st.selectbox('Selecione o Papel', lista_tickers)
nivel_ifr = st.number_input('Nível de IFR para compra',min_value=5, max_value=50, value=25)
capital = st.number_input('Capital inicial',min_value=1000, value=10000)
data_inicio = "2015-01-01"
data_fim = "2020-12-30"

capital, lucros, saldos = backtest_ifr(ticker, nivel_ifr, capital, data_inicio, data_fim)
strategy_test(capital, lucros)
capital_plot(saldos, lucros)