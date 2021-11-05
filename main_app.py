import streamlit as st
import quant_app_home
import quant_app_carteira
import quant_app_correlacao
import quant_app_sazonalidade
import quant_app_altas_quedas
import quant_app_backtest_ifr
import quant_app_raiox
import quant_app_contato
# import quant_app_carteira2
# import quant_app_teste
import yfinance as yf
#import investpy as inv
import pandas as pd
from datetime import datetime
import os
import plotly
import fundamentus

st.set_option('deprecation.showPyplotGlobalUse', False)  # Desabilitar os Warnigs sobre o Pyplot
st.set_page_config(page_title='Análise Quant', layout='wide', initial_sidebar_state='auto')  # Configurar Pagina

def main():

    # Removing and add pages
    pages = {
        "Home": page_home,
        "Análise de Carteira": page_carteira,
        "Correlações": page_correlacao,
        "Sazonalidade do Mercado": page_sazonalidade,
        "Analise de Altas e Quedas": page_altas_quedas,
        # "Backtest IFR2": page_backtest_ifr,
        "Raio-X do Mercado": page_raiox,
        "Contato / Reporte de Erros": page_contato
    }

    st.sidebar.image('./imagens/analisequant_logo-removebg.png')
    #st.sidebar.title(":chart: Análise Quant")
    page = st.sidebar.radio("Selecione a opção", tuple(pages.keys()))
    st.sidebar.markdown("***")
    with st.sidebar.expander('Versões'):
        # Mostrar versões das bibliotecas
        st.write(os.popen(f'python --version').read())
        st.write('Streamlit:', st.__version__)
        st.write('Pandas:', pd.__version__)
        st.write('yfinance:', yf.__version__)
        st.write('plotly:', plotly.__version__)
        st.write('Fundamentus:', fundamentus.__version__)
    st.sidebar.markdown('''<small>Criado por Roberto Martins</small>''', unsafe_allow_html=True)
    st.sidebar.markdown('''<small>rraires.dev@gmail.com</small>''', unsafe_allow_html=True)
    # puxar_tickers_investing()
    # st.session_state.lista_tickers = puxar_tickers_grafbolsa()
    st.session_state.tabela_papeis = puxar_tabela_papeis()


    ###### Iniciar o DataFrame do Portifolio, somente no primeiro carregamento da Página

    if 'portifolio' not in st.session_state:
        st.session_state.portifolio = pd.DataFrame()
        st.session_state.portifolio['Ação'] = ''
        st.session_state.portifolio['Qtde'] = ''
        st.session_state.portifolio['Últ. Preço'] = ''
        st.session_state.portifolio['Valor na Carteira'] = ''
        # st.session_state.portifolio['%'] = ''
        st.session_state.portifolio['Setor'] = ''
        st.session_state.portifolio['SubSetor'] = ''
        st.session_state.portifolio['Beta do Ativo'] = ''
        # state.portifolio['Beta Ponderado'] = ''

    ##########################################

    # Display the selected page with the session state
    pages[page]()

def page_home():
    quant_app_home.home()

def page_carteira():
    quant_app_carteira.carteira()

def page_correlacao():
    quant_app_correlacao.correlacao()

def page_sazonalidade():
    quant_app_sazonalidade.sazonalidade()

def page_altas_quedas():
    quant_app_altas_quedas.altas_quedas()

def page_backtest_ifr():
    quant_app_backtest_ifr.backtest_ifr()

def page_raiox():
    quant_app_raiox.raiox()

def page_contato():
    quant_app_contato.contato()

def puxar_tickers_investing():
    st.session_state.lista_tickers = inv.get_stocks_list(country='Brazil')  # Pegar a lista das Ações Brasileiras
    st.session_state.lista_tickers.remove('NATU3')
    st.session_state.lista_tickers.append('NTCO3')
    st.session_state.lista_tickers.append('BOVA11')

@st.cache
def puxar_tickers_grafbolsa():
    url = 'http://www.grafbolsa.com/index.html'
    tabela = pd.read_html(url)[1][3:]  # Pega a 2º tabela, da 3º linha para baixo
    tabela = tabela.sort_values(9)  # Classifica em ordem alfabetica pela coluna do código
    #st.session_state.lista_tickers = tabela[9].to_list()  # Transforma a Serie em lista, para ser usada nos widgets
    lista_tickers = tabela[9].to_list()
    return lista_tickers

@st.cache
def puxar_tabela_papeis():
    return pd.read_csv('tabela_tickers.csv')
##############################################

if __name__ == "__main__":
    main()