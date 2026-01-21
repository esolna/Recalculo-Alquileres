import streamlit as st
import pandas as pd
from datetime import date

# =========================
# TÍTULO
# =========================
st.title("Recalculo de Alquileres con IPC y Modificaciones")

# =========================
# DATOS SIMULADOS (estructura tipo SICOP)
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
# SELECTOR PROVEEDOR
# =========================
if institucion_sel != "Seleccione...":
    df_inst = df[df["institucion"] == institucion_sel]
    proveedores = ["Seleccione..."] + sorted(df_inst["proveedor"].unique().tolist())
    proveedor_sel = st.selectbox("Proveedor", proveedores)
else:
    proveedor_sel = None

# =========================
# FECHA DE CORTE
# =========================
fecha_corte = st.date_input("Fecha de corte", value=date.today())

# =========================
# MODIFICACIÓN AL CONTRATO
# =========================
modificacion = st.number_input(
    "Modificación al contrato (₡)",
    value=0.0,
    step=1000.0
)

# =========================
# IPC ANUAL
# =========================
ipc_anual = st.number_input(
    "IPC Anual (%)",
    min_value=-100.0,
    max_value=100.0,
    value=0.0,
    step=0.01
) / 100

# =========================
# IPC MENSUAL
# =========================
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
        key=f"ipc_{mes}"
    )
    ipc_mensual.append(valor / 100)

# IPC acumulado compuesto
ipc_acumulado = 1
for ipc in ipc_mensual:
    ipc_acumulado *= (1 + ipc)

ipc_mensual_final = ipc_acumulado - 1

# =========================
# CÁLCULOS
# =========================
if proveedor_sel:
    fila = df[
        (df["institucion"] == institucion_sel) &
        (df["proveedor"] == proveedor_sel)
    ]

    if not fila.empty:
        precio_base = fila.iloc[0]["precio_unitario_contratado"]

        precio_anual = precio_base * (1 + ipc_anual) + modificacion
        precio_mensual = precio_base * (1 + ipc_mensual_final) + modificacion

        st.markdown("---")
        st.subheader("Resultados Comparativos")

        resultados = pd.DataFrame({
            "Escenario": ["IPC Anual", "IPC Mensual Acumulado"],
            "IPC Aplicado (%)": [
                ipc_anual * 100,
                ipc_mensual_final * 100
            ],
            "Precio Recalculado (₡)": [
                precio_anual,
                precio_mensual
            ]
        })

        st.dataframe(resultados.style.format({
            "IPC Aplicado (%)": "{:.2f}",
            "Precio Recalculado (₡)": "₡ {:,.0f}"
        }))
