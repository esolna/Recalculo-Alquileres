import streamlit as st

# =========================
# TÍTULO DE LA APP
# =========================
st.title("Recalculo de Alquileres")

st.write("Seleccione la institución")

# =========================
# SELECTOR DE INSTITUCIÓN
# =========================
instituciones = [
    "Seleccione...",
    "Institución A",
    "Institución B",
    "Institución C"
]

institucion_seleccionada = st.selectbox(
    "Institución",
    instituciones
)

# =========================
# MOSTRAR SELECCIÓN (DEBUG)
# =========================
st.write("Institución seleccionada:", institucion_seleccionada)
