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
    html, body, .stApp {
        font-family: 'Outfit', sans-serif !important;
        background-color: #F8FAFC !important;
    }
    .hero-container {
        background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%);
        padding: 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.3);
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .hero-container::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 60%);
        pointer-events: none;
    }
    .hero-dept {
        font-size: 1.1em;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-weight: 500;
        color: #93C5FD;
        margin-bottom: 8px;
    }
    .hero-title {
        font-size: 2.6em;
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
        background: linear-gradient(to right, #FFFFFF, #E0F2FE);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1.2em;
        font-weight: 300;
        color: #CBD5E1;
        margin-top: 10px;
    }
    h2, h3, h4 {
        color: #1E3A8A !important;
        font-weight: 700 !important;
        font-family: 'Outfit', sans-serif !important;
    }
    .premium-card {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 20px;
    }
    .premium-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 20px -8px rgba(0, 0, 0, 0.1), 0 4px 12px -2px rgba(0, 0, 0, 0.05);
        border-color: #3B82F6;
    }
    .kpi-wrapper {
        display: flex;
        gap: 20px;
        margin-bottom: 30px;
        flex-wrap: wrap;
    }
    .kpi-card {
        flex: 1;
        min-width: 220px;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
        display: flex;
        align-items: center;
        gap: 15px;
        transition: all 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: #3B82F6;
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.1);
    }
    .kpi-icon-container {
        width: 50px;
        height: 50px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5em;
    }
    .kpi-blue { background-color: #EFF6FF; color: #1D4ED8; }
    .kpi-green { background-color: #ECFDF5; color: #047857; }
    .kpi-purple { background-color: #F5F3FF; color: #6D28D9; }
    .kpi-orange { background-color: #FFF7ED; color: #C2410C; }
    .kpi-info {
        display: flex;
        flex-direction: column;
    }
    .kpi-num {
        font-size: 1.8em;
        font-weight: 800;
        color: #0F172A;
        line-height: 1;
    }
    .kpi-lbl {
        font-size: 0.85em;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 5px;
    }
    .dark-panel {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        border: none !important;
        color: #F8FAFC !important;
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #3B82F6 !important;
    }
    .dark-panel h4 {
        color: #60A5FA !important;
        margin-top: 0;
        font-size: 1.25em;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .dark-panel p, .dark-panel li {
        color: #E2E8F0 !important;
        font-size: 0.95em;
        line-height: 1.6;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F1F5F9;
        padding: 6px;
        border-radius: 12px;
        border-bottom: none;
    }
    .stTabs [data-baseweb="tab-list"] button {
        background-color: transparent;
        color: #64748B !important;
        font-weight: 600 !important;
        font-size: 0.95em !important;
        padding: 10px 18px !important;
        border-radius: 8px !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [data-baseweb="tab-list"] button:hover {
        background-color: #E2E8F0 !important;
        color: #1E3A8A !important;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #1E3A8A !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05) !important;
    }
    .archive-room {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        justify-content: center;
        margin: 25px 0;
    }
    .cabinet-box {
        border-radius: 12px;
        background: #F8FAFC;
        border: 2px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        padding: 15px;
        width: 175px;
        transition: all 0.4s ease;
        position: relative;
    }
    .cabinet-box.active {
        background: #FFFFFF;
    }
    .cabinet-title {
        text-align: center;
        font-weight: 700;
        margin-top: 0;
        margin-bottom: 12px;
        font-size: 1.05em;
        color: #1E3A8A;
    }
    .drawer-grid {
        display: grid;
        grid-template-columns: repeat(8, 1fr);
        gap: 3px;
    }
    .drawer-header-cell {
        font-size: 0.7em;
        font-weight: 700;
        color: #64748B;
        text-align: center;
        padding-bottom: 3px;
    }
    .drawer-row-num {
        font-size: 0.7em;
        font-weight: 700;
        color: #64748B;
        align-self: center;
        text-align: center;
    }
    .drawer-cell {
        aspect-ratio: 1;
        border: 1px solid #CBD5E1;
        background: #E2E8F0;
        border-radius: 3px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8em;
        color: transparent;
        transition: all 0.2s ease;
        position: relative;
    }
    .drawer-cell:hover {
        background: #94A3B8;
        border-color: #64748B;
        cursor: pointer;
    }
    .drawer-cell.active-drawer {
        background: #10B981 !important;
        border-color: #059669 !important;
        color: #FFFFFF !important;
        animation: pulse-glow 2s infinite alternate;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.8);
    }
    @keyframes pulse-glow {
        0% { transform: scale(1); box-shadow: 0 0 5px rgba(16, 185, 129, 0.5); }
        100% { transform: scale(1.1); box-shadow: 0 0 15px rgba(16, 185, 129, 0.9); }
    }
    .floating-action-btn {
        position: fixed;
        bottom: 25px;
        right: 25px;
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: #FFFFFF !important;
        border-radius: 30px;
        padding: 12px 24px;
        font-size: 0.95em;
        font-weight: 600;
        text-decoration: none;
        box-shadow: 0 8px 16px -4px rgba(30, 58, 138, 0.4);
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 2px solid rgba(255, 255, 255, 0.25);
    }
    .floating-action-btn:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 20px -4px rgba(30, 58, 138, 0.5);
        border-color: rgba(255, 255, 255, 0.6);
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
    }
    .simulated-banner {
        background: #FFFBEB;
        border-left: 5px solid #F59E0B;
        color: #B45309;
        padding: 12px 20px;
        border-radius: 8px;
        margin-bottom: 25px;
        font-size: 0.9em;
        display: flex;
        align-items: center;
        gap: 10px;
    }
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
            
    import numpy as np
    np.random.seed(42)
    n_rows = 380
    
    reg_pat = [f"Y{np.random.randint(10,99)}-{np.random.randint(10000,99999)}-{np.random.randint(10,99)}" for _ in range(n_rows)]
    
    secciones = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    ubicaciones = []
    for _ in range(n_rows):
        c = np.random.randint(1, 6)
        f = np.random.randint(1, 8)
        s = np.random.choice(secciones)
        ubicaciones.append(f"ARCHIVERO {c} FILA {f} SECCIÓN {s}")
        
    estatus_choices = ['ACTIVO', 'BAJA', 'SUSPENDIDO']
    estatus_probs = [0.884, 0.100, 0.016]
    estatus = np.random.choice(estatus_choices, size=n_rows, p=estatus_probs)
    
    motivos_baja = []
    for est in estatus:
        if est == 'BAJA':
            motivos_baja.append(np.random.choice([
                "Falta de localización del domicilio",
                "Impago prolongado de cuotas",
                "Cierre definitivo de empresa",
                "Fusión o sustitución patronal"
            ]))
        else:
            motivos_baja.append(None)
            
    actividades = np.random.choice([
        "SERVICIOS DE RESTAURANTES Y HOTELES",
        "CONSTRUCCIÓN DE VIVIENDA Y EDIFICACIONES",
        "COMERCIO AL POR MENOR",
        "CONSULTORÍA PROFESIONAL Y LEGAL",
        "FABRICACIÓN DE ALIMENTOS Y BEBIDAS",
        "INVESTIGACIÓN Y DESARROLLO CIENTÍFICO",
        "AGRICULTURA Y CITRICULTURA"
    ], size=n_rows, p=[0.30, 0.22, 0.18, 0.12, 0.08, 0.05, 0.05])
    
    prima_ant = np.round(np.random.uniform(0.5, 7.5, size=n_rows), 5)
    change = np.random.choice([-0.4, 0.0, 0.4, 0.8, -0.6], size=n_rows, p=[0.25, 0.4, 0.2, 0.08, 0.07])
    prima_act = np.clip(np.round(prima_ant + change + np.random.normal(0, 0.05, size=n_rows), 5), 0.5, 7.585)
    
    trabajadores = np.random.randint(2, 450, size=n_rows)
    for i in range(n_rows):
        if "CONSTRUCCIÓN" in actividades[i]:
            trabajadores[i] = np.random.randint(40, 580)
        elif "SERVICIOS" in actividades[i]:
            trabajadores[i] = np.random.randint(8, 250)
            
    tipo_mov = np.random.choice(['1', '2', '3', '4'], size=n_rows, p=[0.45, 0.25, 0.15, 0.15])
    
    start_date = pd.to_datetime('2018-01-01')
    end_date = pd.to_datetime('2026-05-01')
    dates = pd.to_datetime(np.random.randint(start_date.value, end_date.value, size=n_rows))
    
    medios = np.random.choice(['INTERNET', 'VENTANILLA'], size=n_rows, p=[0.74, 0.26])
    
    df_synthetic = pd.DataFrame({
        'REGISTRO PATRONAL': reg_pat,
        'UBICACIÓN DE ARCHIVO': ubicaciones,
        'ESTATUS': estatus,
        'MOTIVO BAJA': motivos_baja,
        'ACTIVIDAD': actividades,
        'PRIMA DE RIESGO ACTUAL': prima_act,
        'PRIMA DE RIESGO ANTERIOR': prima_ant,
        'TRABAJADORES': trabajadores,
        'TIPO DE MOVIMIENTO': tipo_mov,
        'ULTIMO MOVIMIENTO FECHA ULTIMO MOV': dates,
        'MEDIO': medios
    })
    
    return df_synthetic, True
file_path = 'DATOS/PATRONES PROYECTO FINAL.xlsx'
df, is_simulated = load_data(file_path)
if is_simulated:
    st.markdown(
        """
        <div class="simulated-banner">
            <span>💡</span>
            <span><b>Modo Demostración Activo:</b> No se detectó el archivo en <code>DATOS/PATRONES PROYECTO FINAL.xlsx</code>.
            Se ha inicializado una base de datos sintética de alta calidad con 380 registros simulados para evaluar la interfaz.</span>
        </div>
        """,
        unsafe_allow_html=True
    )
def check_col(col_name):
    return col_name in df.columns
# --- Panel de Métricas Ejecutivas (KPIs) --- #
total_patrones = len(df)
activos_pct = (df['ESTATUS'] == 'ACTIVO').mean() * 100 if check_col('ESTATUS') else 0
total_empleados = int(df['TRABAJADORES'].sum()) if check_col('TRABAJADORES') else 0
digital_pct = (df['MEDIO'] == 'INTERNET').mean() * 100 if check_col('MEDIO') else 0
st.markdown(
    f"""
    <div class="kpi-wrapper">
        <div class="kpi-card">
            <div class="kpi-icon-container kpi-blue">🏢</div>
            <div class="kpi-info">
                <span class="kpi-num">{total_patrones}</span>
                <span class="kpi-lbl">Total Patrones</span>
            </div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon-container kpi-green">📈</div>
            <div class="kpi-info">
                <span class="kpi-num">{activos_pct:.1f}%</span>
                <span class="kpi-lbl">Tasa de Actividad</span>
            </div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon-container kpi-purple">👷</div>
            <div class="kpi-info">
                <span class="kpi-num">{total_empleados:,}</span>
                <span class="kpi-lbl">Empleados Totales</span>
            </div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon-container kpi-orange">💻</div>
            <div class="kpi-info">
                <span class="kpi-num">{digital_pct:.1f}%</span>
                <span class="kpi-lbl">Trámite Vía Web</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
# --- Buscador y Archivero Visual Premium --- #
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.subheader('🔍 Búsqueda Inteligente de Registro Patronal')
st.markdown("Busca el expediente físico en los archiveros institucionales de la subdelegación ingresando el código de registro.")
registro_patronal_input = st.text_input('Ingresa el Registro Patronal para ubicar:', '', placeholder="Ej. Y12-34567-89")
if registro_patronal_input:
    if check_col('REGISTRO PATRONAL'):
        filtered_patron = df[df['REGISTRO PATRONAL'].astype(str).str.contains(registro_patronal_input, case=False, na=False)]
        
        if not filtered_patron.empty:
            st.markdown("#### Datos del Patrón Encontrado:")
            st.dataframe(filtered_patron.reset_index(drop=True), use_container_width=True)
            
            if check_col('UBICACIÓN DE ARCHIVO'):
                location_str = str(filtered_patron['UBICACIÓN DE ARCHIVO'].iloc[0])
                
                def parse_location(location_string):
                    cabinet_match = re.search(r'A[R]?CHIVERO\s*(\d+)', location_string, re.IGNORECASE)
                    fila_match = re.search(r'FILA\s*(\d+)', location_string, re.IGNORECASE)
                    seccion_match = re.search(r'SECCI[OÓ]?N\s*([A-G])', location_string, re.IGNORECASE)
                    
                    cabinet = int(cabinet_match.group(1)) if cabinet_match else None
                    fila = int(fila_match.group(1)) if fila_match else None
                    seccion = seccion_match.group(1).upper() if seccion_match else None
                    return cabinet, fila, seccion
                    
                cabinet, fila, seccion = parse_location(location_str)
                
                if cabinet and fila and seccion:
                    st.success(f"📂 El expediente físico está localizado en el **Archivero {cabinet}, Fila {fila}, Sección {seccion}**.")
                    st.markdown("#### Ubicación en Sala de Archivo:")
                    
                    html_archivero = "<div class='archive-room'>"
                    for c in range(1, 6):
                        is_active = (c == cabinet)
                        active_class = "active" if is_active else ""
                        
                        html_archivero += f"""
                        <div class="cabinet-box {active_class}">
                            <div class="cabinet-title">Archivero {c}</div>
                            <div class="drawer-grid">
                        """
                        html_archivero += "<div class='drawer-header-cell'></div>"
                        for s_char in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
                            html_archivero += f"<div class='drawer-header-cell'>{s_char}</div>"
                            
                        for r in range(1, 8):
                            html_archivero += f"<div class='drawer-row-num'>{r}</div>"
                            for s_char in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
                                if is_active and r == fila and s_char == seccion:
                                    bg_style = "active-drawer"
                                    text = "📂"
                                else:
                                    bg_style = ""
                                    text = "&nbsp;"
                                    
                                tooltip = f"Archivero {c}, Fila {r}, Sección {s_char}"
                                html_archivero += f'<div class="drawer-cell {bg_style}" title="{tooltip}">{text}</div>'
                                
                        html_archivero += "</div></div>"
                    html_archivero += "</div>"
                    st.markdown(html_archivero, unsafe_allow_html=True)
                else:
                    st.warning(f"La ubicación '{location_str}' no coincide con el formato esperado.")
            else:
                st.info("Columna 'UBICACIÓN DE ARCHIVO' no disponible en el conjunto de datos.")
        else:
            st.warning('No se encontraron registros que coincidan con ese Registro Patronal.')
    else:
        st.error("No se encontró la columna 'REGISTRO PATRONAL' en el conjunto de datos.")
st.markdown('</div>', unsafe_allow_html=True)
# Helper MEJORADO para legibilidad de gráficas Plotly
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
    # Se añade tickfont explícito con color oscuro (#0F172A) para que las leyendas sean legibles
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
# --- Pestañas de Análisis e Información Ejecutiva --- #
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Estatus Patronal", 
    "📉 Motivos de Baja", 
    "🏭 Actividades Económicas", 
    "⚠️ Primas de Riesgo", 
    "👷 Trabajadores Asegurados", 
    "📑 Movimientos Afiliatorios",
    "🌐 Medios Digitales"
])
with tab1:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("Estatus Patronal - Sección Norte")
    st.markdown("Distribución global de los registros patronales vigentes vs. suspendidos y dados de baja.")
    
    if check_col('ESTATUS'):
        estatus_counts = df['ESTATUS'].value_counts()
        
        col1, col2 = st.columns([3, 2])
        with col1:
            fig1 = px.pie(
                values=estatus_counts.values,
                names=estatus_counts.index,
                hole=0.6,
                color_discrete_sequence=['#10B981', '#F43F5E', '#F59E0B']
            )
            fig1.update_traces(
                textposition='inside',
                textinfo='percent+label',
                marker=dict(line=dict(color='#FFFFFF', width=2)),
                insidetextfont=dict(size=14, color='white')
            )
            configure_plotly_theme(fig1)
            st.plotly_chart(fig1, use_container_width=True)
            
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                """
                <div class="dark-panel">
                    <h4>Análisis de Estatus Regional</h4>
                    <p>El porcentaje mayoritario de patrones en estatus <b>ACTIVO</b> consolida la presencia productiva en el área norte de Mérida, impulsada principalmente por servicios y nuevos desarrollos habitacionales.</p>
                    <p>La tasa residual de <b>BAJAS</b> (aprox. 10-12%) se alinea con la fluctuación natural de pequeñas unidades comerciales. Es vital mantener una supervisión constante para agilizar los trámites de reanudación y evitar la informalidad laboral.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.error("Columna 'ESTATUS' no encontrada en la base de datos.")
    st.markdown('</div>', unsafe_allow_html=True)
with tab2:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("Principales Motivos de Baja Patronal")
    st.markdown("Clasificación de expedientes inactivos según causas administrativas y legales.")
    
    if check_col('ESTATUS') and check_col('MOTIVO BAJA'):
        bajas_df = df[df['ESTATUS'] == 'BAJA']
        
        if not bajas_df.empty and bajas_df['MOTIVO BAJA'].notna().sum() > 0:
            baja_motivos = bajas_df['MOTIVO BAJA'].value_counts()
            
            col1, col2 = st.columns([3, 2])
            with col1:
                fig2 = px.pie(
                    values=baja_motivos.values,
                    names=baja_motivos.index,
                    hole=0.6,
                    color_discrete_sequence=px.colors.qualitative.Safe
                )
                fig2.update_traces(
                    textposition='inside',
                    textinfo='percent',
                    marker=dict(line=dict(color='#FFFFFF', width=2))
                )
                configure_plotly_theme(fig2)
                st.plotly_chart(fig2, use_container_width=True)
                
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(
                    """
                    <div class="dark-panel">
                        <h4>Fundamentos del IMSS en Bajas</h4>
                        <p>De acuerdo con la <b>Ley del Seguro Social (LSS)</b>, las bajas de registros patronales pueden ser voluntarias (solicitud del patrón por cese de actividades) o dictadas por el Instituto bajo los siguientes supuestos:</p>
                        <ul>
                            <li><b>No localización:</b> Imposibilidad de verificar físicamente el domicilio fiscal reportado.</li>
                            <li><b>Ausencia de trabajadores:</b> Falta de transmisión de movimientos de alta por periodos prolongados.</li>
                            <li><b>Omisión de cuotas:</b> Incumplimiento persistente que vulnera la estabilidad financiera del seguro.</li>
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No se registran patrones dados de baja o con motivos especificados en esta muestra de datos.")
    else:
        st.error("Columnas 'ESTATUS' o 'MOTIVO BAJA' faltantes.")
    st.markdown('</div>', unsafe_allow_html=True)
with tab3:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("Distribución de Sectores y Actividades Económicas")
    st.markdown("Top 10 ramas de actividad con mayor concentración de patrones en la delegación.")
    
    if check_col('ACTIVIDAD'):
        actividad_counts = df['ACTIVIDAD'].value_counts().head(10).sort_values(ascending=True)
        
        col1, col2 = st.columns([3, 2])
        with col1:
            # CORRECCIÓN: Título claro, etiquetas en los ejes y números dentro de la barra
            fig3 = px.bar(
                x=actividad_counts.values,
                y=actividad_counts.index,
                orientation='h',
                labels={'x': 'Cantidad Total de Patrones', 'y': 'Sector / Actividad Económica'},
                color=actividad_counts.values,
                color_continuous_scale=px.colors.sequential.Plotly3_r,
                text=actividad_counts.values, # Muestra el número dentro de la gráfica
                title="Volumen de Patrones por Actividad"
            )
            fig3.update_traces(
                textposition='auto', 
                textfont=dict(size=14, color='white', family="Outfit", weight="bold")
            )
            fig3.update_layout(yaxis=dict(tickmode='linear')) # Asegura que todas las etiquetas Y se muestren
            fig3.update_coloraxes(showscale=False)
            configure_plotly_theme(fig3)
            st.plotly_chart(fig3, use_container_width=True)
            
        with col2:
            st.markdown(
                """
                <div class="dark-panel" style="margin-top: 20px;">
                    <h4>Estructura Económica Regional</h4>
                    <ul style="padding-left:15px; margin:0;">
                        <li style="margin-bottom:8px;">🛎️ <b>Servicios y Turismo:</b> Mérida se consolida como hub de servicios médicos, hoteleros y de enseñanza en el sureste.</li>
                        <li style="margin-bottom:8px;">🏗️ <b>Construcción:</b> Sector clave impulsado por la expansión urbana, proyectos residenciales de gama alta y la infraestructura federal.</li>
                        <li style="margin-bottom:8px;">🛒 <b>Comercio:</b> Flujo dinámico de abasto mayorista y retail concentrado en las plazas del norte de la ciudad.</li>
                        <li>💼 <b>Corporativos:</b> Firmas de consultoría, desarrollo de software y servicios legales especializados.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.error("Columna 'ACTIVIDAD' no encontrada.")
    st.markdown('</div>', unsafe_allow_html=True)
with tab4:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("Análisis de Primas de Riesgo de Trabajo")
    st.markdown("Monitoreo anual de las fluctuaciones en la clasificación de siniestralidad obrero-patronal.")
    
    if check_col('PRIMA DE RIESGO ACTUAL') and check_col('PRIMA DE RIESGO ANTERIOR') and check_col('REGISTRO PATRONAL'):
        df['PRIMA DE RIESGO ACTUAL'] = pd.to_numeric(df['PRIMA DE RIESGO ACTUAL'], errors='coerce').fillna(0)
        df['PRIMA DE RIESGO ANTERIOR'] = pd.to_numeric(df['PRIMA DE RIESGO ANTERIOR'], errors='coerce').fillna(0)
        df['CAMBIO PRIMA DE RIESGO'] = df['PRIMA DE RIESGO ACTUAL'] - df['PRIMA DE RIESGO ANTERIOR']
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### 📈 Top 5 Aumentos de Prima")
            top_inc = df.sort_values(by='CAMBIO PRIMA DE RIESGO', ascending=False).head(5)
            st.dataframe(
                top_inc[['REGISTRO PATRONAL', 'PRIMA DE RIESGO ANTERIOR', 'PRIMA DE RIESGO ACTUAL', 'CAMBIO PRIMA DE RIESGO']].reset_index(drop=True),
                use_container_width=True
            )
        with c2:
            st.markdown("##### 📉 Top 5 Reducciones de Prima")
            top_dec = df.sort_values(by='CAMBIO PRIMA DE RIESGO', ascending=True).head(5)
            st.dataframe(
                top_dec[['REGISTRO PATRONAL', 'PRIMA DE RIESGO ANTERIOR', 'PRIMA DE RIESGO ACTUAL', 'CAMBIO PRIMA DE RIESGO']].reset_index(drop=True),
                use_container_width=True
            )
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # CORRECCIÓN: Dispersión con Plotly más clara
        fig4 = px.scatter(
            df,
            x='PRIMA DE RIESGO ANTERIOR',
            y='PRIMA DE RIESGO ACTUAL',
            color='CAMBIO PRIMA DE RIESGO',
            size=df['CAMBIO PRIMA DE RIESGO'].abs().clip(0.1, 5),
            hover_data=['REGISTRO PATRONAL', 'ACTIVIDAD'],
            color_continuous_scale=px.colors.diverging.RdYlBu_r,
            labels={
                'CAMBIO PRIMA DE RIESGO': 'Aumento/Disminución (%)',
                'PRIMA DE RIESGO ANTERIOR': 'Prima Año Pasado (%)',
                'PRIMA DE RIESGO ACTUAL': 'Prima de Este Año (%)'
            },
            title="Comparativa de Primas de Riesgo (Anterior vs Actual)"
        )
        
        # Calcular límites dinámicos para los ejes para hacer zoom perfecto
        min_v = min(df['PRIMA DE RIESGO ANTERIOR'].min(), df['PRIMA DE RIESGO ACTUAL'].min())
        max_v = max(df['PRIMA DE RIESGO ANTERIOR'].max(), df['PRIMA DE RIESGO ACTUAL'].max())
        
        # Añadir un pequeño margen (10%) para que los puntos no queden pegados al borde
        margen = (max_v - min_v) * 0.1
        if margen == 0: margen = 0.1 # Por si todos los valores son idénticos
        lim_inf = max(0, min_v - margen) # Evitar bajar de 0 si las primas son positivas
        lim_sup = max_v + margen
        # Agregar línea de control dinámica visible en todo el nuevo rango de datos
        fig4.add_trace(
            go.Scatter(
                x=[lim_inf, lim_sup],
                y=[lim_inf, lim_sup],
                mode='lines',
                name='Misma Prima (Sin Siniestralidad)',
                line=dict(color='#475569', width=2, dash='dash')
            )
        )
        # Posicionar anotaciones textualmente basadas en las proporciones de la gráfica (20% y 80%)
        fig4.add_annotation(
            x=lim_inf + (lim_sup - lim_inf) * 0.2, 
            y=lim_sup - (lim_sup - lim_inf) * 0.15,
            text="<b>↑ Aumentó su Prima</b><br><span style='font-size:11px'>Mayor Siniestralidad</span>",
            showarrow=False,
            font=dict(color="#E11D48", size=14),
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#E11D48",
            borderwidth=1,
            borderpad=6
        )
        fig4.add_annotation(
            x=lim_sup - (lim_sup - lim_inf) * 0.2, 
            y=lim_inf + (lim_sup - lim_inf) * 0.15,
            text="<b>↓ Redujo su Prima</b><br><span style='font-size:11px'>Mejor Seguridad Integral</span>",
            showarrow=False,
            font=dict(color="#059669", size=14),
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#059669",
            borderwidth=1,
            borderpad=6
        )
        fig4.update_traces(marker=dict(line=dict(width=1, color='rgba(0,0,0,0.5)')), selector=dict(mode='markers'))
        fig4.update_layout(
            xaxis_range=[lim_inf, lim_sup], 
            yaxis_range=[lim_inf, lim_sup],
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        configure_plotly_theme(fig4)
        st.plotly_chart(fig4, use_container_width=True)
        
        st.markdown("<br><hr style='border-top:1px solid #E2E8F0;'/><br>", unsafe_allow_html=True)
        
        # NUEVA GRÁFICA: Prima Promedio por Sector
        st.markdown("##### 📊 Análisis de Riesgo por Sector Económico")
        st.markdown("Identifica qué actividades económicas concentran el mayor nivel de siniestralidad y, por tanto, las primas más altas.")
        
        avg_prima_sector = df.groupby('ACTIVIDAD')['PRIMA DE RIESGO ACTUAL'].mean().reset_index()
        avg_prima_sector = avg_prima_sector.sort_values(by='PRIMA DE RIESGO ACTUAL', ascending=True)
        
        min_val_s = avg_prima_sector['PRIMA DE RIESGO ACTUAL'].min()
        max_val = avg_prima_sector['PRIMA DE RIESGO ACTUAL'].max()
        fig4b = px.bar(
            avg_prima_sector,
            x='PRIMA DE RIESGO ACTUAL',
            y='ACTIVIDAD',
            orientation='h',
            color='PRIMA DE RIESGO ACTUAL',
            color_continuous_scale=px.colors.sequential.OrRd,
            color_continuous_scale=[[0, '#F97316'], [0.5, '#DC2626'], [1, '#7F0000']],
            range_color=[min_val_s, max_val],
            labels={'PRIMA DE RIESGO ACTUAL': 'Prima Promedio (%)', 'ACTIVIDAD': 'Sector Económico'},
            text=avg_prima_sector['PRIMA DE RIESGO ACTUAL'].apply(lambda x: f"{x:.2f}%"),
            title="Prima de Riesgo Promedio por Sector"
        )
        fig4b.update_traces(textposition='outside', textfont=dict(size=14, color='#0F172A', family="Outfit", weight='bold'))
        max_val = avg_prima_sector['PRIMA DE RIESGO ACTUAL'].max()
        fig4b.update_layout(yaxis=dict(tickmode='linear'), xaxis=dict(range=[0, max_val * 1.15]))
        fig4b.update_coloraxes(showscale=False)
        configure_plotly_theme(fig4b)
        st.plotly_chart(fig4b, use_container_width=True)
        st.markdown(
            """
            <div class="dark-panel" style="margin-top: 15px;">
                <h4>Gestión Preventiva de la Prima de Riesgo</h4>
                <p>La Prima de Riesgo de Trabajo es una de las cuotas patronales más variables. Se recalcula en febrero de cada año en función de los riesgos ocurridos en el ejercicio anterior (accidentes de trayecto, incapacidades temporales y defunciones).</p>
                <p><b>Clave Operativa:</b> Las empresas con programas robustos de medicina preventiva y capacitación en seguridad disminuyen su siniestralidad, lo que reduce legalmente su prima de riesgo anual, optimizando sus finanzas corporativas.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error("No se cuentan con los datos de Primas de Riesgo necesarios.")
    st.markdown('</div>', unsafe_allow_html=True)
with tab5:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("Promedio de Trabajadores Asegurados por Sector")
    st.markdown("Análisis representativo de la escala de mano de obra y empleabilidad directa por patrón.")
    
    if check_col('ACTIVIDAD') and check_col('TRABAJADORES'):
        df['TRABAJADORES'] = pd.to_numeric(df['TRABAJADORES'], errors='coerce').fillna(0)
        avg_workers = df.groupby('ACTIVIDAD')['TRABAJADORES'].mean().reset_index()
        avg_workers = avg_workers.sort_values(by='TRABAJADORES', ascending=True).tail(15)
        
        col1, col2 = st.columns([3, 2])
        with col1:
            # CORRECCIÓN: Título explícito, etiquetas legibles
            fig5 = px.bar(
                avg_workers,
                x='TRABAJADORES',
                y='ACTIVIDAD',
                orientation='h',
                color='TRABAJADORES',
                color_continuous_scale=px.colors.sequential.Tealgrn,
                labels={'TRABAJADORES': 'Promedio de Trabajadores por Empresa', 'ACTIVIDAD': 'Sector Económico'},
                text=avg_workers['TRABAJADORES'].apply(lambda x: f"{x:.0f} emp."), # Muestra texto de empleados
                title="Volumen Promedio de Plantilla Laboral"
            )
            fig5.update_traces(
                textposition='auto', 
                textfont=dict(size=13, color='white', weight="bold")
            )
            fig5.update_layout(yaxis=dict(tickmode='linear')) # Asegura mostrar todas las actividades en el eje Y
            fig5.update_coloraxes(showscale=False)
            configure_plotly_theme(fig5)
            st.plotly_chart(fig5, use_container_width=True)
            
        with col2:
            st.markdown(
                """
                <div class="dark-panel" style="margin-top: 15px;">
                    <h4>Sectores de Empleo Intensivo</h4>
                    <p>Este gráfico identifica qué sectores albergan corporativos de mayor tamaño organizativo:</p>
                    <ul>
                        <li><b>Construcción e Industria:</b> Suelen registrar una concentración masiva de jornaleros y albañiles de manera temporal.</li>
                        <li><b>Servicios de Limpieza / Seguridad:</b> Altamente intensivos en recursos humanos debido al outsourcing y subcontratación autorizada (REPSE).</li>
                        <li><b>Comercio:</b> Presenta una estructura más fragmentada, donde predominan las micro y pequeñas empresas familiares.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.error("Las columnas 'ACTIVIDAD' o 'TRABAJADORES' no están completas en el set de datos.")
    st.markdown('</div>', unsafe_allow_html=True)
with tab6:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("Tipos de Movimientos Afiliatorios Oficiales")
    st.markdown("Distribución y evolución histórica de los trámites patronales administrados ante la ventanilla única.")
    
    if check_col('TIPO DE MOVIMIENTO'):
        movimiento_counts = df['TIPO DE MOVIMIENTO'].value_counts()
        
        tramite_map = {
            '1': '1 — Alta Patronal',
            '2': '2 — Cambio de Domicilio',
            '3': '3 — Cambio de Representante Legal',
            '4': '4 — Renovación de TIP'
        }
        mov_index_mapped = [tramite_map.get(str(x), f"Trámite Código {x}") for x in movimiento_counts.index]
        
        col1, col2 = st.columns([3, 2])
        with col1:
            fig6a = px.pie(
                values=movimiento_counts.values,
                names=mov_index_mapped,
                hole=0.6,
                color_discrete_sequence=px.colors.qualitative.Prism,
                title="Proporción por Tipo de Trámite"
            )
            fig6a.update_traces(
                textposition='inside',
                textinfo='percent',
                marker=dict(line=dict(color='#FFFFFF', width=2)),
                insidetextfont=dict(size=14, color='white')
            )
            configure_plotly_theme(fig6a)
            st.plotly_chart(fig6a, use_container_width=True)
            
        with col2:
            st.markdown(
                """
                <div class="dark-panel">
                    <h4>Catálogo de Trámites — IMSS</h4>
                    <ul style="padding-left: 15px; margin: 0;">
                        <li style="margin-bottom:8px;"><b>Alta Patronal:</b> Asignación de registro ante el inicio de operaciones mercantiles.</li>
                        <li style="margin-bottom:8px;"><b>Cambio de Domicilio:</b> Actualización de la circunscripción de la subdelegación correspondiente.</li>
                        <li style="margin-bottom:8px;"><b>Representación Legal:</b> Sustitución o poder legal oficial ante el IMSS.</li>
                        <li><b>Renovación de Tarjeta de Identificación Patronal:</b> Vigencia de la credencial oficial de trámites.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        st.markdown("<br><hr style='border-top:1px solid #E2E8F0;'/><br>", unsafe_allow_html=True)
        
        st.markdown("##### Frecuencia e Historial de Movimientos por Año")
        if check_col('ULTIMO MOVIMIENTO FECHA ULTIMO MOV'):
            df['Año Movimiento'] = df['ULTIMO MOVIMIENTO FECHA ULTIMO MOV'].dt.year.astype('Int64')
            movimientos_por_año = df['Año Movimiento'].value_counts().sort_index()
            
            if not movimientos_por_año.empty:
                fig6b = px.line(
                    x=movimientos_por_año.index,
                    y=movimientos_por_año.values,
                    markers=True,
                    labels={'x': 'Año de Gestión', 'y': 'Número de Trámites Realizados'},
                    color_discrete_sequence=['#8B5CF6'],
                    title="Tendencia Histórica de Trámites (Por Año)"
                )
                fig6b.update_traces(line=dict(width=3), marker=dict(size=8))
                configure_plotly_theme(fig6b)
                st.plotly_chart(fig6b, use_container_width=True)
            else:
                st.info("Formato de fecha no compatible para la extracción anual.")
        else:
            st.warning("Columna de fecha del último movimiento no disponible.")
    else:
        st.error("Columna 'TIPO DE MOVIMIENTO' ausente.")
    st.markdown('</div>', unsafe_allow_html=True)
with tab7:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("Medio de Trámite: Transición Digital e Internet")
    st.markdown("Comparativa entre trámites virtuales mediante el escritorio digital vs. ventanilla física tradicional.")
    
    if check_col('MEDIO'):
        medio_counts = df['MEDIO'].value_counts()
        
        col1, col2 = st.columns([3, 2])
        with col1:
            fig7 = px.pie(
                values=medio_counts.values,
                names=medio_counts.index,
                hole=0.6,
                color_discrete_sequence=['#2563EB', '#F43F5E'],
                title="Trámites por Internet vs Ventanilla"
            )
            fig7.update_traces(
                textposition='inside',
                textinfo='percent+label',
                marker=dict(line=dict(color='#FFFFFF', width=2)),
                insidetextfont=dict(size=14, color='white')
            )
            configure_plotly_theme(fig7)
            st.plotly_chart(fig7, use_container_width=True)
            
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                """
                <div class="dark-panel">
                    <h4>Directriz de Transformación Digital</h4>
                    <p>El <b>Instituto Mexicano del Seguro Social</b> impulsa fuertemente el uso de herramientas digitales como el IDSE (IMSS desde su Empresa) y el Buzón IMSS.</p>
                    <p>El predominio de las operaciones por <b>INTERNET</b> descongestiona las salas físicas de la subdelegación, reduce los tiempos de respuesta de semanas a minutos y combate la corrupción, brindando certidumbre en tiempo real a los patrones de Yucatán.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.error("Columna 'MEDIO' no disponible.")
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown(
    """
    <a href="https://www.imss.gob.mx/tramites/alta-patronal" target="_blank" class="floating-action-btn">
        <span>💻</span> Trámite de Alta Patronal Digital
    </a>
    """,
    unsafe_allow_html=True
)
