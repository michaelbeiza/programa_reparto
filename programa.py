import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Rutas de Reparto", page_icon="🚚")

st.title("🚚 Ruta del Día")

# 1. Botón para que tu tío suba el archivo diario
archivo_subido = st.file_uploader("Sube el archivo de la ruta de hoy (Excel o CSV)", type=["xlsx", "csv"])

if archivo_subido is not None:
    try:
        # 2. Leer el archivo que acaba de subir tu tío
        if archivo_subido.name.endswith('.xlsx'):
            # Si sube un Excel, lo leemos directamente (¡Cero problemas de comas/puntos y comas!)
            df_ruta = pd.read_excel(archivo_subido)
        else:
            # Si sube un CSV por inercia, intentamos adivinar el separador automáticamente
            df_ruta = pd.read_csv(archivo_subido, encoding="latin1", sep=None, engine="python")

        # Limpiar columnas de la ruta
        df_ruta.columns = df_ruta.columns.str.strip()

        # 3. Leer la base de datos de clientes (este sigue fijo en tu GitHub)
        # Asegúrate de poner el sep="," o sep=";" según cómo esté guardado tu clientes.csv actual
        df_clientes = pd.read_csv("clientes.csv", encoding="latin1", sep=",")
        df_clientes.columns = df_clientes.columns.str.strip()

        # 4. Cruzar los datos
        df_completo = pd.merge(df_ruta, df_clientes, on="Cliente", how="left")

        # 5. Ordenar por hora (desde el más temprano por la mañana)
        # Cambia "fecha" por el nombre exacto de la columna de la hora si es distinto
        if 'fecha' in df_completo.columns:
            df_completo = df_completo.sort_values(by="fecha", ascending=True)

        st.success("✅ Ruta cargada y ordenada correctamente")

        # 6. Mostrar la ruta al conductor
        for index, fila in df_completo.iterrows():
            hora = fila.get('fecha', 'Sin hora')
            cliente = fila.get('Cliente', 'Desconocido')
            direccion = fila.get('DireccionCl', 'Dirección no encontrada')

            with st.expander(f"🕒 {hora} - {cliente}"):
                st.write(f"📍 {direccion}")
                
                if direccion != 'Dirección no encontrada':
                    direccion_codificada = urllib.parse.quote(str(direccion))
                    # Enlace optimizado para abrir la navegación GPS
                    link_maps = f"https://www.google.com/maps/dir/?api=1&destination={direccion_codificada}"
                    st.link_button("🗺️ NAVEGAR EN MAPS", link_maps)

    except Exception as e:
        st.error(f"⚠️ Ha ocurrido un error al procesar el archivo: {e}")

else:
    st.info("👆 Por favor, sube el archivo con la ruta de hoy para comenzar.")