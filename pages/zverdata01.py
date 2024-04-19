import streamlit as st
import pandas as pd
from deta import Deta

deta = Deta(st.secrets["deta_key"])

def row_style(row):
    if row['paycon'] == 'SI++':
        return pd.Series('background-color: #7986cb; color:#000000', row.index)
    elif row['paycon'] == 'PENDIENTE X DIFERENCIA':
        return pd.Series('background-color: #ff6f00; color:#000000', row.index)
    elif row['paycon'] == 'SI':
        return pd.Series('background-color: #8ede99; color:#000000', row.index)
    elif row['paycon'] == 'PENDIENTE':
        return pd.Series('background-color: #fdd834; color:#000000', row.index)
    else:
        return pd.Series('', row.index)

def row_style_2(row):
    if row['Distrito'] in ('Andino', 'Centro Llanos', 'Lara', 'Llanos Occidentales', 'Nor Oriente', 'Yaracuy' ):
        return pd.Series('background-color: #8eddf9; color:#000000', row.index)
    else:
        return pd.Series('background-color: #eeeeee; color:#000229', row.index)

def row_style_3(row):
    if row['index']=='Ministro Licenciado' :
        return pd.Series('background-color: #eeeeee; color:#000229', row.index)


@st.cache_data
def load_data():
    # # Carga el Pronda
    Prondamin24 = deta.Base('Prondamin2024C')
    Pronda24 = Prondamin24.fetch(limit=4500)
    Pronda24items = Pronda24.items
    Pronda24last = Pronda24.last
    Pronda24count = Pronda24.count
    return (pd.DataFrame(Pronda24items), Pronda24last, Pronda24count)
    
@st.cache_data
def load_data02():
    Pronda24 = deta.Base('Prondamin2024C')
    res = Pronda24.fetch()
    all_items = res.items

    while res.last:
        res = Pronda24.fetch(last=res.last)
        all_items += res.items
    return pd.DataFrame(all_items)
    
# Boolean to resize the dataframe, stored as a session state variable
# st.checkbox("Use container width", value=False, key="use_container_width")

#df, lastdf, countdf = load_data()
#df
#lastdf
#countdf

df2 = load_data02()
df2
df2 = df2.reindex(columns=['distrito', 'categoría', 'key', 'nombre', 'apellido', 'emails', 'teléfonos', 'modalidad', 'paycon', 'montoApagar', 'fuenteOrigen', 'referenciaPago', 'fechaPago', 'montoPago' ]) #Reordena las columnas como se mostraran
df2_color = df2.style.apply(row_style, axis=1)  #Coloriza las filas
df2_color
