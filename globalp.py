import streamlit as st
import webbrowser

# --- ESTÉTICA AQUA LAPRIDA ---
st.set_page_config(page_title="GPC Calc", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #001b3a; }
    h1 { color: #00ffcc; text-align: center; }
    .stTextInput>div>div>input { background-color: #00ffcc !important; color: #001b3a !important; font-weight: bold; }
    .stNumberInput>div>div>input { background-color: #00ffcc !important; color: #001b3a !important; font-weight: bold; }
    div.stButton > button { background-color: #00ffcc; color: #001b3a; width: 100%; font-weight: bold; border-radius: 10px; height: 3em; }
    label { color: #00ffcc !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE CÁLCULO ---
def calcular_argentina(precio_base, tipo_cambio, es_dolares):
    precio_usd = precio_base if es_dolares else precio_base / tipo_cambio
    precio_ars_puro = precio_base * tipo_cambio if es_dolares else precio_base
    
    imp_tarjeta = precio_usd * 0.30 * tipo_cambio
    excedente = max(0, precio_usd - 50.0)
    aduana_ars = excedente * 0.50 * tipo_cambio
    tasa_correo = 7500.0
    
    total = precio_ars_puro + imp_tarjeta + aduana_ars + tasa_correo
    return total, imp_tarjeta, aduana_ars, precio_ars_puro

# --- INTERFAZ ---
st.title("GLOBALP CALCULATOR")

# Estado para que el cálculo no se borre al tocar el tipo de cambio
if 'ejecutar_calculo' not in st.session_state:
    st.session_state.ejecutar_calculo = False

# 1. BLOQUE DE BÚSQUEDA
articulo = st.text_input("Ponga un Artículo para el cálculo", placeholder="Ej: Paazomu")

col_n1, col_n2 = st.columns(2)
with col_n1:
    node_ali = st.checkbox("Aliexpress", value=True)
with col_n2:
    node_temu = st.checkbox("Temu", value=False)

if st.button("BUSCAR EN NODOS"):
    if articulo:
        query = articulo.replace(" ", "+")
        if node_ali:
            webbrowser.open_new_tab(f"https://www.aliexpress.com/wholesale?SearchText={query}")
        if node_temu:
            webbrowser.open_new_tab(f"https://www.temu.com/search_result.html?search_key={query}")

st.markdown("---")

# 2. BLOQUE DE DATOS
col_moneda, col_tc = st.columns(2)
with col_moneda:
    moneda = st.radio("Moneda de entrada:", ["USD", "ARS"], horizontal=True, index=1)
with col_tc:
    # Corrección de la línea 63: paréntesis y comillas cerrados correctamente
    talle_cambio = st.number_input("Tipo de Cambio (ARS):", min_value=1.0, value=1840.0, step=1.0)

precio_input = st.number_input(f"Precio en {moneda}:", min_value=0.0, value=None, placeholder="0,00")

# 3. BOTÓN DE CALCULAR
if st.button("CALCULAR"):
    st.session_state.ejecutar_calculo = True

# Ejecución persistente (recalcula si cambias el TC sin cerrar la sesión)
if st.session_state.ejecutar_calculo:
    if precio_input is not None and precio_input > 0:
        total_val, imp_t, adu_a, base_a = calcular_argentina(precio_input, talle_cambio, moneda == "USD")
        
        st.markdown("### Desarrollo de Costos (ARG)")
        st.text_input("Costo Inicial (ARS):", value=f"$ {base_a:,.2f}", disabled=True)
        st.text_input("Impuestos (30%):", value=f"$ {imp_t:,.2f}", disabled=True)
        st.text_input("Aduana (50% exc):", value=f"$ {adu_a:,.2f}", disabled=True)
        st.text_input("Tasa Correo:", value="$ 7,500.00", disabled=True)
        
        st.success(f"TOTAL FINAL: $ {total_val:,.2f} ARS")
    else:
        st.warning("Ingrese el precio para realizar el cálculo.")
