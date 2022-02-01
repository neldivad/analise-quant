import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go

st.set_page_config(layout='wide')
key = {'x-api-key': 'vDQAZKPcub6iasVMb4l4Y4pv4xaP1uzo7ENFD6q8'}

@st.cache
def puxar_lista_fundos():
    url = 'https://api.carteiraglobal.com/funds/'
    res = requests.get(url, headers=key)
    lista_fundos = res.json()
    pages = lista_fundos['pages']
    df_lista_fundos_completa = pd.DataFrame(columns=['id', 'name', 'cnpj'])
    for page in list(range(1,pages+1)):
        url = 'https://api.carteiraglobal.com/funds?page='+str(page)+'&limit=5000'
        res = requests.get(url, headers=key)
        lista_fundos = res.json()
        df_lista_fundos = pd.DataFrame(lista_fundos['rows'])
        df_lista_fundos_completa = df_lista_fundos_completa.append(df_lista_fundos)
    df_lista_fundos_completa.reset_index(inplace=True, drop=True)

    return df_lista_fundos_completa

st.subheader('Informações de Fundos de Investimentos')
# Escolher fundo
df_lista_fundos_completa = puxar_lista_fundos()
with st.form(key='Seleção Fundo'):
    selecao = st.selectbox('Selecione o Fundo', df_lista_fundos_completa['name'])
    busca = st.form_submit_button('Buscar Informações')

if busca:
    id = df_lista_fundos_completa[df_lista_fundos_completa['name'] == selecao].iloc[0][0]
    cnpj = df_lista_fundos_completa[df_lista_fundos_completa['name'] == selecao].iloc[0][2]

    # Puxar report (cotas) do fundo escolhido
    url = 'https://api.carteiraglobal.com/funds/'+str(id)+'/reports' 
    res_report = requests.get(url, headers=key)
    if len(res_report.json()) != 1: # Verificar se há dados de cotas
        df_cota_fundo = pd.DataFrame(res_report.json())
        df_cota_fundo['rent_norm'] = (df_cota_fundo['quote_value']/df_cota_fundo['quote_value'][0])-1
        df_cota_fundo['date_report'] = pd.to_datetime(df_cota_fundo['date_report'])
        df_cota_fundo.set_index('date_report', drop=True, inplace=True)
        ult_rent= df_cota_fundo['rent_norm'][-1]

        # Puxar profile do fundo
        url = 'https://api.carteiraglobal.com/funds/'+cnpj
        res_profile = requests.get(url, headers=key)
        profile = res_profile.json()


        with st.expander('Informações', expanded=True):
            col1, col2 = st.columns([0.4,1])

            with col1:
                st.write(' ')
                st.markdown('**Fundo:** ' + selecao)
                cnpj_fundo = cnpj[0:2] + '.' + cnpj[2:5] + '.' + cnpj[5:8] + '/' + cnpj[8:12] + '-' + cnpj[12:14]
                st.markdown('**CNPJ:** ' + cnpj_fundo)
                st.markdown('**Tipo Anbima:** ' +  profile['anbima_type'] )
                st.markdown('**Benchmark:** ' +  profile['benchmark'] )
                data_inicio_fundo = profile['activity_initial_date']
                data_inicio_fundo = data_inicio_fundo[8:10] + '/' + data_inicio_fundo[5:7] + '/' + data_inicio_fundo[0:4]
                st.markdown('**Data de Início:** ' +  data_inicio_fundo )
                tx_adm = float(profile['adm_fee'])
                tx_adm = f'{tx_adm:.2%}'
                st.markdown('**Tx. Adm.:** ' + tx_adm)
                st.write(' ')
                rent_12m = (df_cota_fundo.tail(252).iloc[-1][0]/df_cota_fundo.tail(252).iloc[0][0])-1
                st.metric('Rentabilidade - Ult. 12 meses e desde início', value = f'{rent_12m:.0%}', delta = f'{ult_rent:.0%}')
            with col2:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df_cota_fundo.index, y=df_cota_fundo['rent_norm']))
                fig.update_layout(title_text = '<b>Histórico Rentabilidade</b>', yaxis_tickformat = '%', width=750, height=400,
                                    margin=dict(l=20, r=20, t=60, b=20))
                fig.update_xaxes(showline=False, showgrid=False)
                fig.update_yaxes(showline=False, showgrid=False, zeroline = False)
                fig.add_layout_image(
                dict(source='https://analise-quant.herokuapp.com/media/b25913f6835e74fc51249994ddecaf68599311449505c3a07b1c49c4.png',
                    xref="x domain", yref="y domain", 
                    x=0.25, y=0.6,
                    sizex=0.5, sizey=0.5,
                    opacity=0.3, layer="below"))
                st.plotly_chart(fig)
    else:
        st.error('Este fundo não possui dados nesta base')