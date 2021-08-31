import streamlit as st

def home():

    def v_spacer(height, sb=False) -> None:
        for _ in range(height):
            if sb:
                st.sidebar.write('\n')
            else:
                st.write('\n')

    v_spacer(height=3, sb=True)


    col1, col2, col3 = st.columns([0.1,2,0.1])
    with col2:
        v_spacer(height=15, sb=False)
    col2.image('./imagens/analisequant_logo-removebg.png')


    # col1, col2, col3 = st.columns([0.7,3,0.1])
    # col2.header('Bem Vindo ao Análise Quant')
    #
    # st.image('./imagens/video_correlaçao.gif')
