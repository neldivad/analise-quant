import streamlit as st
# import bokeh
# import bokeh.layouts
# import bokeh.models
# import bokeh.plotting
# import markdown


def home():

    col1, col2, col3 = st.columns([0.7,1,0.7])
    col2.image('./imagens/analisequant_logo-removebg.png')
    st.markdown("<h2 style='text-align: center; color: black;'>Bem Vindo ao Análise Quant</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: black;'>Uma plataforma de análises e estudos quantitativos do mercado financeiro.</h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: black;'>Veja o que você pode fazer:</h3>", unsafe_allow_html=True)
    st.markdown("***")
    st.markdown("<h4 style='text-align: center; color: black;'>Análise de Carteira</h4>", unsafe_allow_html=True)
    st.markdown("")
    col1, col2, col3, col4, col5  = st.columns([0.1,1,0.01,1,0.1])
    col2.image('./imagens/video_analise_carteira.gif')
    col4.markdown("")
    col4.markdown("<h5 style='text-align: left; color: black;'>- Inserir os ativos da sua carteira.</h5>", unsafe_allow_html=True)
    col4.markdown("<h5 style='text-align: left; color: black;'>- Calcular o BETA e ver as informações sobre Hedge.</h5>", unsafe_allow_html=True)
    col4.markdown("<h5 style='text-align: left; color: black;'>- Analisar as correlações entre os ativos da sua carteira e principais indices.</h5>", unsafe_allow_html=True)
    col4.markdown("<h5 style='text-align: left; color: black;'>- Verificar a distribuição Setorial.</h5>", unsafe_allow_html=True)
    col4.markdown("<h5 style='text-align: left; color: black;'>- Análise de Risco x Retorno de cada Ativo.</h5>", unsafe_allow_html=True)
    col4.markdown("<h5 style='text-align: left; color: black;'>- Simulação da Rentabilidade da sua Carteira.</h5>", unsafe_allow_html=True)
    st.markdown("***")
    st.markdown("<h4 style='text-align: center; color: black;'>Correlações</h4>", unsafe_allow_html=True)
    st.markdown("")
    col1, col2, col3, col4, col5  = st.columns([0.1,1,0.01,1,0.1])
    col2.image('./imagens/video_correlacao.gif')
    col4.markdown("")
    col4.markdown("")
    col4.markdown("")
    col4.markdown("<h5 style='text-align: left; color: black;'>- Verificar as correlações entre os ativos.</h5>", unsafe_allow_html=True)
    col4.markdown("<h5 style='text-align: left; color: black;'>- Comparar a correlação com os principais indices.</h5>", unsafe_allow_html=True)
    col4.markdown("<h5 style='text-align: left; color: black;'>- Analisar a correlação no tempo.</h5>", unsafe_allow_html=True)
    st.markdown("***")
    st.markdown("<h4 style='text-align: center; color: black;'>Sazonalidade do Mercado</h4>", unsafe_allow_html=True)
    st.markdown("")
    col1, col2, col3, col4, col5  = st.columns([0.1,1,0.01,1,0.1])
    col2.image('./imagens/video_sazonalidade.gif')
    col4.markdown("")
    col4.markdown("")
    col4.markdown("")
    col4.markdown("<h5 style='text-align: left; color: black;'>- Analisar a sazonalidade de um deteminado ativo.</h5>", unsafe_allow_html=True)
    col4.markdown("<h5 style='text-align: left; color: black;'>- Ações e Indices Brasileiros e dos Estados Unidos.</h5>", unsafe_allow_html=True)
    col4.markdown("<h5 style='text-align: left; color: black;'>- Verificar a rentabilidade mensal.</h5>", unsafe_allow_html=True)
    col4.markdown("<h5 style='text-align: left; color: black;'>- Identificar padrões de comportamento ao longo do ano.</h5>", unsafe_allow_html=True)
    st.markdown("***")
    st.markdown("<h4 style='text-align: center; color: black;'>Raio-X do Mercado</h4>", unsafe_allow_html=True)
    st.markdown("")
    col1, col2, col3, col4, col5  = st.columns([0.1,1,0.01,1,0.1])
    col2.image('./imagens/video_raiox.gif')
    col4.markdown("")
    col4.markdown("")
    col4.markdown("")
    col4.markdown("<h5 style='text-align: left; color: black;'>- Verificar como estão as bolsas pelo mundo em tempo real.</h5>", unsafe_allow_html=True)
    col4.markdown("<h5 style='text-align: left; color: black;'>- Dados e informações das principais bolsas.</h5>", unsafe_allow_html=True)


###### Com  BOKEH TABS

#     from bokeh.io import show
#     from bokeh.models import Panel, Tabs
#     from bokeh.plotting import figure
#     from bokeh.models import PreText
#     from bokeh.models import Paragraph
#
#     # p1 = figure(plot_width=300, plot_height=300)
#     # p1.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)
#     # tab1 = Panel(child=p1, title="circle")
#     #
#     # p2 = figure(plot_width=300, plot_height=300)
#     # p2.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=3, color="navy", alpha=0.5)
#     # tab2 = Panel(child=p2, title="line")
#     #
#     # p3 = PreText(text="""Your text is initialized with the 'text' argument.
#     # The remaining Paragraph arguments are 'width' and 'height'. For this example,
#     # those values are 500 and 100, respectively.""",
#     # width=500, height=100)
#     # tab3 = Panel(child=p3, title="Pretext")
#     #
#     # p4 = Paragraph(text="""Your text is initialized with the 'text' argument.  The
#     # remaining Paragraph arguments are 'width' and 'height'. For this example, those values
#     # are 200 and 100, respectively.""",
#     # width=200, height=100)
#     # tab4 = Panel(child=p4, title="Paragraph")
#     #
#     #
#     # st.bokeh_chart(Tabs(tabs=[tab1, tab2, tab3, tab4]))
#
#     def analise_carteira_panel():
#         text = """
# **Análise de Carteira**
#
#  Inserir os ativos da sua carteira.
#
#  Calcular o BETA e ver as informações sobre Hedge.
#
#  Analisar as correlações entre os ativos da sua carteira e principais indices.
#
#  Verificar a distribuição Setorial.
#
#  Análise de Risco x Retorno de cada Ativo.
#
#  Simulação da Rentabilidade da sua Carteira.
#         """
#         grid = bokeh.layouts.grid(children=[[_image('analise_carteira'), _markdown(text)]],sizing_mode="stretch_width")
#         return bokeh.models.Panel(child=grid, title="Análise de Carteira")
#
#
#     def correlacao_panel():
#         text = """
# **Correlações**
#
#  Verificar as correlações entre os ativos.
#
#  Comparar a correlação com os principais indices.
#
#  Analisar a correlação no tempo.
#             """
#         grid = bokeh.layouts.grid(children=[[_image('correlacao'), _markdown(text)]], sizing_mode="stretch_width")
#         return bokeh.models.Panel(child=grid, title="Correlações")
#
#
#     def sazonalidade_panel():
#         text = """
# **Sazonalidade do Mercado**
#
#  Analisar a sazonalidade de um deteminado ativo.
#
#  Ações e Indices Brasileiros e dos Estados Unidos.
#
#  Verificar a rentabilidade mensal.
#
#  Identificar padrões de comportamento ao longo do ano.
#
#
#             """
#         grid = bokeh.layouts.grid(children=[[_image('sazonalidade'), _markdown(text)]], sizing_mode="stretch_width")
#         return bokeh.models.Panel(child=grid, title="Sazonalidade do Mercado")
#
#
#     def raiox_panel():
#         text = """
# **Raio-X do Mercado**
#
#  Verificar como estão as bolsas pelo mundo em tempo real.
#
#  Dados e informações das principais bolsas.
#
#             """
#         grid = bokeh.layouts.grid(children=[[_image('raiox'), _markdown(text)]], sizing_mode="stretch_width")
#         return bokeh.models.Panel(child=grid, title="Raio-X do Mercado")
#
#     def _image(pagina):
#         if pagina == 'analise_carteira':
#             return bokeh.models.widgets.markups.Div(
#                 text='<img src="imagens/video_analise_carteira.gif" style="width:400px"></img>',
#             sizing_mode="scale_both",
#             )
#         if pagina == 'correlacao':
#             return bokeh.models.widgets.markups.Div(
#                 text='<img src="http://www.openmindlab.com.br/imagens/video_correlacao.gif" style="width:400px"></img>',
#             sizing_mode="scale_both",
#             )
#         if pagina == 'sazonalidade':
#             return bokeh.models.widgets.markups.Div(
#                 text='<img src="http://www.openmindlab.com.br/imagens/video_sazonalidade.gif" style="width:400px"></img>',
#             sizing_mode="scale_both",
#             )
#         if pagina == 'raiox':
#             return bokeh.models.widgets.markups.Div(
#                 text='<img src="http://www.openmindlab.com.br/imagens/video_raiox.gif" style="width:400px"></img>',
#             sizing_mode="scale_both",
#             )
#
#
#     def _markdown(text):
#         return bokeh.models.widgets.markups.Div(
#             text=markdown.markdown(text), sizing_mode="stretch_width"
#         )
#
#     tabs = bokeh.models.Tabs(tabs=[analise_carteira_panel(),correlacao_panel(),sazonalidade_panel(), raiox_panel(),])
#     col1, col2, col3 = st.columns([0.4, 1, 0.7])
#     col2.bokeh_chart(tabs)