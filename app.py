import streamlit as st
import pandas as pd

# =========================
# TÍTULO
# =========================
st.title("Recalculo de Alquileres")

# =========================
# DATOS SIMULADOS (estructura KNIME)
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
    "monto_alquiler": [
        1000,
        1500,
        2000,
        1800,
        2200
    ]
}

df = pd.DataFrame(data)

# =========================
# SELECTOR INSTITUCIÓN
# =========================
instituciones = ["Seleccione..."] + sorted(df["institucion"].unique().tolist())

institucion_sel = st.selectbox(
    "Institución",
    instituciones
)

st.write("Institución seleccionada:", institucion_sel)

# =========================
# SELECTOR PROVEEDOR (DEPENDIENTE)
# =========================
if institucion_sel != "Seleccione...":
    df_filtrado = df[df["institucion"] == institucion_sel]
    proveedores = ["Seleccione..."] + sorted(df_filtrado["proveedor"].unique().tolist())

    proveedor_sel = st.selectbox(
        "Proveedor",
        proveedores
    )

    st.write("Proveedor seleccionado:", proveedor_sel)
else:
    st.info("Seleccione una institución para habilitar proveedores")
