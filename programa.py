import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Rutas de Reparto", page_icon="🚚")

st.title("🚚 Ruta del Día")

try:
    # 1. Leer los archivos usando la COMA como separador
    df_clientes = pd.read_csv("clientes.csv", encoding="latin1", sep=",")
    df_ruta = pd.read_csv("ruta_hoy.csv", encoding="latin1", sep=",")

    # 2. Limpieza de seguridad: quitar espacios vacíos accidentales
    df_clientes.columns = df_clientes.columns.str.strip()
    df_ruta.columns = df_ruta.columns.str.strip()

    # 3. Cruzar los datos por la columna "Cliente"
    df_completo = pd.merge(df_ruta, df_clientes, on="Cliente", how="left")

    # 4. Mostrar la ruta al conductor
    for index, fila in df_completo.iterrows():
        # Usamos los nombres de columnas de tu captura
        hora = fila.get('fecha', 'Sin hora') # He puesto fecha porque no veo 'Hora' en tu captura
        cliente = fila.get('Cliente', 'Desconocido')
        
        # En clientes.csv la dirección se llama 'DireccionCl'
        direccion = fila.get('DireccionCl', 'Dirección no encontrada')

        with st.expander(f"🕒 {hora} - {cliente}"):
            st.write(f"📍 {direccion}")
            
            # Crear enlace correcto de Google Maps para navegación
            if direccion != 'Dirección no encontrada':
                direccion_codificada = urllib.parse.quote(str(direccion))
                link_maps = f"https://www.google.com/maps/search/?api=1&query={direccion_codificada}"
                st.link_button("🗺️ NAVEGAR EN MAPS", link_maps)

except FileNotFoundError as e:
    st.error(f"⚠️ Falta un archivo. Comprueba que están subidos: {e.filename}")
except KeyError as e:
    st.error(f"⚠️ Hay un problema con los nombres de las columnas. Falta: {e}")
except Exception as e:
    st.error(f"⚠️ Error inesperado: {e}")