import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Rutas de Reparto", page_icon="🚚")

st.title("🚚 Ruta del Día")

try:
    # 1. Leer los archivos. 
    # Añadimos sep=";" porque Excel en España suele exportar los CSV separando por punto y coma.
    df_clientes = pd.read_csv("clientes.csv", encoding="latin1", sep=";")
    df_ruta = pd.read_csv("ruta_hoy.csv", encoding="latin1", sep=";")

    # 2. Limpieza de seguridad...
    df_clientes.columns = df_clientes.columns.str.strip()
    df_ruta.columns = df_ruta.columns.str.strip()

    # Añade esto temporalmente para investigar:
    st.write("🕵️ Columnas de clientes detectadas:", df_clientes.columns.tolist())
    st.write("🕵️ Columnas de ruta detectadas:", df_ruta.columns.tolist())

    # 3. Cruzar los datos por la columna "Cliente"
    df_completo = pd.merge(df_ruta, df_clientes, on="Cliente", how="left")

    # 4. Mostrar la ruta al conductor
    for index, fila in df_completo.iterrows():
        # Usamos los nombres exactos de las columnas de tus nuevos archivos
        hora = fila.get('Hora', 'Sin hora')
        cliente = fila.get('Cliente', 'Desconocido')
        direccion = fila.get('Direccion', 'Dirección no encontrada')

        with st.expander(f"🕒 {hora} - {cliente}"):
            st.write(f"📍 {direccion}")
            
            # Crear enlace correcto de Google Maps para navegación
            if direccion != 'Dirección no encontrada':
                direccion_codificada = urllib.parse.quote(str(direccion))
                # Esta URL sí abre Google Maps buscando la dirección exacta
                link_maps = f"https://www.google.com/maps/search/?api=1&query={direccion_codificada}"
                
                st.link_button("🗺️ NAVEGAR EN MAPS", link_maps)

except FileNotFoundError as e:
    st.error(f"⚠️ Falta un archivo. Comprueba que están subidos: {e.filename}")
except KeyError as e:
    st.error(f"⚠️ Hay un problema con los nombres de las columnas. Falta: {e}")
except Exception as e:
    st.error(f"⚠️ Error inesperado: {e}")