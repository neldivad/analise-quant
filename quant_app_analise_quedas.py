import streamlit as st
import pandas as pd
import yfinance as yf

@st.cache
def puxar_tickers_grafbolsa():
    url = 'http://www.grafbolsa.com/index.html'
    tabela = pd.read_html(url)[1][3:]  # Pega a 2º tabela, da 3º linha para baixo
    tabela = tabela.sort_values(9)  # Classifica em ordem alfabetica pela coluna do código
    lista_tickers = tabela[9].to_list()  # Transforma a Serie em lista, para ser usada nos widgets
    return lista_tickers

def Quedas():
    st.title('Análise de quedas e comportamento no dia seguinte')
    lista_tickers = puxar_tickers_grafbolsa()
    col1, col2 = st.columns(2)
    with col1:
        ticker = st.selectbox('Escolha a Ação (Clique no campo e digite as iniciais do Ticker)', lista_tickers)
    with col2:
        perc_queda = st.number_input(
            'Entre com a % de queda (Ex.: 10 para listar os dias em que a Ação caiu mais do que 10%', min_value=2, value=10)
    pressed_calc = st.button('Listar')
    st.markdown('***')

    if pressed_calc:
        papel = yf.download(ticker + '.SA')  # Baixar dados históricos do ticker
        papel = papel.reset_index()  # Resetar o index, que antes estava como Date, e agora Index
        papel['Retorno'] = papel[
            'Adj Close'].pct_change()  # Calcular a variação % entre um dia e outro do fechamento e criar a coluna Retorno
        papel = papel[
                :-1]  # Retirar a ultima linha (dia atual) caso ele tenha queda maior que o escolhido, para nao dar erro no dia seguinte q não existe

        perc = -(perc_queda / 100)  # Dividir o valor de perc por 100 para a busca

        indice = papel[papel[
                           "Retorno"] < perc].index  # Procurar pelas linhas onde o Retorno for menor que perc, e gerar a lista com os indices

        dia_queda = papel.iloc[indice]  # Criar a tabela com os dias de queda escolhido
        dia_seguinte = papel.iloc[indice + 1]  # Criar a tabela com os dias seguintes

        dados_df = pd.DataFrame()  # Criar o dataframe dos dados a serem apresentados
        dados_df['Data Queda'] = dia_queda['Date'].values  # Coluna das Datas de Queda
        dados_df['Data Queda'] = dados_df['Data Queda'].dt.strftime(
            '%d-%m-%Y')  # Formatar as coluna de datas commo string. Para apresentar no Streamlit
        dados_df['% Queda'] = dia_queda['Retorno'].values.round(2)  # Coluna com a % de queda
        dados_df['Abert. Dia Seguinte'] = (
        ((dia_seguinte['Open'].values - dia_queda['Close'].values) / dia_queda['Close'].values)).round(
            2)  # Coluna com a % da Abertura do dia seguinte
        dados_df['Fech. Dia Seguinte'] = dia_seguinte['Retorno'].values.round(
            2)  # Coluna com a % do Fechamento do dia seguinte
        dados_df['Var. Dia Seguinte'] = (
        ((dia_seguinte['Close'] - dia_seguinte['Open']) / dia_seguinte['Open'])).values.round(
            2)  # Coluna com a % Variação do dia seguinte

        dados_df.set_index('Data Queda', inplace=True)

        qtde_total = len(dados_df)
        qtde_abert = (dados_df[dados_df['Abert. Dia Seguinte'] > 0].count()[0])/qtde_total
        qtde_fech = (dados_df[dados_df['Fech. Dia Seguinte'] > 0].count()[0])/qtde_total
        qtde_var = (dados_df[dados_df['Var. Dia Seguinte'] > 0].count()[0])/qtde_total


        def _color_red_or_green(val):  # Função para o mapa de cores da tabela
            color = 'red' if val < 0 else 'green'
            return 'color: %s' % color
            # return 'background-color: %s' % color
       
        dados_df = dados_df.style.applymap(_color_red_or_green,
                                           subset=['% Queda', 'Abert. Dia Seguinte', 'Fech. Dia Seguinte',
                                                   'Var. Dia Seguinte']).format(
            {"% Queda": "{:.2%}", "Abert. Dia Seguinte": "{:.2%}", "Fech. Dia Seguinte": "{:.2%}",
             "Var. Dia Seguinte": "{:.2%}"})  # Formatar o dataframe com as cores do mapa acima e com a formatação de %

        col1, col2, col3 = st.columns(3)
        col1.metric('Abert. no Dia Seguinte Potitivo', value = f'{qtde_abert:.0%}')
        col2.metric('Fecha. no Dia Seguinte Positivo', value = f'{qtde_fech:.0%}')
        col3.metric('Variação no Dia Seguinte Positiva', value = f'{qtde_var:.0%}')
        

        
        st.write('Dias onde', ticker, ' teve uma queda de mais de', -perc_queda, '%')
        st.table(dados_df)

Quedas()