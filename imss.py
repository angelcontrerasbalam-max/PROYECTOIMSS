import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# --- Configuración de la Página --- #
st.set_page_config(
    page_title="DEPARTAMENTO DE AFILIACIÓN Y VIGENCIA SUB DELEGACIÓN 33 LA CEIBA",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS Personalizado (Estilo Formal/Ejecutivo) ---
st.markdown(
    """
    <style>
    /* Forzar fondo claro y texto oscuro para evitar problemas con el modo oscuro automático */
    .stApp { background-color: #F0F2F6 !important; }
    .main { background-color: #F0F2F6 !important; }
    
    /* Forzar color oscuro en los textos normales de Streamlit */
    .stMarkdown p, .stText p, label, li, .stDataFrame { color: #1E293B !important; }
    p { color: #1E293B !important; }
    
    h1 { 
        color: #1E3A8A !important; 
        text-align: center;
        font-size: 2.5em;
        padding-bottom: 20px;
        font-family: 'Arial', sans-serif;
    }
    h2, h3, h4 { color: #1E3A8A !important; font-family: 'Arial', sans-serif; }
    
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1em;
        font-weight: bold;
        color: #1E3A8A !important;
    }
    .stTabs [data-baseweb="tab-list"] button {
        background-color: #E0E7FF; 
        border-radius: 5px 5px 0px 0px;
        padding: 10px 15px;
        border-bottom: 3px solid transparent;
    }
    .stTabs [data-baseweb="tab-list"] button:hover {
        border-bottom: 3px solid #4CAF50; 
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        border-bottom: 3px solid #1E3A8A; 
        background-color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True
)

# --- Título ---
st.title('DEPARTAMENTO DE AFILIACIÓN Y VIGENCIA SUB DELEGACIÓN 33 LA CEIBA')

# --- Carga y Limpieza de Datos ---
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        # ESTA LÍNEA SOLUCIONA TU ERROR: Estandariza las columnas a mayúsculas y quita espacios invisibles
        df.columns = df.columns.astype(str).str.strip().str.upper()
        
        if 'ULTIMO MOVIMIENTO FECHA ULTIMO MOV' in df.columns:
            df['ULTIMO MOVIMIENTO FECHA ULTIMO MOV'] = pd.to_datetime(df['ULTIMO MOVIMIENTO FECHA ULTIMO MOV'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo Excel: {e}")
        return pd.DataFrame()

# Cargar el Dataframe
file_path = 'DATOS/PATRONES PROYECTO FINAL.xlsx'
df = load_data(file_path)

if df.empty:
    st.warning("No se pudo cargar la información. Por favor, verifica que el archivo Excel esté en la ruta 'DATOS/PATRONES PROYECTO FINAL.xlsx'.")
    st.stop()

# Función para evitar errores si no existe la columna en el Excel
def check_col(col_name):
    return col_name in df.columns

# --- Buscador y Archivero Visual ---
st.header('Búsqueda de Registro Patronal')
registro_patronal_input = st.text_input('🔍 Ingresa el Registro Patronal para buscar:', '')

if registro_patronal_input:
    if check_col('REGISTRO PATRONAL'):
        filtered_patron = df[df['REGISTRO PATRONAL'].astype(str).str.contains(registro_patronal_input, case=False, na=False)]
        
        if not filtered_patron.empty:
            st.subheader('Datos del Patrón Encontrado:')
            st.dataframe(filtered_patron.reset_index(drop=True), use_container_width=True)

            if check_col('UBICACIÓN DE ARCHIVO'):
                st.subheader('Ubicación Física del Archivo:')
                location_str = str(filtered_patron['UBICACIÓN DE ARCHIVO'].iloc[0])
                
                # Función para extraer datos del string
                def parse_location(location_string):
                    cabinet_match = re.search(r'ARCHIVERO\s*(\d+)', location_string, re.IGNORECASE)
                    fila_match = re.search(r'FILA\s*(\d+)', location_string, re.IGNORECASE)
                    seccion_match = re.search(r'SECCI[OÓ]N\s*([A-G])', location_string, re.IGNORECASE)
                    
                    cabinet = int(cabinet_match.group(1)) if cabinet_match else None
                    fila = int(fila_match.group(1)) if fila_match else None
                    seccion = seccion_match.group(1).upper() if seccion_match else None
                    return cabinet, fila, seccion

                cabinet, fila, seccion = parse_location(location_str)

                if cabinet and fila and seccion:
                    st.success(f"📂 El archivo se encuentra en el **Archivero {cabinet}, Fila {fila}, Sección {seccion}**.")
                    
                    # Generar Representación Visual del Archivero en HTML/CSS
                    st.markdown("### Representación Visual de los Archiveros:")
                    html_archivero = "<div style='display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;'>"
                    for c in range(1, 6): # 5 Archiveros
                        border_color = "#4CAF50" if c == cabinet else "#1E3A8A"
                        box_shadow = "box-shadow: 0px 4px 8px rgba(76, 175, 80, 0.6);" if c == cabinet else "box-shadow: 0px 2px 4px rgba(0,0,0,0.1);"
                        
                        html_archivero += f"<div style='border: 3px solid {border_color}; padding: 10px; border-radius: 8px; background: #FFFFFF; {box_shadow}'><h4 style='text-align:center; color:{border_color}; margin-top:0;'>Archivero {c}</h4><table style='border-collapse: collapse; width: 100%; font-size: 0.9em;'>"
                        
                        # Encabezados de columnas (A-G)
                        html_archivero += "<tr><th style='padding: 5px;'></th>"
                        for s_char in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
                            html_archivero += f"<th style='padding: 5px; text-align: center; color: #555;'>{s_char}</th>"
                        html_archivero += "</tr>"

                        for r in range(1, 8): # 7 Filas
                            html_archivero += "<tr><td style='padding: 5px; font-weight: bold; color: #555;'>F{r}</td>"
                            for s_char in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
                                if c == cabinet and r == fila and s_char == seccion:
                                    bg, color, weight, text = "#4CAF50", "white", "bold", "📂"
                                else:
                                    bg, color, weight, text = "#F8F9FA", "#DDD", "normal", "X"
                                html_archivero += f"<td style='border: 1px solid #ddd; background-color: {bg}; color: {color}; font-weight: {weight}; text-align: center; padding: 5px; width: 35px; height: 35px;'>{text}</td>"
                            html_archivero += "</tr>"
                        html_archivero += "</table></div>"
                    html_archivero += "</div>"
                    
                    st.markdown(html_archivero, unsafe_allow_html=True)
                else:
                    st.warning(f"No se pudo descifrar la coordenada exacta del archivo a partir de: '{location_str}'. Asegúrate de que siga el formato: 'ARCHIVERO X', 'FILA X', 'SECCIÓN X'.")
            else:
                st.info("La columna 'UBICACIÓN DE ARCHIVO' no está disponible.")
        else:
            st.warning('No se encontró ningún patrón con ese Registro Patronal.')
    else:
        st.error(f"⚠️ No se encontró la columna 'REGISTRO PATRONAL' en el Excel. Columnas detectadas: {', '.join(df.columns)}")

st.markdown('<hr style="border-top: 3px solid #1E3A8A;">', unsafe_allow_html=True)

# --- Pestañas de Análisis ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Estatus Patronal", 
    "📉 Motivos de Baja", 
    "🏭 Actividades Económicas", 
    "⚠️ Primas de Riesgo", 
    "👷 Trabajadores por Actividad", 
    "📑 Movimientos Afiliatorios"
])

with tab1:
    st.header("ESTATUS PATRONAL SECCIÓN NORTE")
    if check_col('ESTATUS'):
        estatus_counts = df['ESTATUS'].value_counts()
        col1, col2 = st.columns([1, 1])
        with col1:
            fig1, ax1 = plt.subplots(figsize=(6, 6))
            ax1.pie(estatus_counts, labels=estatus_counts.index, autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#E74C3C', '#F39C12'])
            ax1.axis('equal')
            st.pyplot(fig1)
        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown(
                """
                <div style='background-color: #FFFFFF; padding: 20px; border-radius: 8px; border-left: 5px solid #1E3A8A; box-shadow: 0px 4px 6px rgba(0,0,0,0.05);'>
                <h4 style="margin-top:0; color:#1E3A8A;">Análisis del Estatus</h4>
                Esta gráfica de pastel muestra la distribución porcentual de los patrones 
                dados de <b>ALTA</b> y <b>BAJA</b> en la sección. Es un indicador clave para 
                entender la dinámica de crecimiento y contracción de la base patronal. 
                <br><br>
                Un porcentaje alto de patrones <b>'ALTA'</b> indica un ambiente económico 
                activo y saludable en términos de nuevas empresas y generación de empleos.
                </div>
                """, unsafe_allow_html=True
            )
    else:
        st.error("Columna 'ESTATUS' no encontrada.")

with tab2:
    st.header("PRINCIPALES MOTIVOS DE BAJA PATRONAL")
    if check_col('ESTATUS') and check_col('MOTIVO BAJA'):
        baja_motivos = df[df['ESTATUS'] == 'BAJA']['MOTIVO BAJA'].value_counts()
        if not baja_motivos.empty:
            col1, col2 = st.columns([1, 1])
            with col1:
                fig2, ax2 = plt.subplots(figsize=(6, 6))
                ax2.pie(baja_motivos, labels=baja_motivos.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
                ax2.axis('equal')
                st.pyplot(fig2)
            with col2:
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.markdown(
                    """
                    <div style='background-color: #FFFFFF; padding: 20px; border-radius: 8px; border-left: 5px solid #E74C3C; box-shadow: 0px 4px 6px rgba(0,0,0,0.05);'>
                    <h4 style="margin-top:0; color:#E74C3C;">Motivos Legales de Baja</h4>
                    Esta gráfica ilustra las razones principales por las cuales los registros patronales son dados de baja. 
                    <br><br>
                    Según la <b>Ley del Instituto Mexicano del Seguro Social (IMSS)</b>, la baja de un registro patronal 
                    puede ocurrir de forma obligatoria por la falta de localización del domicilio o el impago 
                    de cuotas obrero-patronales prolongado. Estas situaciones conllevan a que el IMSS inicie procedimientos para 
                    regularizar la situación o dar de baja el registro para proteger los fondos de recaudación del sistema y salvaguardar los derechos de los trabajadores.
                    </div>
                    """, unsafe_allow_html=True
                )
        else:
            st.info("No hay datos de patrones con estatus 'BAJA' o motivos registrados para analizar.")
    else:
        st.error("Columnas 'ESTATUS' o 'MOTIVO BAJA' no encontradas.")

with tab3:
    st.header("PRINCIPALES ACTIVIDADES ECONÓMICAS DE PATRONES EN LA DELEGACIÓN NORTE")
    if check_col('ACTIVIDAD'):
        actividad_counts = df['ACTIVIDAD'].value_counts().head(10)
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        sns.barplot(x=actividad_counts.values, y=actividad_counts.index, palette='viridis', ax=ax3)
        ax3.set_title('Top 10 Actividades Económicas')
        ax3.set_xlabel('Número de Patrones')
        ax3.set_ylabel('')
        st.pyplot(fig3)
        st.markdown(
            """
            <div style='background-color: #FFFFFF; padding: 20px; border-radius: 8px; border-left: 5px solid #27AE60; box-shadow: 0px 4px 6px rgba(0,0,0,0.05);'>
            <h4 style="margin-top:0; color:#27AE60;">Contexto Económico de Yucatán</h4>
            Este gráfico de barras muestra las actividades económicas predominantes entre los patrones de la delegación.
            <ul>
                <li><b>SERVICIOS:</b> En este grupo se encuentran actividades destinadas a brindar atención y soluciones para satisfacer necesidades de la población, como turismo, restaurantes, consultoría y servicios profesionales.</li>
                <li><b>CONSTRUCCIÓN:</b> Engloba a empresas dedicadas a la edificación y desarrollo inmobiliario, siendo un motor de empleo temporal.</li>
                <li><b>MANUFACTURA:</b> Comprende la transformación de materias primas en productos elaborados (ej. industria textil, aeroespacial y maquiladora).</li>
            </ul>
            En <b>Yucatán</b>, la diversificación económica ha impulsado enormemente el turismo y los servicios. Además, la construcción ha experimentado un auge histórico debido al crecimiento urbano, desarrollos inmobiliarios y proyectos de infraestructura en la región.
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.error("Columna 'ACTIVIDAD' no encontrada.")

with tab4:
    st.header("PRIMAS DE RIESGO PATRONALES")
    if check_col('PRIMA DE RIESGO ACTUAL') and check_col('PRIMA DE RIESGO ANTERIOR') and check_col('REGISTRO PATRONAL'):
        df['PRIMA DE RIESGO ACTUAL'] = pd.to_numeric(df['PRIMA DE RIESGO ACTUAL'], errors='coerce').fillna(0)
        df['PRIMA DE RIESGO ANTERIOR'] = pd.to_numeric(df['PRIMA DE RIESGO ANTERIOR'], errors='coerce').fillna(0)
        df['CAMBIO PRIMA DE RIESGO'] = df['PRIMA DE RIESGO ACTUAL'] - df['PRIMA DE RIESGO ANTERIOR']

        col1, col2 = st.columns(2)
        with col1:
            st.subheader('📈 10 Patrones con Mayor Aumento')
            top_increase = df.sort_values(by='CAMBIO PRIMA DE RIESGO', ascending=False).head(10)
            cols_to_show = ['REGISTRO PATRONAL', 'PRIMA DE RIESGO ANTERIOR', 'PRIMA DE RIESGO ACTUAL', 'CAMBIO PRIMA DE RIESGO']
            st.dataframe(top_increase[cols_to_show], use_container_width=True)

        with col2:
            st.subheader('📉 10 Patrones con Mayor Decremento')
            top_decrease = df.sort_values(by='CAMBIO PRIMA DE RIESGO', ascending=True).head(10)
            st.dataframe(top_decrease[cols_to_show], use_container_width=True)
        
        # Gráfica de Tendencia
        fig4, ax4 = plt.subplots(figsize=(10, 5))
        sns.scatterplot(x='PRIMA DE RIESGO ANTERIOR', y='PRIMA DE RIESGO ACTUAL', data=df, ax=ax4, hue='CAMBIO PRIMA DE RIESGO', size='CAMBIO PRIMA DE RIESGO', sizes=(20, 300), palette='coolwarm')
        
        min_val = min(df['PRIMA DE RIESGO ANTERIOR'].min(), df['PRIMA DE RIESGO ACTUAL'].min())
        max_val = max(df['PRIMA DE RIESGO ANTERIOR'].max(), df['PRIMA DE RIESGO ACTUAL'].max())
        ax4.plot([min_val, max_val], [min_val, max_val], 'k--', label='Sin Cambio (Misma Prima)', alpha=0.5)
        
        ax4.set_title('Tendencia de Prima de Riesgo (Anterior vs. Actual)')
        ax4.set_xlabel('Prima de Riesgo Anterior')
        ax4.set_ylabel('Prima de Riesgo Actual')
        ax4.legend()
        st.pyplot(fig4)

        st.markdown(
            """
            <div style='background-color: #FFFFFF; padding: 20px; border-radius: 8px; border-left: 5px solid #F39C12; box-shadow: 0px 4px 6px rgba(0,0,0,0.05);'>
            <h4 style="margin-top:0; color:#F39C12;">¿Qué es la Prima de Riesgo de Trabajo del IMSS?</h4>
            Es una cuota obligatoria que los patrones pagan al IMSS para cubrir la probabilidad de ocurrencia de accidentes o enfermedades laborales de sus trabajadores. Esta cuota financia las prestaciones médicas y económicas.
            <br><br>
            <b>¿De qué depende la asignación de la Prima de Riesgo?</b><br>
            Depende de la clase de riesgo de la actividad económica de la empresa (Clase I a V). Al inscribirse, a la empresa se le asigna una "prima media" correspondiente a su clase.
            <br><br>
            <b>¿De qué depende que aumente o baje la Prima de Riesgo?</b>
            <ul>
                <li><b>Aumento:</b> La prima sube si, tras la revisión anual de siniestralidad, se constata que ocurrieron más accidentes, enfermedades o defunciones por riesgo de trabajo en la empresa.</li>
                <li><b>Disminución:</b> La prima baja si la empresa mejora sus protocolos de seguridad, logrando reducir o mantener su índice de siniestralidad al mínimo (menos accidentes o incapacidades).</li>
            </ul>
            <small><i>Toda esta información está estipulada según la Ley del Seguro Social.</i></small>
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.error("Faltan columnas ('PRIMA DE RIESGO ACTUAL' o 'PRIMA DE RIESGO ANTERIOR') para este análisis.")

with tab5:
    st.header("TRABAJADORES POR ACTIVIDAD")
    if check_col('ACTIVIDAD') and check_col('TRABAJADORES'):
        df['TRABAJADORES'] = pd.to_numeric(df['TRABAJADORES'], errors='coerce').fillna(0)
        avg_workers_by_activity = df.groupby('ACTIVIDAD')['TRABAJADORES'].mean().sort_values(ascending=False).head(15)
        
        fig5, ax5 = plt.subplots(figsize=(10, 6))
        sns.barplot(x=avg_workers_by_activity.values, y=avg_workers_by_activity.index, palette='magma', ax=ax5)
        ax5.set_title('Promedio de Trabajadores por Sector Económico')
        ax5.set_xlabel('Promedio de Empleados por Patrón')
        ax5.set_ylabel('')
        st.pyplot(fig5)

        st.markdown(
            """
            <div style='background-color: #FFFFFF; padding: 20px; border-radius: 8px; border-left: 5px solid #8E44AD; box-shadow: 0px 4px 6px rgba(0,0,0,0.05);'>
            <h4 style="margin-top:0; color:#8E44AD;">Sectores Intensivos en Mano de Obra</h4>
            Este análisis promedia el número de trabajadores por actividad económica, mostrando qué sectores emplean a más personal por unidad económica de manera directa.
            <br><br>
            Actividades como la <b>CONSTRUCCIÓN</b>, <b>AGRICULTURA EXTENSIVA</b> o <b>MANUFACTURA MASIVA</b> suelen requerir grandes volúmenes de personal para operar, lo que las convierte en sectores "intensivos en mano de obra". En contraste, sectores como el comercio al detalle, servicios inmobiliarios o consultorías tienden a funcionar con planillas más reducidas y un mayor enfoque en el conocimiento.
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.error("Columnas 'ACTIVIDAD' o 'TRABAJADORES' no encontradas.")

with tab6:
    st.header("MOVIMIENTOS AFILIATORIOS")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Tipos de Movimientos Realizados')
        if check_col('TIPO DE MOVIMIENTO'):
            movimiento_counts = df['TIPO DE MOVIMIENTO'].value_counts()
            fig6a, ax6a = plt.subplots(figsize=(6, 6))
            ax6a.pie(movimiento_counts, labels=movimiento_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("cool"))
            ax6a.axis('equal')
            st.pyplot(fig6a)
            st.markdown(
                """
                <div style='background-color: #F8F9FA; padding: 15px; border-radius: 5px; font-size: 0.9em;'>
                <b>Tipos de Movimientos (IMSS):</b>
                <ul>
                    <li><b>Alta:</b> Inscripción inicial del patrón ante el IMSS adquiriendo obligaciones.</li>
                    <li><b>Baja:</b> Clausura o terminación definitiva de la relación obrero-patronal.</li>
                    <li><b>Modificación:</b> Cambio de salario, actividad, representante legal o datos del registro.</li>
                    <li><b>Reingreso:</b> Reactivación de un registro patronal tras una baja previa.</li>
                </ul>
                <small><i>Estos son los movimientos administrativos registrados oficialmente.</i></small>
                </div>
                """, unsafe_allow_html=True
            )
        else:
            st.warning("Columna 'TIPO DE MOVIMIENTO' no encontrada.")

    with col2:
        st.subheader('Medio de Trámite: Internet vs Ventanilla')
        if check_col('MEDIO'):
            medio_counts = df['MEDIO'].value_counts()
            fig6c, ax6c = plt.subplots(figsize=(6, 6))
            ax6c.pie(medio_counts, labels=medio_counts.index, autopct='%1.1f%%', startangle=90, colors=['#3498DB', '#E74C3C', '#2ECC71'])
            ax6c.axis('equal')
            st.pyplot(fig6c)
            st.markdown(
                """
                <div style='background-color: #F8F9FA; padding: 15px; border-radius: 5px; font-size: 0.9em;'>
                <b>Digitalización de Trámites:</b><br>
                El <b>IMSS</b> está impulsando intensivamente su plataforma digital y el Buzón IMSS. 
                El objetivo primordial es que los patrones puedan realizar sus movimientos a través de <b>INTERNET</b> para evitar que tengan que ir físicamente a la subdelegación, eliminando filas, agilizando la actualización y reduciendo los tiempos de respuesta de forma significativa.
                </div>
                """, unsafe_allow_html=True
            )
        else:
            st.warning("Columna 'MEDIO' no encontrada.")

    st.markdown("---")
    st.subheader('Frecuencia de Movimientos por Año')
    if check_col('ULTIMO MOVIMIENTO FECHA ULTIMO MOV'):
        df['Año Movimiento'] = df['ULTIMO MOVIMIENTO FECHA ULTIMO MOV'].dt.year.astype('Int64')
        movimientos_por_año = df['Año Movimiento'].value_counts().sort_index()
        if not movimientos_por_año.empty:
            fig6b, ax6b = plt.subplots(figsize=(10, 4))
            sns.lineplot(x=movimientos_por_año.index, y=movimientos_por_año.values, marker='o', ax=ax6b, color='#8E44AD', linewidth=2.5)
            ax6b.set_title('Tendencia de Movimientos Registrados por Año')
            ax6b.set_xlabel('Año')
            ax6b.set_ylabel('Número de Movimientos')
            ax6b.grid(True, linestyle='--', alpha=0.7)
            st.pyplot(fig6b)
        else:
            st.info("No hay fechas válidas para graficar la tendencia por año.")
    else:
        st.warning("La columna 'ULTIMO MOVIMIENTO FECHA ULTIMO MOV' no se encuentra en tu Excel.")
