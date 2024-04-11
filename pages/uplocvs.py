
import streamlit as st
import pandas as pd
from deta import Deta

def check_csv_header(header):
    #required_columns = ['Fecha', 'Descripcion', 'Referencia', 'Egreso', 'Ingreso']
    required_columns = ['FECHA', 'DESCRIPCION', 'REFERENCIA', 'EGRESO', 'INGRESO']
    return all(column in header for column in required_columns)
    
# Carga el archivo CSV desde el usuario
uploaded_file = st.file_uploader("Cargar archivo CSV", type=["csv"])

if uploaded_file is not None:
    # Lee el archivo CSV en un DataFrame
    # Leer el archivo CSV
    df = pd.read_csv(uploaded_file)

    # Verificar si el archivo es CSV
    if not uploaded_file.name.lower().endswith('.csv'):
        st.error('El archivo seleccionado no es un archivo CSV válido.')
        #return

    # Verificar si la cabecera cumple con los campos requeridos
    elif not check_csv_header(df.columns):
        st.error('El archivo CSV debe tener las siguientes columnas: Fecha, Descripcion, Referencia, Egreso, Ingreso.')
        #return

    else:
        # Mostrar el DataFrame si todas las verificaciones son exitosas
        st.header('Contenido del archivo CSV')
        st.write(df)
    
    
    
        
        #df = pd.read_csv(uploaded_file)
        dfingresoXpm = df[df['DESCRIPCION'] == 'NC - PAGO MOVIL INTERBANCARIO']
        dfingresoXtrans = df[df['DESCRIPCION'] == 'NC - TRANSFERENCIA DE FONDOS VIA INTERNET']
        frames = [dfingresoXpm, dfingresoXtrans]
    
        dfingreso = pd.concat(frames)
        # Muestra el DataFrame
        st.write(dfingreso)

        DatBan = dfingreso.reindex(columns=['FECHA', 'DESCRIPCION', 'REFERENCIA', 'INGRESO'])
        DatBan['REFERENCIA'] = df['REFERENCIA'].apply(lambda x: str(x)[-4:])
        DatBan['INGRESO'] = DatBan['INGRESO'].str.replace(',', '.').astype(float)
        DatBan['INGRESO'] = pd.to_numeric(DatBan['INGRESO'])
        
        # Muestra el DataFrame
        # st.write(DatBan)
        
        # Compara Df.REFERENCIA con dfPronda24.referenciaPago
        DatBan['REFERENCIA'] = DatBan['REFERENCIA'].astype(str)
        dfPronda24['referenciaPago'] = dfPronda24['referenciaPago'].astype(str)
        
        #dfnew = df[df['REFERENCIA'].isin(dfPronda24['referenciaPago'])]
        #dfnew = dfPronda24[dfPronda24['referenciaPago'].isin(df['REFERENCIA'])]
        
        # datban_verif = pd.merge(df, dfPronda24, left_on='REFERENCIA', right_on='referenciaPago', how='inner')
        # 'datban_verif = '
        # datban_verif
        
        DatBanVerif = DatBan[DatBan['REFERENCIA'].isin(dfPronda24['referenciaPago'])]
        DatBanVerif1 = DatBanVerif.rename(columns={'REFERENCIA': 'key'})
        
        DatBanVerif1
        # grabo DatBanVerif en Deta BD: DBanVerif2024
        dbvreg = DatBanVerif1.to_dict('records')
        cont=1
        for registro in dbvreg:
            #registro
            DBanV24.put(registro)
            st.toast('se ha cargado el registro: '+str(cont))
            cont+=1
        
        referencias = set(DatBanVerif1['key'])
        dfPronda24.loc[dfPronda24['referenciaPago'].isin(referencias), 'paycon'] = 'SI'
        #dfPronda24.style.applymap(color_paycon, subset=['paycon'])
        dfPronda24['paycon'] = dfPronda24.apply(update_paycon, axis=1)
        dfPronda24_ordenado = dfPronda24.sort_values(by='paycon', ascending=False)
        dfPronda24B = dfPronda24_ordenado.style.apply(row_style, axis=1)  #Coloriza las filas
        
        dfPronda24B



# lee csv desde detadrive
# deta = Deta(st.secrets["deta_key"])
# drive2024 = deta.Drive("datoscvsminec")
# dicPminec2024 =  drive2024.list()
# dicPminec2024

# response = drive2024.get("data2024-01bkp.csv")
# content = response.read()
# type(content)

# # content
# df = pd.read_csv(response)
# df = pd.read_csv(content)
# df
