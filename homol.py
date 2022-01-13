import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go

st.set_page_config(layout='wide')
st.header('API Carteira Global')
st.markdown('***')
key = {'x-api-key': 'vDQAZKPcub6iasVMb4l4Y4pv4xaP1uzo7ENFD6q8'}

# Puxar lista dos fundos
url = 'https://api.carteiraglobal.com/funds/'
res = requests.get(url, headers=key)
lista_fundos = res.json()
df_lista_fundos = pd.DataFrame(lista_fundos['rows'])
df_lista_fundos.set_index('id', drop=True)

st.subheader('Fundos')
# Escolher fundo
selecao = st.selectbox('Selecione o Fundo', df_lista_fundos['name'])
id = df_lista_fundos[df_lista_fundos['name'] == selecao].iloc[0][0]
cnpj = df_lista_fundos[df_lista_fundos['name'] == selecao].iloc[0][2]

# Puxar report (cotas) do fundo escolhido
url = 'https://api.carteiraglobal.com/funds/'+str(id)+'/reports' 
res = requests.get(url, headers=key)
res.json()
if len(res.json()) != 1: # Verificar se há dados de cotas
    df_cota_fundo = pd.DataFrame(res.json())
    df_cota_fundo['quote_norm'] = (df_cota_fundo['quote_value']/df_cota_fundo['quote_value'][0])-1
    df_cota_fundo['date_report'] = pd.to_datetime(df_cota_fundo['date_report'])
    df_cota_fundo.set_index('date_report', drop=True, inplace=True)
    ult_cota = df_cota_fundo['quote_norm'][-1]

    col1, col2 = st.columns([0.4,1])

    with col1:
        st.write(' ')
        st.subheader('Fundo: ' + selecao)
        st.subheader('CNPJ: ' + cnpj)
        st.write(' ')
        st.metric('Rentabilidade desde Início', value = f'{ult_cota:.0%}')
    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_cota_fundo.index, y=df_cota_fundo['quote_norm']))
        fig.update_layout(title_text = 'Histórico Rentabilidade', yaxis_tickformat = '%', width=1000, height=500)
        st.plotly_chart(fig)
else:
    st.error('Este fundo não possui dados na nossa base')