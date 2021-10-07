import streamlit as st
import pandas as pd
import yfinance as yf

def altas_quedas():
    st.header('Altas e Quedas e comportamento no dia seguinte')
    st.write('')
    col1, col2 = st.columns(2)
    with col1:
        ticker = st.selectbox('Escolha a Ação (Clique no campo e digite as iniciais do Ticker)', st.session_state.lista_tickers)
    with col2:
        perc_escolha = st.number_input(
            'Entre com a %  (Ex.: 10 para listar os dias em que a Ação caiu ou subiu mais do que 10%', min_value=2, value=10)
    opcao = st.radio('Escolha entre dias de Alta ou dias de Queda', ['Alta', 'Queda'])
    pressed_calc = st.button('Listar')
    st.markdown('***')

    if pressed_calc:
        papel = yf.download(ticker + '.SA')  # Baixar dados históricos do ticker
        papel = papel.reset_index()  # Resetar o index, que antes estava como Date, e agora Index
        papel['Retorno'] = papel['Adj Close'].pct_change()  # Calcular a variação % entre um dia e outro do fechamento e criar a coluna Retorno
      
        if opcao == 'Alta':
            perc = (perc_escolha / 100)  # Dividir o valor de perc por 100 para a busca
            indice = papel[papel["Retorno"] > perc].index  # Procurar pelas linhas onde o Retorno for menor que perc, e gerar a lista com os indices
        else:
            perc = -(perc_escolha / 100)  # Dividir o valor de perc por 100 para a busca
            indice = papel[papel["Retorno"] < perc].index  # Procurar pelas linhas onde o Retorno for menor que perc, e gerar a lista com os indices

        if len(indice) == 0:
            st.warning('Não há dias com a variação de queda ou alta escolhida!')
            st.stop()

        # Bloco para verificar se o dia atual é um dos dias de queda escolhido. Se sim, apaga ele.
        if indice[-1] == (len(papel)-1):
            papel = papel[:-1] # Tirar o ultimo dia
            indice = papel[papel["Retorno"] < perc].index
            dia_queda = papel.iloc[indice]
            dia_seguinte = papel.iloc[indice+1]
        else:
            dia_queda = papel.iloc[indice]
            dia_seguinte = papel.iloc[indice+1]

        dados_df = pd.DataFrame()  # Criar o dataframe dos dados a serem apresentados
        dados_df['Data Queda'] = dia_queda['Date'].values  # Coluna das Datas de Queda
        dados_df['Data Queda'] = dados_df['Data Queda'].dt.strftime(
            '%d-%m-%Y')  # Formatar as coluna de datas commo string. Para apresentar no Streamlit
        dados_df['%'] = dia_queda['Retorno'].values.round(2)  # Coluna com a % de queda
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
        qtde_abert_positivos = (dados_df[dados_df['Abert. Dia Seguinte'] > 0].count()[0])/qtde_total
        qtde_fech_positivos = (dados_df[dados_df['Fech. Dia Seguinte'] > 0].count()[0])/qtde_total
        qtde_fech_positivos = (dados_df[dados_df['Var. Dia Seguinte'] > 0].count()[0])/qtde_total

        qtde_abert_negativos= (dados_df[dados_df['Abert. Dia Seguinte'] < 0].count()[0])/qtde_total
        qtde_fech_negativos = (dados_df[dados_df['Fech. Dia Seguinte'] < 0].count()[0])/qtde_total
        qtde_fech_negativos = (dados_df[dados_df['Var. Dia Seguinte'] < 0].count()[0])/qtde_total


        def _color_red_or_green(val):  # Função para o mapa de cores da tabela
            color = 'red' if val < 0 else 'green'
            return 'color: %s' % color
            # return 'background-color: %s' % color
       
        dados_df = dados_df.style.applymap(_color_red_or_green,
                                           subset=['%', 'Abert. Dia Seguinte', 'Fech. Dia Seguinte',
                                                   'Var. Dia Seguinte']).format(
            {"%": "{:.2%}", "Abert. Dia Seguinte": "{:.2%}", "Fech. Dia Seguinte": "{:.2%}",
             "Var. Dia Seguinte": "{:.2%}"})  # Formatar o dataframe com as cores do mapa acima e com a formatação de %

        if opcao == 'Alta':
            st.subheader('Dia seguinte à ALTAS maiores que ' + str(perc_escolha) + '%')
        else:
            st.subheader('Dia seguinte à QUEDAS maiores que ' + str(perc_escolha) + '%')

        st.write('')
        col1, col2, col3= st.columns(3)
        col1.metric('Abert. no Dia Seguinte Positivo', value = f'{qtde_abert_positivos:.0%}')
        col2.metric('Fech. no Dia Seguinte Positivo', value = f'{qtde_fech_positivos:.0%}')
        col3.metric('Variação no Dia Seguinte Positiva', value = f'{qtde_fech_positivos:.0%}')

        col1, col2, col3= st.columns(3)
        col1.metric('Abert. no Dia Seguinte Negativa', value = f'{qtde_abert_negativos:.0%}')
        col2.metric('Fech. no Dia Seguinte Negativo', value = f'{qtde_fech_negativos:.0%}')
        col3.metric('Variação no Dia Seguinte Negativa', value = f'{qtde_fech_negativos:.0%}')

        if opcao == 'Alta':
            st.write('Dias onde', ticker, ' teve uma ALTA de mais de', perc_escolha, '%')
        else:
            st.write('Dias onde', ticker, ' teve uma QUEDA de mais de', perc_escolha, '%')
        st.table(dados_df)