import streamlit as st
import pandas as pd
from datetime import datetime

# Cargar CSV
df = pd.read_csv("datos_clima.csv")

# Limpiar columnas y convertir tipos
df["ciudad"] = df["ciudad"].astype(str).str.strip()
df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
df["lat"] = pd.to_numeric(df["latitud"].astype(str).str.replace("'", ""), errors="coerce")
df["lon"] = pd.to_numeric(df["longitud"].astype(str).str.replace("'", ""), errors="coerce")

# Eliminar filas con datos críticos faltantes
df = df.dropna(subset=["lat", "lon", "fecha", "ciudad"])

# Título
st.title("🌦️ Dashboard de Monitoreo Climático")

# Filtro por ciudad
ciudades = sorted(df["ciudad"].unique())
ciudad_sel = st.selectbox("Selecciona una ciudad", ciudades)

# Filtro por fecha
fecha_min = df["fecha"].min().date()
fecha_max = df["fecha"].max().date()
fecha_ini, fecha_fin = st.date_input("Selecciona el rango de fechas", [fecha_min, fecha_max])

# Filtrado de datos
df_ciudad = df[
    (df["ciudad"] == ciudad_sel) &
    (df["fecha"].dt.date >= fecha_ini) &
    (df["fecha"].dt.date <= fecha_fin)
].copy()


# Predicción simple basada en humedad y nubes
st.subheader("🔮 Predicción simple")
if not df_ciudad.empty:
    registro = df_ciudad.iloc[0]
    h = registro["humedad"]
    n = registro["nubes"]
    pred = "🌧️ Probable lluvia" if h > 80 or n > 80 else "☀️ No se espera lluvia"
    st.info(f"Último registro: {registro['descripcion']} — {pred}")
else:
    st.warning("No hay datos disponibles para esta ciudad y rango de fechas.")


# Tabla de registros recientes
st.subheader("📋 Registros recientes")
st.dataframe(df_ciudad[["fecha", "hora", "temperatura", "humedad", "descripcion", "lluvia_probable"]].sort_values("fecha", ascending=False).head(10))

# Ranking top 10 de ciudades más cálidas
st.subheader("🔥 Top 10 ciudades más cálidas (promedio)")
top10 = df.groupby("ciudad")["temperatura"].mean().sort_values(ascending=False).head(10)
st.dataframe(top10.reset_index().rename(columns={"temperatura": "Temperatura Promedio"}))

# Mapa al final
st.subheader("🗺️ Ubicación geográfica")
df_mapa = df_ciudad[["lat", "lon"]].dropna()
if not df_mapa.empty:
    st.map(df_mapa)
else:
    st.warning("No hay coordenadas disponibles para mostrar en el mapa.")
