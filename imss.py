import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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
    /* Forzar fondo claro principal */
    .stApp { background-color: #F0F2F6 !important; }
    .main { background-color: #F0F2F6 !important; }
    
    /* Forzar color oscuro en los textos normales de Streamlit */
    .stMarkdown p, .stText p, label, li { color: #1E293B; }
    p { color: #1E293B; }
    
    /* Color blanco garantizado para TODO dentro de tarjetas oscuras */
    .dark-card, .dark-card * { color: #FFFFFF !important; }
    
    /* Botón Flotante */
    .floating-btn {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background-color: #1E3A8A;
        color: white !important;
        border-radius: 50px;
        padding: 15px 25px;
        font-size: 16px;
        font-weight: bold;
        text-decoration: none;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
        z-index: 99999;
        display: flex;
        align-items: center;
        gap: 10px;
        transition: 0.3s;
        border: 2px solid white;
    }
    .floating-btn:hover {
        background-color: #4CAF50;
        transform: scale(1.05);
        color: white !important;
    }
    
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
                    st.success(f"📂 El archivo se encuentra en el **Archivero {cabinet}, Fila {fila}, Sección {seccion}**.")
                    
                    st.markdown("### Representación Visual de los Archiveros:")
                    html_archivero = "<div style='display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;'>"
                    for c in range(1, 6):
                        border_color = "#4CAF50" if c == cabinet else "#1E3A8A"
                        box_shadow = "box-shadow: 0px 4px 8px rgba(76, 175, 80, 0.6);" if c == cabinet else "box-shadow: 0px 2px 4px rgba(0,0,0,0.1);"
                        
                        html_archivero += f"<div style='border: 3px solid {border_color}; padding: 10px; border-radius: 8px; background: #FFFFFF; {box_shadow}'><h4 style='text-align:center; color:{border_color}; margin-top:0;'>Archivero {c}</h4><table style='border-collapse: collapse; width: 100%; font-size: 0.9em;'>"
                        
                        html_archivero += "<tr><th style='padding: 5px;'></th>"
                        for s_char in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
                            html_archivero += f"<th style='padding: 5px; text-align: center; color: #555;'>{s_char}</th>"
                        html_archivero += "</tr>"
                        for r in range(1, 8):
                            html_archivero += f"<tr><td style='padding: 5px; font-weight: bold; color: #555;'>{r}</td>"
                            for s_char in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
                                if c == cabinet and r == fila and s_char == seccion:
                                    bg, color, weight, text = "#4CAF50", "white", "bold", "📂"
                                else:
                                    bg, color, weight, text = "#F8F9FA", "#DDD", "normal", "&nbsp;"
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
# Se añade la nueva pestaña "🌐 Medios" al final
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Estatus Patronal", 
    "📉 Motivos de Baja", 
    "🏭 Actividades Económicas", 
    "⚠️ Primas de Riesgo", 
    "👷 Trabajadores por Actividad", 
    "📑 Movimientos Afiliatorios",
    "🌐 Medios"
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
                <div class='dark-card' style='background-color: #1E293B; padding: 20px; border-radius: 8px; border-left: 5px solid #4CAF50; box-shadow: 0px 4px 6px rgba(0,0,0,0.2);'>
                <h4 style="margin-top:0; color:#4CAF50;">Análisis del Estatus</h4>
                El 88.4% de patrones activos en la sección norte refleja la fortaleza empresarial de Mérida, impulsada por turismo, servicios y nuevas inversiones. El 11.6% de bajas corresponde a ajustes en sectores tradicionales, principalmente comercio y pequeñas empresas, que requieren atención estratégica.
                <br><br>
                Este balance confirma un entorno económico estable, con tendencia positiva hacia la generación de empleos y consolidación de la base patronal. La vigilancia de las bajas permitirá anticipar riesgos y diseñar políticas de apoyo que mantengan el dinamismo regional.
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
                    <div class='dark-card' style='background-color: #1E293B; padding: 20px; border-radius: 8px; border-left: 5px solid #E74C3C; box-shadow: 0px 4px 6px rgba(0,0,0,0.2);'>
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
            <div class='dark-card' style='background-color: #1E293B; padding: 20px; border-radius: 8px; border-left: 5px solid #27AE60; box-shadow: 0px 4px 6px rgba(0,0,0,0.2);'>
            <h4 style="margin-top:0; color:#27AE60;">Contexto Económico de Yucatán</h4>
            <ul style='list-style-type: none; padding-left: 0;'>
                <li style='margin-bottom: 10px;'>🛎️ <b>SERVICIOS:</b> Es la actividad más representativa. En Mérida, los servicios abarcan turismo, salud, educación, restaurantes y hotelería. Refleja el papel de la ciudad como centro regional de comercio y cultura.</li>
                <li style='margin-bottom: 10px;'>🏗️ <b>CONSTRUCCIÓN:</b> Segundo lugar en importancia. El auge inmobiliario y proyectos como el Tren Maya y el Puerto de Progreso han impulsado la demanda de constructoras y desarrolladoras.</li>
                <li style='margin-bottom: 10px;'>🛒 <b>COMERCIO:</b> Incluye comercio mayorista y minorista. Mérida concentra más del 38% de las unidades económicas del estado, con fuerte presencia de supermercados, tiendas locales y cadenas nacionales.</li>
                <li style='margin-bottom: 10px;'>💼 <b>CONSULTORÍA:</b> Representa servicios profesionales en áreas como contabilidad, auditoría, asesoría legal y tecnológica. Su crecimiento está ligado al aumento de empresas formales que requieren soporte especializado.</li>
                <li style='margin-bottom: 10px;'>🏭 <b>FABRICACIÓN:</b> Incluye manufactura ligera, textil, agroindustrial y alimentos procesados. Aunque no es el sector dominante, es clave para exportaciones y encadenamientos productivos.</li>
                <li>🔬 <b>INVESTIGACIÓN:</b> Vinculada a universidades y centros tecnológicos de Mérida, como la UADY y el Parque Científico y Tecnológico de Yucatán. Impulsa innovación en biotecnología, energías renovables y ciencias sociales.</li>
            </ul>
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
            <div class='dark-card' style='background-color: #1E293B; padding: 20px; border-radius: 8px; border-left: 5px solid #F39C12; box-shadow: 0px 4px 6px rgba(0,0,0,0.2);'>
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
            <div class='dark-card' style='background-color: #1E293B; padding: 20px; border-radius: 8px; border-left: 5px solid #8E44AD; box-shadow: 0px 4px 6px rgba(0,0,0,0.2);'>
            <h4 style="margin-top:0; color:#8E44AD;">Sectores Intensivos en Mano de Obra</h4>
            Este análisis promedia el número de trabajadores por actividad económica, mostrando qué sectores emplean a más personal por unidad económica de manera directa.
            <br><br>
            Actividades como la <b>CONSTRUCCIÓN</b>, <b>AGRICULTURA EXTENSIVA</b> o <b>MANUFACTURA MASIVA</b> suelen requerir grandes volúmenes de personal para operar, lo que las convierte en sectores "intensivos en mano de obra". En contraste, sectores como el comercio al detalle, servicios inmobiliarios o consultorías tienden a funcionar con planillas más reducidas y un mayor enfoque en el conocimiento.
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.error("Columnas 'ACTIVIDAD' o 'TRABAJADORES' no encontradas.")
# ─────────────────────────────────────────────────────────────────────────────
# TAB 6 — MOVIMIENTOS AFILIATORIOS (sin la sección de Medios)
# ─────────────────────────────────────────────────────────────────────────────
with tab6:
    st.header("MOVIMIENTOS AFILIATORIOS")
    if check_col('TIPO DE MOVIMIENTO'):
        movimiento_counts = df['TIPO DE MOVIMIENTO'].value_counts()
        # Paleta de colores para la gráfica de pastel
        pie_colors = ['#3498DB', '#9B59B6', '#1ABC9C', '#E67E22', '#E74C3C',
                      '#2ECC71', '#F39C12', '#D35400', '#8E44AD', '#2980B9']
        fig6a, ax6a = plt.subplots(figsize=(7, 7))
        wedges, texts, autotexts = ax6a.pie(
            movimiento_counts,
            labels=None,          # Quitamos labels del pastel para usar solo la leyenda
            autopct='%1.1f%%',
            startangle=90,
            colors=pie_colors[:len(movimiento_counts)],
            pctdistance=0.75,
            wedgeprops=dict(edgecolor='white', linewidth=1.5)
        )
        # Hacer los porcentajes más legibles
        for autotext in autotexts:
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')
            autotext.set_color('white')
        ax6a.axis('equal')
        # ── Mapeo de códigos numéricos a nombres de trámite ──
        tramite_nombres = {
            '1': '1 — Alta Patronal',
            '2': '2 — Cambio de Domicilio',
            '3': '3 — Cambio de Representante Legal',
            '4': '4 — Renovación de TIP',
        }
        # ── Leyenda con nombre completo de cada tipo de trámite ──
        legend_patches = [
            mpatches.Patch(
                color=pie_colors[i],
                label=tramite_nombres.get(str(label), str(label))
            )
            for i, label in enumerate(movimiento_counts.index)
        ]
        ax6a.legend(
            handles=legend_patches,
            title="Tipo de Trámite",
            title_fontsize=11,
            fontsize=10,
            loc='lower center',
            bbox_to_anchor=(0.5, -0.28),
            ncol=1,
            frameon=True,
            framealpha=0.9
        )
        ax6a.set_title('Tipos de Movimientos Afiliatorios Realizados', fontsize=13, fontweight='bold', pad=15)
        plt.tight_layout()
        st.pyplot(fig6a)
        # ── Tarjeta con las nuevas definiciones ──
        st.markdown(
            """
            <div class='dark-card' style='background-color: #1E293B; padding: 20px; border-radius: 8px; border-left: 4px solid #3498DB; margin-top: 20px;'>
            <h4 style="margin-top:0; color:#3498DB;">Tipos de Trámites Afiliatorios — IMSS</h4>
            <ul style='padding-left: 18px; line-height: 1.8;'>
                <li>
                    <b>Alta Patronal:</b> Registro inicial de un patrón ante el IMSS para obtener su número de registro patronal 
                    y cumplir con obligaciones de seguridad social.
                </li>
                <li>
                    <b>Cambio de Domicilio:</b> Aviso al IMSS cuando el patrón modifica la ubicación de su centro de trabajo, 
                    para mantener actualizada la información oficial.
                </li>
                <li>
                    <b>Cambio de Representante Legal:</b> Notificación al IMSS sobre la sustitución del representante legal 
                    autorizado, garantizando la validez de trámites y obligaciones.
                </li>
                <li>
                    <b>Renovación de TIP (Tarjeta de Identificación Patronal):</b> Actualización del documento que acredita 
                    al patrón ante el IMSS, necesaria para realizar trámites electrónicos y presenciales.
                </li>
            </ul>
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.warning("Columna 'TIPO DE MOVIMIENTO' no encontrada.")
    st.markdown("---")
    # ── Gráfica de tendencia por año ──
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
# ─────────────────────────────────────────────────────────────────────────────
# TAB 7 — MEDIOS  (nueva pestaña con el contenido que antes estaba en tab6)
# ─────────────────────────────────────────────────────────────────────────────
with tab7:
    st.header("MEDIO DE TRÁMITE: INTERNET VS VENTANILLA")
    if check_col('MEDIO'):
        medio_counts = df['MEDIO'].value_counts()
        # Colores por medio
        medio_colors = ['#3498DB', '#E74C3C', '#2ECC71', '#F39C12', '#9B59B6']
        fig7, ax7 = plt.subplots(figsize=(7, 7))
        wedges7, texts7, autotexts7 = ax7.pie(
            medio_counts,
            labels=None,
            autopct='%1.1f%%',
            startangle=90,
            colors=medio_colors[:len(medio_counts)],
            pctdistance=0.75,
            wedgeprops=dict(edgecolor='white', linewidth=1.5)
        )
        for autotext in autotexts7:
            autotext.set_fontsize(11)
            autotext.set_fontweight('bold')
            autotext.set_color('white')
        ax7.axis('equal')
        # Leyenda con nombres de cada medio
        legend_patches7 = [
            mpatches.Patch(color=medio_colors[i], label=label)
            for i, label in enumerate(medio_counts.index)
        ]
        ax7.legend(
            handles=legend_patches7,
            title="Medio de Trámite",
            title_fontsize=11,
            fontsize=10,
            loc='lower center',
            bbox_to_anchor=(0.5, -0.18),
            ncol=2,
            frameon=True,
            framealpha=0.9
        )
        ax7.set_title('Distribución por Medio de Trámite', fontsize=13, fontweight='bold', pad=15)
        plt.tight_layout()
        st.pyplot(fig7)
        st.markdown(
            """
            <div class='dark-card' style='background-color: #1E293B; padding: 20px; border-radius: 8px; border-left: 4px solid #E74C3C; margin-top: 20px;'>
            <b style='color:#E74C3C; font-size:1.05em;'>Digitalización de Trámites</b><br><br>
            El <b>IMSS</b> está impulsando intensivamente su plataforma digital y el Buzón IMSS. 
            El objetivo primordial es que los patrones puedan realizar sus movimientos a través de <b>INTERNET</b> 
            para evitar que tengan que ir físicamente a la subdelegación, eliminando filas, agilizando la actualización 
            y reduciendo los tiempos de respuesta de forma significativa.
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.warning("Columna 'MEDIO' no encontrada.")
# --- Botón Flotante Fijo ---
st.markdown('<a href="https://www.imss.gob.mx/tramites/alta-patronal" target="_blank" class="floating-btn">💻 Trámite Alta Patronal</a>', unsafe_allow_html=True)
