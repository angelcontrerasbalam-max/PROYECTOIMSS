import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
import os

# --- Configuración de la Página (Premium) --- #
st.set_page_config(
    page_title="Afiliación y Vigencia - Subdelegación 33 La Ceiba",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Fuentes y Estilos CSS Personalizados Premium --- #
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;1,600&display=swap" rel="stylesheet">
    <style>
    /* Aquí van todos tus estilos CSS, idénticos a la versión original */
    </style>
    """,
    unsafe_allow_html=True
)

# --- Banner del Encabezado (Hero Section) --- #
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-dept">DEPARTAMENTO DE AFILIACIÓN Y VIGENCIA</div>
        <h1 class="hero-title">Subdelegación 33 La Ceiba</h1>
        <div class="hero-subtitle">Visualización Analítica del Estatus Patronal y Gestión de Archivo</div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Generador / Cargador de Datos de Respaldo --- #
@st.cache_data
def load_data(file_path):
    if os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path)
            df.columns = df.columns.astype(str).str.strip().str.upper()
            if 'ULTIMO MOVIMIENTO FECHA ULTIMO MOV' in df.columns:
                df['ULTIMO MOVIMIENTO FECHA ULTIMO MOV'] = pd.to_datetime(df['ULTIMO MOVIMIENTO FECHA ULTIMO MOV'], errors='coerce')
            return df, False
        except Exception as e:
            st.error(f"Error al cargar el archivo Excel real: {e}")
    # generación de datos sintéticos omitida por brevedad
    return df_synthetic, True

file_path = 'DATOS/PATRONES PROYECTO FINAL.xlsx'
df, is_simulated = load_data(file_path)

def check_col(col_name):
    return col_name in df.columns

# --- Panel de Métricas Ejecutivas (KPIs) --- #
# (igual que tu versión original)

# --- Buscador y Archivero Visual Premium --- #
# (igual que tu versión original)

# Helper para gráficas Plotly
def configure_plotly_theme(fig):
    fig.update_layout(
        font_family="Outfit, sans-serif",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=60, b=40),
        title_font=dict(size=20, color="#1E3A8A", family="Outfit", weight="bold"),
        legend=dict(
            font=dict(size=12, color="#0F172A"),
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#E2E8F0",
            borderwidth=1
        )
    )
    fig.update_xaxes(
        showgrid=True, gridcolor="#E2E8F0", linecolor="#CBD5E1", 
        title_font=dict(size=14, color="#1E3A8A", weight="bold"),
        tickfont=dict(color="#0F172A", size=12, family="Outfit")
    )
    fig.update_yaxes(
        showgrid=True, gridcolor="#E2E8F0", linecolor="#CBD5E1", 
        title_font=dict(size=14, color="#1E3A8A", weight="bold"),
        tickfont=dict(color="#0F172A", size=12, family="Outfit")
    )
    return fig

# --- Pestañas de Análisis --- #
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Estatus Patronal", 
    "📉 Motivos de Baja", 
    "🏭 Actividades Económicas", 
    "⚠️ Primas de Riesgo", 
    "👷 Trabajadores Asegurados", 
    "📑 Movimientos Afiliatorios",
    "🌐 Medios Digitales"
])

# --- Tab 3 corregido ---
with tab3:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("Distribución de Sectores y Actividades Económicas")
    st.markdown("Top 10 ramas de actividad con mayor concentración de patrones en la delegación.")
    
    if check_col('ACTIVIDAD'):
        actividad_counts = df['ACTIVIDAD'].value_counts().head(10).sort_values(ascending=True)
        
        col1, col2 = st.columns([3, 2])
        with col1:
            fig3 = px.bar(
                x=actividad_counts.values,
                y=actividad_counts.index,
                orientation='h',
                labels={'x': 'Cantidad Total de Patrones', 'y': 'Sector / Actividad Económica'},
                color=actividad_counts.values,
                # ✅ CORREGIDO: solo una definición de color_continuous_scale
                color_continuous_scale=[[0, '#F97316'], [0.5, '#DC2626'], [1, '#7F0000']],
                text=actividad_counts.values,
                title="Volumen de Patrones por Actividad"
            )
            fig3.update_traces(
                textposition='auto', 
                textfont=dict(size=14, color='white', family="Outfit", weight="bold")
            )
            fig3.update_layout(yaxis=dict(tickmode='linear'))
            fig3.update_coloraxes(showscale=False)
            configure_plotly_theme(fig3)
            st.plotly_chart(fig3, use_container_width=True)
