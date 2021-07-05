import streamlit as st
import quant_app_carteira
import quant_app_correlacao
# import quant_app_carteira2
# import quant_app_teste
import yfinance as yf
# mport investpy as inv
import pandas as pd
from datetime import datetime

st.set_option('deprecation.showPyplotGlobalUse', False)  # Desabilitar os Warnigs sobre o Pyplot
st.set_page_config(page_title='Análise Quant', layout='wide', initial_sidebar_state='auto')  # Configurar Pagina

def main():

    # Removing and add pages
    pages = {
        "Análise de Carteira": page_carteira,
        "Análise de Correlações": page_correlacao
    }

    st.sidebar.title(":chart: Análise Quant v.2")
    page = st.sidebar.radio("Selecione a opção", tuple(pages.keys()))
    st.sidebar.markdown("***")
    st.sidebar.markdown('''<small>Criado por Roberto Martins</small>''', unsafe_allow_html=True)
    st.sidebar.markdown('''<small>rraires.dev@gmail.com</small>''', unsafe_allow_html=True)
    # puxar_tickers_investing()
    puxar_tickers_grafbolsa()

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

def page_carteira():
    quant_app_carteira.carteira()

def page_correlacao():
    quant_app_correlacao.correlacao()

def page_teste():
    quant_app_teste.teste()

def puxar_tickers_investing():
    st.session_state.lista_tickers = inv.get_stocks_list(country='Brazil')  # Pegar a lista das Ações Brasileiras
    st.session_state.lista_tickers.remove('NATU3')
    st.session_state.lista_tickers.append('NTCO3')
    st.session_state.lista_tickers.append('BOVA11')

def puxar_tickers_grafbolsa():
    url = 'http://www.grafbolsa.com/index.html'
    tabela = pd.read_html(url)[1][3:]  # Pega a 2º tabela, da 3º linha para baixo
    tabela = tabela.sort_values(9)  # Classifica em ordem alfabetica pela coluna do código
    st.session_state.lista_tickers = tabela[9].to_list()  # Transforma a Serie em lista, para ser usada nos widgets

##############################################

if __name__ == "__main__":
    main()