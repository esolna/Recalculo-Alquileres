import streamlit as st
import pandas as pd
from datetime import date

# =========================
# TÍTULO
# =========================
st.title("Recalculo de Alquileres")

# =========================
# DATOS SIMULADOS (estructura tipo KNIME)
# =========================
data = {
    "institucion": [
        "Ministerio de Salud",
        "Ministerio de Salud",
        "Ministerio de Educación",
        "Ministerio de Educación",
        "Municipalidad Central"
    ],
    "proveedor": [
        "Proveedor A",
        "Proveedor B",
        "Proveedor C",
        "Proveedor D",
        "Proveedor E"
    ],
    "precio_unitario_contratado": [
        1530000,
        1200000,
        2000000,
        1800000,
        2200000
    ]
}

df = pd.DataFrame(data)

# =========================
# SELECTOR INSTITUCIÓN
# =========================
instituciones = ["Seleccione..."] + sorted(df["institucion"].unique().tolist())
institucion_sel = st.selectbox("Institución", instituciones)

# =========================
# SELECTOR PROVEEDOR (DEPENDIENTE)
# =========================
if institucion_sel != "Seleccione...":
    df_inst = df[df["institucion"] == institucion_sel]
    proveedores = ["Seleccione..."] + sorted(df_inst["proveedor"].unique().tolist())
    proveedor_sel = st.selectbox("Proveedor", proveedores)
else:
    st.info("Seleccione una institución para habilitar proveedores")
    proveedor_sel = None

# =========================
# FECHA DE CORTE
# =========================
fecha_corte = st.date_input(
    "Fecha de corte",
    value=date.today()
)

# =========================
# TIPO DE IPC
# =========================
tipo_ipc = st.radio(
    "Tipo de IPC a aplicar",
    ["IPC Anual", "IPC Mensual (acumulado)"]
)

# =========================
# IPC ANUAL (solo si aplica)
# =========================
if tipo_ipc == "IPC Anual":
    ipc_anual = st.number_input(
        "IPC Anual (%)",
        min_value=-100.0,
        max_value=100.0,
        value=0.0,
        step=0.01
    )
else:
    ipc_anual = None

# =========================
# IPC MENSUAL (placeholder)
# =========================
if tipo_ipc == "IPC Mensual (acumulado)":
    st.info("En el siguiente paso se habilitará el ingreso de IPC mensual")

# =========================
# DEBUG VISUAL (TEMPORAL)
# =========================
st.markdown("---")
st.subheader("Valores seleccionados (debug)")

st.write("Institución:", institucion_sel)
st.write("Proveedor:", proveedor_sel)
st.write("Fecha de corte:", fecha_corte)
st.write("Tipo de IPC:", tipo_ipc)
st.write("IPC anual:", ipc_anual)
