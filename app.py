import streamlit as st
import pandas as pd
from datetime import date

# =========================
# TÍTULO
# =========================
st.title("Recalculo de Alquileres por IPC")

# =========================
# DATOS BASE (Proveedor / Institución)
# =========================
data_contratos = {
    "institucion": [
        "Ministerio de Salud",
        "Ministerio de Educación",
        "Municipalidad Central"
    ],
    "proveedor": [
        "Proveedor A",
        "Proveedor B",
        "Proveedor C"
    ],
    "precio_base": [
        1530000,
        1800000,
        2200000
    ]
}

df_contratos = pd.DataFrame(data_contratos)

# =========================
# TABLA IPC 2025 (mensual)
# =========================
data_ipc = {
    "mes": [
        "2025-06", "2025-07", "2025-08",
        "2025-09", "2025-10", "2025-11", "2025-12"
    ],
    "ipc_mensual": [0.04, -0.52, -0.21, -0.40, 0.19, 0.47, 0.08],
    "ipc_interanual": [-0.22, -0.61, -0.94, -1.00, -0.38, -0.38, -1.23]
}

df_ipc = pd.DataFrame(data_ipc)

# =========================
# SELECTORES
# =========================
st.subheader("Selección del contrato")

institucion_sel = st.selectbox(
    "Institución",
    ["Seleccione..."] + df_contratos["institucion"].unique().tolist()
)

if institucion_sel != "Seleccione...":
    df_inst = df_contratos[df_contratos["institucion"] == institucion_sel]

    proveedor_sel = st.selectbox(
        "Proveedor",
        ["Seleccione..."] + df_inst["proveedor"].tolist()
    )
else:
    proveedor_sel = "Seleccione..."

fecha_inicio = st.date_input("Fecha inicio contrato", date(2025, 6, 26))
fecha_corte = st.date_input("Fecha corte", date(2025, 12, 31))

# =========================
# BOTÓN DE CÁLCULO
# =========================
if st.button("Calcular recálculo"):

    if institucion_sel == "Seleccione..." or proveedor_sel == "Seleccione...":
        st.error("Debe seleccionar institución y proveedor")
    else:
        # -------------------------
        # FILTRAR CONTRATO
        # -------------------------
        contrato = df_contratos[
            (df_contratos["institucion"] == institucion_sel) &
            (df_contratos["proveedor"] == proveedor_sel)
        ].iloc[0]

        precio_base = contrato["precio_base"]

        # -------------------------
        # CALCULO IPC MENSUAL
        # -------------------------
        df_ipc_calc = df_ipc.copy()

        df_ipc_calc["factor_mensual"] = 1 + (df_ipc_calc["ipc_mensual"] / 100)
        df_ipc_calc["factor_mensual_acumulado"] = df_ipc_calc["factor_mensual"].cumprod()
        df_ipc_calc["alquiler_ipc_mensual"] = precio_base * df_ipc_calc["factor_mensual_acumulado"]

        # -------------------------
        # CALCULO IPC ANUAL
        # -------------------------
        df_ipc_calc["factor_interanual"] = 1 + (df_ipc_calc["ipc_interanual"] / 100)
        df_ipc_calc["alquiler_ipc_interanual"] = precio_base * df_ipc_calc["factor_interanual"]

        # -------------------------
        # RESULTADOS
        # -------------------------
        st.success("Cálculo realizado correctamente")

        st.subheader("Detalle del cálculo")
        st.dataframe(
            df_ipc_calc[[
                "mes",
                "ipc_mensual",
                "alquiler_ipc_mensual",
                "ipc_interanual",
                "alquiler_ipc_interanual"
            ]]
        )

        st.subheader("Resumen final")
        st.metric(
            "Precio base",
            f"₡ {precio_base:,.0f}"
        )

        st.metric(
            "Alquiler con IPC mensual (dic-2025)",
            f"₡ {df_ipc_calc.iloc[-1]['alquiler_ipc_mensual']:,.0f}"
        )

        st.metric(
            "Alquiler con IPC interanual (dic-2025)",
            f"₡ {df_ipc_calc.iloc[-1]['alquiler_ipc_interanual']:,.0f}"
        )
