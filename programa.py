import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Rutas de Reparto", page_icon="🚚")

st.title("🚚 Ruta del Día")

# Botón de subida
archivo_subido = st.file_uploader("Sube el archivo de la ruta de hoy", type=["xlsx", "xls", "csv"])

if archivo_subido is not None:
    try:
        # 1. Leer archivos
        if archivo_subido.name.endswith('.xlsx'):
            df_ruta = pd.read_excel(archivo_subido, engine='openpyxl')
        elif archivo_subido.name.endswith('.xls'):
            df_ruta = pd.read_excel(archivo_subido, engine='xlrd')
        else:
            df_ruta = pd.read_csv(archivo_subido, encoding="latin1", sep=",", engine="python")

        df_clientes = pd.read_csv("clientes.csv", encoding="latin1", sep=",")

        # 2. Limpieza básica anti-errores
        df_ruta.columns = df_ruta.columns.str.strip()
        df_clientes.columns = df_clientes.columns.str.strip()
        
        if 'Cliente' in df_ruta.columns and 'Cliente' in df_clientes.columns:
            df_ruta['Cliente'] = df_ruta['Cliente'].astype(str).str.strip().str.upper()
            df_clientes['Cliente'] = df_clientes['Cliente'].astype(str).str.strip().str.upper()

        # 3. Cruzar datos
        df_completo = pd.merge(df_ruta, df_clientes, on="Cliente", how="left")

        st.success("✅ Ruta cargada con éxito")

        # 4. Mostrar la lista simplificada
        for index, fila in df_completo.iterrows():
            cliente = fila.get('Cliente', 'Desconocido')
            direccion = fila.get('DireccionCl', 'Dirección no encontrada')

            with st.container():
                st.write("---") # Línea separadora visual
                st.subheader(f"👤 {cliente}")
                
                if pd.isna(direccion) or str(direccion).strip() == 'Dirección no encontrada':
                    st.warning("⚠️ Dirección no encontrada en la base de datos (clientes.csv)")
                else:
                    st.write(f"📍 {direccion}")
                    
                    # Preparamos la dirección para las URLs
                    direccion_codificada = urllib.parse.quote(str(direccion))
                    
                    # Enlaces oficiales para forzar la apertura en la app del móvil
                    link_gmaps = f"https://www.google.com/maps/dir/?api=1&destination={direccion_codificada}"
                    link_waze = f"https://waze.com/ul?q={direccion_codificada}&navigate=yes"
                    
                    # Dividimos en TRES columnas para que quepa todo bien ordenado
                    col1, col2, col3 = st.columns([1, 1, 1])
                    
                    with col1:
                        # Botón Google Maps
                        st.link_button("🗺️ MAPS", link_gmaps, use_container_width=True)
                        
                    with col2:
                        # Botón Waze
                        st.link_button("🚙 WAZE", link_waze, use_container_width=True)
                    
                    with col3:
                        # Casilla de entregado
                        st.checkbox("✅ Entregado", key=f"entregado_{index}")

    except Exception as e:
        st.error(f"⚠️ Error al procesar: {e}")
else:
    st.info("👆 Sube el archivo Excel o CSV para empezar.")