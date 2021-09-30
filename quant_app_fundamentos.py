import streamlit as st
import pandas as pd 
import numpy as np
import altair as alt
from itertools import cycle
import fundamentus

from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode

st.set_page_config(  # Alternate names: setup_page, page, layout
    layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
    initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
    page_title=None,  # String or None. Strings get appended with "• Streamlit".
    page_icon=None,  # String, anything supported by st.image, or None.
)


df = fundamentus.get_resultado()
df.reset_index(inplace=True)
df.columns=['Papel', 'Cotação', 'P/L','P/VP', 'PSR' ,'Div Yield', 'P/Ativos', 'P/Cap Giro', 'P/EBIT', 'P/Ativ Circ Liq', 
            'EV/EBIT','EV/EBITDA', 'Marg EBIT', 'Marg Liq', 'ROIC', 'ROE', 'Liq Corr', 'Vol $ méd (2m)', 'Patrim Liq', 'Div Br/ Patrim', 'Cres Rec (5a)']

#Infer basic colDefs from dataframe types
gb = GridOptionsBuilder.from_dataframe(df)
#customize gridOptions
gb.configure_selection('single')
gb.configure_grid_options(domLayout='normal')
gridOptions = gb.build()

st.header('Informações de Fundamentos')
grid_response = AgGrid(
    df, 
    gridOptions=gridOptions,
    height= 600, 
    width='100%',
    data_return_mode='FILTERED', 
    update_mode='SELECTION_CHANGED',
    fit_columns_on_grid_load=False,
    )

# st.write(grid_response['selected_rows'][0]['papel'])

# if len(grid_response['selected_rows']) == 1:
#     st.subheader("Seleção:")
#     selecao = fundamentus.get_papel(grid_response['selected_rows'][0]['Papel']) 
#     st.write(selecao)