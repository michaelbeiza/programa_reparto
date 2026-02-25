import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Rutas de Reparto", page_icon="🚚", layout="centered")

# --- ESTILOS PERSONALIZADOS (Para que el botón se ponga VERDE) ---
st.markdown("""
    <style>
    /* Forzar que el botón 'primary' sea verde */
    div.stButton > button[kind="primary"] {
        background-color: #28a745 !important;
        color: white !important;
        border-color: #28a745 !important;
    }
    /* Color al pasar el ratón por encima */
    div.stButton > button[kind="primary"]:hover {
        background-color: #218838 !important;
        border-color: #1e7e34 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚚 Ruta del Día")

# --- INICIALIZAR MEMORIA ---
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
            try:
                df_ruta = pd.read_csv(archivo_subido, encoding="utf-8", sep=",", engine="python")
            except UnicodeDecodeError:
                df_ruta = pd.read_csv(archivo_subido, encoding="latin1", sep=",", engine="python")

        # Leer archivo de clientes
        try:
            df_clientes = pd.read_csv("clientes.csv", encoding="utf-8", sep=",")
        except UnicodeDecodeError:
            df_clientes = pd.read_csv("clientes.csv", encoding="latin1", sep=",")

        # 2. Limpieza básica
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
            
            id_envio = f"{index}_{cliente}"
            
            if id_envio not in st.session_state.entregados:
                st.session_state.entregados[id_envio] = False

            with st.container():
                st.subheader(f"👤 {cliente}")
                
                if pd.isna(direccion) or str(direccion).strip() == 'Dirección no encontrada':
                    st.warning("⚠️ Dirección no encontrada en clientes.csv")
                else:
                    st.write(f"📍 {direccion}")
                    
                    direccion_codificada = urllib.parse.quote(str(direccion))
                    link_gmaps = f"https://www.google.com/maps/dir/?api=1&destination={direccion_codificada}"
                    link_waze = f"https://waze.com/ul?q={direccion_codificada}&navigate=yes"
                    
                    col1, col2, col3 = st.columns([1, 1, 2])
                    
                    with col1:
                        st.link_button("🗺️ MAPS", link_gmaps, use_container_width=True)
                        
                    with col2:
                        st.link_button("🚙 WAZE", link_waze, use_container_width=True)
                    
                    with col3:
                        esta_entregado = st.session_state.entregados[id_envio]
                        
                        texto_boton = "🟩 ENTREGADO" if esta_entregado else "⬜ POR ENTREGAR"
                        tipo_boton = "primary" if esta_entregado else "secondary"
                        
                        if st.button(texto_boton, key=f"btn_{id_envio}", type=tipo_boton, use_container_width=True):
                            st.session_state.entregados[id_envio] = not esta_entregado
                            st.rerun()
                
                st.write("---")

    except Exception as e:
        st.error(f"⚠️ Error al procesar: {e}")
else:
    st.info("👆 Sube el archivo Excel o CSV para empezar.")