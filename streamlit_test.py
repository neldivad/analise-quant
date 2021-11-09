from pandas.io.parsers import read_csv
import streamlit as st
import pandas as pd 
import numpy as np
import altair as alt
from itertools import cycle

from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
from streamlit.legacy_caching.caching import cache

def exemplo():
    #Example controlers
    st.sidebar.subheader("St-AgGrid example options")

    sample_size = st.sidebar.number_input("rows", min_value=10, value=10)
    grid_height = st.sidebar.number_input("Grid height", min_value=200, max_value=800, value=200)

    return_mode = st.sidebar.selectbox("Return Mode", list(DataReturnMode.__members__), index=1)
    return_mode_value = DataReturnMode.__members__[return_mode]

    update_mode = st.sidebar.selectbox("Update Mode", list(GridUpdateMode.__members__), index=6)
    update_mode_value = GridUpdateMode.__members__[update_mode]

    #enterprise modules
    enable_enterprise_modules = st.sidebar.checkbox("Enable Enterprise Modules")
    if enable_enterprise_modules:
        enable_sidebar =st.sidebar.checkbox("Enable grid sidebar", value=False)
    else:
        enable_sidebar = False

    #features
    fit_columns_on_grid_load = st.sidebar.checkbox("Fit Grid Columns on Load")

    enable_selection=st.sidebar.checkbox("Enable row selection", value=True)
    if enable_selection:
        st.sidebar.subheader("Selection options")
        selection_mode = st.sidebar.radio("Selection Mode", ['single','multiple'])
        
        use_checkbox = st.sidebar.checkbox("Use check box for selection")
        if use_checkbox:
            groupSelectsChildren = st.sidebar.checkbox("Group checkbox select children", value=True)
            groupSelectsFiltered = st.sidebar.checkbox("Group checkbox includes filtered", value=True)

        if ((selection_mode == 'multiple') & (not use_checkbox)):
            rowMultiSelectWithClick = st.sidebar.checkbox("Multiselect with click (instead of holding CTRL)", value=False)
            if not rowMultiSelectWithClick:
                suppressRowDeselection = st.sidebar.checkbox("Suppress deselection (while holding CTRL)", value=False)
            else:
                suppressRowDeselection=False
        st.sidebar.text("___")

    enable_pagination = st.sidebar.checkbox("Enable pagination", value=False)
    if enable_pagination:
        st.sidebar.subheader("Pagination options")
        paginationAutoSize = st.sidebar.checkbox("Auto pagination size", value=True)
        if not paginationAutoSize:
            paginationPageSize = st.sidebar.number_input("Page size", value=5, min_value=0, max_value=sample_size)
        st.sidebar.text("___")


    df = pd.DataFrame({'month': [1, 4, 7, 10],'year': [2012, 2014, 2013, 2014],'sale':[55, 40, 84, 31]})


    #Infer basic colDefs from dataframe types
    gb = GridOptionsBuilder.from_dataframe(df)

    #customize gridOptions
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)

    # gb.configure_column("date_tz_aware", type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='yyyy-MM-dd HH:mm zzz', pivot=True)

    # gb.configure_column("apple", type=["numericColumn","numberColumnFilter","customNumericFormat"], precision=2, aggFunc='sum')
    # gb.configure_column("banana", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=1, aggFunc='avg')
    # gb.configure_column("chocolate", type=["numericColumn", "numberColumnFilter", "customCurrencyFormat"], custom_currency_symbol="R$", aggFunc='max')

    #configures last row to use custom styles based on cell's value, injecting JsCode on components front end

    cellsytle_jscode = JsCode("""
    function(params) {
        if (params.value == 'A') {
            return {
                'color': 'white',
                'backgroundColor': 'darkred'
                
            }
        } else {
            return {
                'color': 'black',
                'backgroundColor': 'white'
            }
        }
    };
    """)
    # gb.configure_column("month", cellStyle=cellsytle_jscode)

    if enable_sidebar:
        gb.configure_side_bar()

    if enable_selection:
        gb.configure_selection(selection_mode)
        if use_checkbox:
            gb.configure_selection(selection_mode, use_checkbox=True, groupSelectsChildren=groupSelectsChildren, groupSelectsFiltered=groupSelectsFiltered)
        if ((selection_mode == 'multiple') & (not use_checkbox)):
            gb.configure_selection(selection_mode, use_checkbox=False, rowMultiSelectWithClick=rowMultiSelectWithClick, suppressRowDeselection=suppressRowDeselection)

    if enable_pagination:
        if paginationAutoSize:
            gb.configure_pagination(paginationAutoPageSize=True)
        else:
            gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=paginationPageSize)

    gb.configure_grid_options(domLayout='normal')
    gridOptions = gb.build()

    #Display the grid
    st.header("Streamlit Ag-Grid")

    grid_response = AgGrid(
        df, 
        gridOptions=gridOptions,
        height=grid_height, 
        width='100%',
        data_return_mode=return_mode_value, 
        update_mode=update_mode_value,
        fit_columns_on_grid_load=fit_columns_on_grid_load,
        allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
        enable_enterprise_modules=enable_enterprise_modules,
        )



    df = grid_response['data']
    st.dataframe(df)
    # selected = grid_response['selected_rows']
    # selected_df = pd.DataFrame(selected)

    with st.spinner("Displaying results..."):
        st.subheader("Returned grid data:")
        # st.dataframe(grid_response['data'])

        st.subheader("grid selection:")
        st.write(grid_response['selected_rows'])

def exemplo_enxuto():
    df = pd.DataFrame({'month': [1, 4, 7, 10],'year': [2012, 2014, 2013, 2014],'sale':[55, 40, 84, 31]})
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
    gb.configure_selection('single', use_checkbox=True, groupSelectsChildren=True, groupSelectsFiltered=True)
    gb.configure_grid_options(domLayout='normal')
    gridOptions = gb.build()
    #Display the grid
    st.header("Streamlit Ag-Grid")

    return_mode = ['AS_INPUT', 'FILTERED', 'FILTERED_AND_SORTED']
    return_mode_value = DataReturnMode.__members__[return_mode[2]]
    update_mode = ['NO_UPDATE', 'MANUAL', 'VALUE_CHANGED', 'SELECTION_CHANGED', 'FILTERING_CHANGED', 'SORTING_CHANGED', 'MODEL_CHANGED']
    update_mode_value = GridUpdateMode.__members__[update_mode[6]]

    grid_response = AgGrid(
        df, 
        gridOptions=gridOptions,
        height=200, 
        width='100%',
        data_return_mode=return_mode_value, 
        update_mode=update_mode_value,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
        )
    # df = grid_response['data']
    # st.dataframe(df)
    # st.subheader("Returned grid data:")
    st.dataframe(grid_response['data'])
    # st.subheader("grid selection:")
    # st.write(grid_response['selected_rows'])


def homol():
    lista = ['PETR4', 'WEGE3', 'VALE3', 'MGLU3', 'EQTL3']
    if 'portifolio' not in st.session_state:
        st.session_state.portifolio = pd.DataFrame(columns=['Ação', 'Qtde'])
    with st.form(key='Carteira_Inserir_Ativos'):
        st.markdown('Insira os Ativos que compõem sua Carteira')
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.papel = st.selectbox('Insira o Ativo', lista, help='Insira o ativo no caixa de seleção(Não é necessario apagar o ativo, apenas clique e digite as iniciais que a busca irá encontrar)')
        with col2:
            st.session_state.lote = st.number_input('Quantidade', value = 100, step = 100)

        col1, col2, col3, col4 = st.columns([.4,.7,.9,1]) # Cria as colunas para disposição dos botões. Os numeros são os tamanhos para o alinhamento
        with col2:
            if st.form_submit_button(label='Inserir Ativo', help='Clique para inserir o Ativo e a Quantidade na Carteira'):
                if any(st.session_state.portifolio['Ação']==st.session_state.papel): # Verificar se o Ativo já existe no DataFrame(Carteira)
                    st.error('Ativo já existe na carteira. Por favor verifique!')
                else:
                    if 'grid_response' in st.session_state:
                        st.session_state.portifolio = st.session_state.grid_response['data']
                    st.session_state.portifolio = st.session_state.portifolio.append({'Ação': st.session_state.papel, 'Qtde': st.session_state.lote}, ignore_index=True)
                    st.session_state.portifolio['Qtde'] = pd.to_numeric(st.session_state.portifolio['Qtde'])
        with col3:
            if st.form_submit_button(label='Apagar Ativo', help='Clique para apagar o Ativo selecionado'):
                if len(st.session_state.papel_selecao) != 0:
                    st.session_state.portifolio.drop(st.session_state.portifolio[st.session_state.portifolio['Ação'] == st.session_state.papel_selecao[0].get('Ação')].index, inplace = True)
                else:
                    st.warning("Vc não selecionou nada cacete!")
        with col4:
            if st.form_submit_button(label='Limpar Carteira', help='Clique para apagar todos os Ativos da Carteira'):
                st.session_state.portifolio = pd.DataFrame(columns=['Ação', 'Qtde'])

    if st.checkbox('Upload da Carteira (Somente arquivos salvos previamentes no AnaliseQuant)'):    
        file_carteira = st.file_uploader('Upload Carteira')
        if file_carteira is not None:
            st.session_state.portifolio = ''
            st.session_state.portifolio = pd.read_csv(file_carteira,index_col=0)
                
    gb = GridOptionsBuilder.from_dataframe(st.session_state.portifolio)
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False)
    gb.configure_column('Qtde', editable=True, singleClickEdit=True)
    gb.configure_selection('single', use_checkbox=True, groupSelectsChildren=True, groupSelectsFiltered=True)
    gb.configure_grid_options(domLayout='normal')
    gridOptions = gb.build()
    #Display the grid
    return_mode = ['AS_INPUT', 'FILTERED', 'FILTERED_AND_SORTED']
    return_mode_value = DataReturnMode.__members__[return_mode[2]]
    update_mode = ['NO_UPDATE', 'MANUAL', 'VALUE_CHANGED', 'SELECTION_CHANGED', 'FILTERING_CHANGED', 'SORTING_CHANGED', 'MODEL_CHANGED']
    update_mode_value = GridUpdateMode.__members__[update_mode[6]]

    st.session_state.grid_response = AgGrid(
        st.session_state.portifolio, 
        gridOptions=gridOptions,
        height=200, 
        width='100%',
        data_return_mode=return_mode_value, 
        update_mode=update_mode_value,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
        )
    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(st.session_state.portifolio)
    st.download_button(label="Download Carteira como CSV", data=csv, file_name='carteira_analisequant.csv', mime='text/csv')

    # st.session_state.portifolio = grid_response['data']
    st.write('Grid DATA')
    st.dataframe(st.session_state.grid_response['data'])
    st.write('DataFrame DATA')
    st.dataframe(st.session_state.portifolio)
    # st.subheader("grid selection:")
    # st.write(st.session_state.grid_response['selected_rows'])
    st.session_state.papel_selecao = st.session_state.grid_response['selected_rows']

# exemplo()
# exemplo_enxuto()
homol()