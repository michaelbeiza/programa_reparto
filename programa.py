import streamlit as st
import pandas as pd
import urllib.parse
from datetime import date

# Configuración de la página para que se vea bien en el móvil
st.set_page_config(page_title="Rutas Alma Nomad", page_icon="🥐", layout="centered")

st.title("🚚 Ruta de Hoy")
st.write(f"**Fecha:** {date.today().strftime('%d/%m/%Y')}")

# --- SIMULACIÓN DE DATOS (Esto vendría de tu Access o Excel exportado) ---
datos_hoy = {
    "Hora": ["08:30:00", "08:40:00", "09:00:00", "11:05:00"],
    "Cliente": ["Natif 1 FR", "Pan y Pepinillos", "La Deseada", "Araia"],
    "Direccion": [
        "C. de Francisco de Rojas, 7, Local 2, Chamberí, 28010 Madrid",
        "C. de El Escorial, 2, Centro, 28004 Madrid",
        "Calle de José Abascal, 53, Chamberí, 28003 Madrid",
        "C/ de Murillo, 3, Chamberí, 28010 Madrid"
    ],
    "Estado": ["Pendiente", "Pendiente", "Pendiente", "Pendiente"]
}
df_ruta = pd.DataFrame(datos_hoy)

# --- VISTA DEL CONDUCTOR ---
st.subheader("📍 Paradas")

# Recorremos cada cliente de la ruta
for index, fila in df_ruta.iterrows():
    # Creamos una tarjeta desplegable para cada parada
    with st.expander(f"🕒 {fila['Hora']} - {fila['Cliente']}"):
        st.write(f"**Dirección:** {fila['Direccion']}")
        
        # Generamos el enlace universal de Google Maps
        # api=1&destination= indica a Maps que calcule la ruta desde tu ubicación actual
        direccion_codificada = urllib.parse.quote(fila['Direccion'])
        link_maps = f"https://www.google.com/maps/dir/?api=1&destination={direccion_codificada}"
        
        col1, col2 = st.columns(2)
        with col1:
            # Botón que abre Google Maps en el móvil
            st.link_button("🗺️ NAVEGAR", link_maps, use_container_width=True)
        with col2:
            # Un checkbox para que el conductor marque si ya lo entregó
            st.checkbox("✅ Entregado", key=f"check_{index}")

# Zona de Administración (Oculta en un menú desplegable)
with st.sidebar:
    st.header("⚙️ Admin")
    st.write("Vista previa de los datos brutos cargados:")
    st.dataframe(df_ruta)