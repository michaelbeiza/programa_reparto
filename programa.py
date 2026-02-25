import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Rutas de Reparto", page_icon="🚚", layout="centered")

st.title("🚚 Ruta del Día")

# --- INICIALIZAR MEMORIA ---
# Esto guarda qué clientes ya están entregados para que no se borre al recargar
if 'entregados' not in st.session_state:
    st.session_state.entregados = {}

# Botón de subida
archivo_subido = st.file_uploader("Sube el archivo de la ruta de hoy", type=["xlsx", "xls", "csv"])

if archivo_subido is not None:
    try:
        # 1. Leer archivo de ruta
        if archivo_subido.name.endswith('.xlsx'):
            df_ruta = pd.read_excel(archivo_subido, engine='openpyxl')
        elif archivo_subido.name.endswith('.xls'):
            df_ruta = pd.read_excel(archivo_subido, engine='xlrd')
        else:
            # Intentamos leer el CSV en UTF-8 (para evitar problemas de tildes)
            try:
                df_ruta = pd.read_csv(archivo_subido, encoding="utf-8", sep=",", engine="python")
            except UnicodeDecodeError:
                df_ruta = pd.read_csv(archivo_subido, encoding="latin1", sep=",", engine="python")

        # Leer archivo de clientes (Solución para las tildes)
        try:
            df_clientes = pd.read_csv("clientes.csv", encoding="utf-8", sep=",")
        except UnicodeDecodeError:
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
        st.write("---")

        # 4. Mostrar la lista 
        for index, fila in df_completo.iterrows():
            cliente = fila.get('Cliente', 'Desconocido')
            direccion = fila.get('DireccionCl', 'Dirección no encontrada')
            
            # Crear un identificador único para este envío en la memoria
            id_envio = f"{index}_{cliente}"
            
            # Si es la primera vez que vemos este envío, lo marcamos como NO entregado
            if id_envio not in st.session_state.entregados:
                st.session_state.entregados[id_envio] = False

            with st.container():
                st.subheader(f"👤 {cliente}")
                
                if pd.isna(direccion) or str(direccion).strip() == 'Dirección no encontrada':
                    st.warning("⚠️ Dirección no encontrada en clientes.csv")
                else:
                    st.write(f"📍 {direccion}")
                    
                    # Preparamos la dirección para las URLs
                    direccion_codificada = urllib.parse.quote(str(direccion))
                    link_gmaps = f"https://www.google.com/maps/dir/?api=1&destination={direccion_codificada}"
                    link_waze = f"https://waze.com/ul?q={direccion_codificada}&navigate=yes"
                    
                    # Dividimos en columnas (Las dos primeras para mapas, la última grande para Entregado)
                    col1, col2, col3 = st.columns([1, 1, 2])
                    
                    with col1:
                        st.link_button("🗺️ MAPS", link_gmaps, use_container_width=True)
                        
                    with col2:
                        st.link_button("🚙 WAZE", link_waze, use_container_width=True)
                    
                    with col3:
                        # Leemos el estado actual de la memoria
                        esta_entregado = st.session_state.entregados[id_envio]
                        
                        # Cambiamos el texto y el diseño según el estado
                        texto_boton = "🟩 ENTREGADO" if esta_entregado else "⬜ POR ENTREGAR"
                        tipo_boton = "primary" if esta_entregado else "secondary"
                        
                        # Botón que cambia de estado al pulsarlo
                        if st.button(texto_boton, key=f"btn_{id_envio}", type=tipo_boton, use_container_width=True):
                            # Al pulsar, invertimos el estado (de False a True, o de True a False)
                            st.session_state.entregados[id_envio] = not esta_entregado
                            # Recargamos la interfaz para mostrar el cambio
                            st.rerun()
                
                st.write("---") # Línea separadora visual

    except Exception as e:
        st.error(f"⚠️ Error al procesar: {e}")
else:
    st.info("👆 Sube el archivo Excel o CSV para empezar.")