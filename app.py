import streamlit as st
import pandas as pd
from datetime import date

# =========================
# TÍTULO
# =========================
st.title("Recalculo de Alquileres con IPC")

# =========================
# DATOS SIMULADOS (estructura tipo SICOP / KNIME)
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
fecha_corte = st.date_input("Fecha de corte", value=date.today())

# =========================
# TIPO DE IPC
# =========================
tipo_ipc = st.radio(
    "Tipo de IPC a aplicar",
    ["IPC Anual", "IPC Mensual (acumulado)"]
)

# =========================
# IPC ANUAL
# =========================
ipc_final = None

if tipo_ipc == "IPC Anual":
    ipc_anual = st.number_input(
        "IPC Anual (%)",
        min_value=-100.0,
        max_value=100.0,
        value=0.0,
        step=0.01
    )
    ipc_final = ipc_anual / 100

# =========================
# IPC MENSUAL
# =========================
if tipo_ipc == "IPC Mensual (acumulado)":
    st.markdown("### IPC Mensual (%)")

    meses = [
        "Enero", "Febrero", "Marzo", "Abril",
        "Mayo", "Junio", "Julio", "Agosto",
        "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    ipc_mensual = []

    for mes in meses:
        valor = st.number_input(
            f"{mes}",
            min_value=-100.0,
            max_value=100.0,
            value=0.0,
            step=0.01,
            key=mes
        )
        ipc_mensual.append(valor / 100)

    # IPC acumulado compuesto
    ipc_acumulado = 1
    for ipc in ipc_mensual:
        ipc_acumulado *= (1 + ipc)

    ipc_final = ipc_acumulado - 1

    st.success(f"IPC acumulado aplicado: {ipc_final * 100:.2f} %")

# =========================
# CÁLCULO FINAL
# =========================
if proveedor_sel and ipc_final is not None:
    fila = df[
        (df["institucion"] == institucion_sel) &
        (df["proveedor"] == proveedor_sel)
    ]

    if not fila.empty:
        precio_original = fila.iloc[0]["precio_unitario_contratado"]
        precio_recalculado = precio_original * (1 + ipc_final)

        st.markdown("---")
        st.subheader("Resultado del Recalculo")

        st.write("Precio original:", f"₡ {precio_original:,.0f}")
        st.write("IPC aplicado:", f"{ipc_final * 100:.2f} %")
        st.write("Precio recalculado:", f"₡ {precio_recalculado:,.0f}")

