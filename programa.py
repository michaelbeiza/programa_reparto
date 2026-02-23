import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Rutas de Reparto", page_icon="🚚")

st.title("🚚 Ruta del Día")

try:
    # 1. Leer los dos archivos CSV directamente desde tu GitHub
    df_clientes = pd.read_csv("clientes.csv")
    df_ruta = pd.read_csv("ruta_hoy.csv")

    # 2. Cruzar los datos (Asegúrate de que la columna del nombre del cliente se llame igual en ambos)
    # Suponiendo que la columna se llama "Cliente" en ambos archivos:
    df_completo = pd.merge(df_ruta, df_clientes, on="Cliente", how="left")

    # 3. Mostrar la ruta al conductor
    for index, fila in df_completo.iterrows():
        # Asumimos que tienes columnas llamadas 'Hora de entrega' y 'Direccion'
        hora = fila.get('Hora de entrega', 'Sin hora')
        cliente = fila['Cliente']
        direccion = fila.get('Direccion', 'Dirección no encontrada')

        with st.expander(f"🕒 {hora} - {cliente}"):
            st.write(f"📍 {direccion}")
            
            # Crear enlace de Maps
            direccion_codificada = urllib.parse.quote(str(direccion))
            link_maps = f"https://www.google.com/maps/dir/?api=1&destination={direccion_codificada}"
            
            st.link_button("🗺️ NAVEGAR", link_maps)

except FileNotFoundError:
    st.error("⚠️ Faltan los archivos. Asegúrate de que 'clientes.csv' y 'ruta_hoy.csv' están subidos a GitHub.")