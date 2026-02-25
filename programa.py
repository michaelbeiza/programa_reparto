import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Rutas de Reparto", page_icon="🚚")

st.title("🚚 Ruta del Día")

# 1. Botón de subida (acepta xls, xlsx y csv)
archivo_subido = st.file_uploader("Sube el archivo de la ruta de hoy", type=["xlsx", "xls", "csv"])

if archivo_subido is not None:
    try:
        # 2. Leer la ruta según el formato
        if archivo_subido.name.endswith('.xlsx'):
            df_ruta = pd.read_excel(archivo_subido, engine='openpyxl')
        elif archivo_subido.name.endswith('.xls'):
            df_ruta = pd.read_excel(archivo_subido, engine='xlrd')
        else:
            df_ruta = pd.read_csv(archivo_subido, encoding="latin1", sep=",", engine="python") # Cambia sep=";" si tu Excel usa punto y coma

        # 3. Leer los clientes (Asegúrate de que sep="," o sep=";" coincida con tu archivo fijo)
        df_clientes = pd.read_csv("clientes.csv", encoding="latin1", sep=",")

        # 4. LIMPIEZA EXTREMA PARA EVITAR LOS NaN
        # Quitar espacios en los nombres de las columnas
        df_ruta.columns = df_ruta.columns.str.strip()
        df_clientes.columns = df_clientes.columns.str.strip()
        
        # Limpiar la columna Cliente: quitar espacios a los lados y forzar mayúsculas
        if 'Cliente' in df_ruta.columns and 'Cliente' in df_clientes.columns:
            df_ruta['Cliente'] = df_ruta['Cliente'].astype(str).str.strip().str.upper()
            df_clientes['Cliente'] = df_clientes['Cliente'].astype(str).str.strip().str.upper()

        # 5. Cruzar los datos
        df_completo = pd.merge(df_ruta, df_clientes, on="Cliente", how="left")

        # 6. ORDENAR LAS HORAS COMO UN RELOJ (NO COMO TEXTO)
        # Asumiendo que la columna se llama 'fecha' como vimos en tu captura anterior
        if 'fecha' in df_completo.columns:
            # Convertimos a formato hora/fecha real, ignorando los errores si hay texto raro
            df_completo['Hora_Limpia'] = pd.to_datetime(df_completo['fecha'], format='mixed', errors='coerce')
            # Ordenamos por esa nueva columna
            df_completo = df_completo.sort_values(by="Hora_Limpia", ascending=True)

        st.success("✅ Ruta cargada, emparejada y ordenada")

        # 7. Mostrar la ruta
        for index, fila in df_completo.iterrows():
            # Extraer los datos limpios
            hora = fila.get('fecha', 'Sin hora') 
            cliente = fila.get('Cliente', 'Desconocido')
            direccion = fila.get('DireccionCl', 'Dirección no encontrada')

            with st.expander(f"🕒 {hora} - {cliente}"):
                # Si sigue habiendo NaN en la dirección, avisamos
                if pd.isna(direccion) or direccion == 'Dirección no encontrada':
                    st.warning("⚠️ No se encontró la dirección. Comprueba que este cliente existe en 'clientes.csv'.")
                else:
                    st.write(f"📍 {direccion}")
                    
                    # Generar enlace GPS
                    direccion_codificada = urllib.parse.quote(str(direccion))
                    link_maps = f"https://www.google.com/maps/dir/?api=1&destination={direccion_codificada}"
                    st.link_button("🗺️ NAVEGAR EN MAPS", link_maps)

    except Exception as e:
        st.error(f"⚠️ Error al procesar: {e}")

else:
    st.info("👆 Sube el archivo de Access/Excel con la ruta de hoy.")