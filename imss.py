import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re # For parsing the file location string

# --- Page Configuration --- #
st.set_page_config(
    page_title="DEPARTAMENTO DE AFILIACIÓN Y VIGENCIA SUB DELEGACIÓN 33 LA CEIBA",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for styling (formal, executive look) ---
st.markdown(
    """
    <style>
    .main { 
        background-color: #F0F2F6; /* Light grey background */
    }
    .stApp {
        background-color: #F0F2F6;
    }
    h1 { 
        color: #1E3A8A; /* Dark blue for title */
        text-align: center;
        font-size: 2.5em;
        padding-bottom: 20px;
    }
    h2 {
        color: #1E3A8A;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size:1.2em;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab-list"] button {
        background-color: #E0E7FF; /* Light blue for tabs */
        border-radius: 4px 4px 0px 0px;
        padding: 10px 15px;
        border-bottom: 2px solid #1E3A8A;
    }
    .stTabs [data-baseweb="tab-list"] button:hover {
        border-bottom: 2px solid #4CAF50; /* Green on hover */
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        border-bottom: 2px solid #007BFF; /* Active tab blue */
    }
    .reportview-container .main .block-container{ 
        padding-top: 2rem; 
        padding-bottom: 2rem;
    }
    .stTextInput>div>div>input {
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    .stButton>button {
        background-color: #4CAF50; /* Green button */
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True
)

# --- Title ---
st.title('DEPARTAMENTO DE AFILIACIÓN Y VIGENCIA SUB DELEGACIÓN 33 LA CEIBA')

# --- Data Loading ---
@st.cache_data
def load_data(file_path):
    df = pd.read_excel(file_path)
    # Ensure date column is datetime for potential time series analysis
    if 'ULTIMO MOVIMIENTO FECHA ULTIMO MOV' in df.columns:
        df['ULTIMO MOVIMIENTO FECHA ULTIMO MOV'] = pd.to_datetime(df['ULTIMO MOVIMIENTO FECHA ULTIMO MOV'], errors='coerce')
    return df

file_path = 'DATOS/PATRONES PROYECTO FINAL.xlsx'
df = load_data(file_path)

# --- Search Bar and Patron Data Display ---
st.header('Búsqueda de Registro Patronal')
registro_patronal_input = st.text_input('Ingresa el Registro Patronal para buscar:', '')

if registro_patronal_input:
    # Ensure the input matches the format of the 'REGISTRO PATRONAL' column
    # Assuming the format is consistent, we'll try to find an exact match
    filtered_patron = df[df['REGISTRO PATRONAL'].astype(str).str.contains(registro_patronal_input, case=False, na=False)]
    
    if not filtered_patron.empty:
        st.subheader('Datos del Patrón Encontrado:')
        st.dataframe(filtered_patron.reset_index(drop=True))

        # --- Archivero Visualization (Simplified Text-based) ---
        st.subheader('Ubicación del Archivo:')
        location_str = filtered_patron['UBICACIÓN DE ARCHIVO'].iloc[0]
        
        # Function to parse location string
        def parse_location(location_string):
            cabinet_match = re.search(r'ARCHIVERO (\d+)', location_string, re.IGNORECASE)
            fila_match = re.search(r'FILA (\d+)', location_string, re.IGNORECASE)
            seccion_match = re.search(r'SECCIÓN ([A-G])', location_string, re.IGNORECASE)
            
            cabinet = int(cabinet_match.group(1)) if cabinet_match else None
            fila = int(fila_match.group(1)) if fila_match else None
            seccion = seccion_match.group(1).upper() if seccion_match else None
            
            return cabinet, fila, seccion

        cabinet, fila, seccion = parse_location(location_str)

        if cabinet and fila and seccion:
            st.write(f"El archivo se encuentra en el **Archivero {cabinet}, Fila {fila}, Sección {seccion}**.")
            
            st.markdown("### Representación del Archivero:")
            # Simple text-based representation
            for c in range(1, 6): # 5 Archiveros
                st.markdown(f"#### Archivero {c}")
                for r in range(1, 8): # 7 Filas
                    row_display = []
                    for s_char in ['A', 'B', 'C', 'D', 'E', 'F', 'G']: # Columns A-G
                        if c == cabinet and r == fila and s_char == seccion:
                            row_display.append(f"**`[{s_char}]`**") # Highlighted
                        else:
                            row_display.append(f"` {s_char} `")
                    st.markdown(" &nbsp; ".join(row_display))
                st.markdown("--- ")
        else:
            st.warning(f"No se pudo parsear la ubicación del archivo: {location_str}")
    else:
        st.warning('No se encontró ningún patrón con ese Registro Patronal.')

st.markdown('---')

# --- Tabs for Analysis ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Estatus Patronal", 
    "Motivos de Baja", 
    "Actividades Económicas", 
    "Primas de Riesgo", 
    "Trabajadores por Actividad", 
    "Movimientos Afiliatorios"
])

with tab1:
    st.header("ESTATUS PATRONAL SECCIÓN NORTE")
    # Pie chart for 'ESTATUS'
    estatus_counts = df['ESTATUS'].value_counts()
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    ax1.pie(estatus_counts, labels=estatus_counts.index, autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#FFC107'])
    ax1.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)
    st.markdown(
        """
        <div style='background-color: #E0E7FF; padding: 15px; border-radius: 5px;'>
        Esta gráfica de pastel muestra la distribución porcentual de los patrones 
        dados de **ALTA** y **BAJA** en la sección. Es un indicador clave para 
        entender la dinámica de crecimiento y contracción de la base patronal. 
        Un porcentaje alto de patrones 'ALTA' indica un ambiente económico 
        activo y saludable en términos de nuevas empresas y empleos.
        </div>
        """, unsafe_allow_html=True
    )

with tab2:
    st.header("PRINCIPALES MOTIVOS DE BAJA PATRONAL")
    # Filter for 'BAJA' status and count motives
    baja_motivos = df[df['ESTATUS'] == 'BAJA']['MOTIVO BAJA'].value_counts()
    if not baja_motivos.empty:
        fig2, ax2 = plt.subplots(figsize=(8, 8))
        ax2.pie(baja_motivos, labels=baja_motivos.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
        ax2.axis('equal')
        st.pyplot(fig2)
        st.markdown(
            """
            <div style='background-color: #E0E7FF; padding: 15px; border-radius: 5px;'>
            Esta gráfica ilustra las razones principales por las cuales los registros patronales son dados de baja. 
            Motivos como **'DOMICILIO NO LOCALIZADO'** o **'SUSPENSIÓN DE ACTIVIDADES'** suelen indicar situaciones 
            en las que el patrón ya no cumple con sus obligaciones fiscales o de seguridad social.
            <br><br>
            Según la Ley del Instituto Mexicano del Seguro Social (IMSS), la baja de un registro patronal 
            puede ocurrir por diversas razones, entre ellas, la falta de localización del domicilio o el impago 
            de cuotas obrero-patronales. Estas situaciones conllevan a que el IMSS inicie procedimientos para 
            regularizar la situación o, en su defecto, dar de baja el registro, afectando la continuidad de la 
            cobertura de seguridad social para los trabajadores y la recaudación de fondos para el sistema.
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.info("No hay datos de patrones con estatus 'BAJA' para analizar los motivos.")

with tab3:
    st.header("PRINCIPALES ACTIVIDADES ECONÓMICAS DE PATRONES EN LA DELEGACIÓN NORTE")
    # Bar chart for 'ACTIVIDAD'
    actividad_counts = df['ACTIVIDAD'].value_counts().head(10) # Top 10 activities
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=actividad_counts.values, y=actividad_counts.index, palette='viridis', ax=ax3)
    ax3.set_title('Top 10 Actividades Económicas')
    ax3.set_xlabel('Número de Patrones')
    ax3.set_ylabel('Actividad Económica')
    st.pyplot(fig3)
    st.markdown(
        """
        <div style='background-color: #E0E7FF; padding: 15px; border-radius: 5px;'>
        Este gráfico de barras muestra las actividades económicas predominantes entre los patrones de la delegación.
        Por ejemplo, el sector de **CONSTRUCCIÓN** engloba a empresas dedicadas a la edificación, 
        infraestructura y desarrollo inmobiliario, siendo un motor importante de empleo. El sector de 
        **SERVICIOS** puede incluir una amplia gama de actividades como consultoría, servicios profesionales, 
        turismo, etc., que son fundamentales para la economía. La **FABRICACIÓN** o **INDUSTRIA MANUFACTURERA** 
        comprende la transformación de materias primas en productos elaborados. 
        <br><br>
        En Yucatán, la diversificación económica ha impulsado sectores como el turismo, la manufactura 
        (especialmente la industria textil y maquiladora), y los servicios, junto con el tradicional sector 
        agropecuario. La construcción también ha experimentado un auge significativo debido al crecimiento 
        urbano y turístico de la región.
        </div>
        """, unsafe_allow_html=True
    )

with tab4:
    st.header("PRIMAS DE RIESGO PATRONALES")
    
    # Calculate change in prima de riesgo
    df['CAMBIO PRIMA DE RIESGO'] = df['PRIMA DE RIESGO ACTUAL'] - df['PRIMA DE RIESGO ANTERIOR']

    st.subheader('10 Patrones con Mayor Aumento en Prima de Riesgo')
    top_increase = df.sort_values(by='CAMBIO PRIMA DE RIESGO', ascending=False).head(10)
    st.dataframe(top_increase[['REGISTRO PATRONAL', 'NOMBRE', 'PRIMA DE RIESGO ANTERIOR', 'PRIMA DE RIESGO ACTUAL', 'CAMBIO PRIMA DE RIESGO']])

    st.subheader('10 Patrones con Mayor Decremento en Prima de Riesgo')
    top_decrease = df.sort_values(by='CAMBIO PRIMA DE RIESGO', ascending=True).head(10)
    st.dataframe(top_decrease[['REGISTRO PATRONAL', 'NOMBRE', 'PRIMA DE RIESGO ANTERIOR', 'PRIMA DE RIESGO ACTUAL', 'CAMBIO PRIMA DE RIESGO']])
    
    # Trend graph (simple comparison)
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='PRIMA DE RIESGO ANTERIOR', y='PRIMA DE RIESGO ACTUAL', data=df, ax=ax4, hue='CAMBIO PRIMA DE RIESGO', size='CAMBIO PRIMA DE RIESGO', sizes=(20, 400), palette='coolwarm')
    ax4.plot([df['PRIMA DE RIESGO ANTERIOR'].min(), df['PRIMA DE RIESGO ANTERIOR'].max()], 
             [df['PRIMA DE RIESGO ANTERIOR'].min(), df['PRIMA DE RIESGO ANTERIOR'].max()], 
             'r--', label='Sin Cambio')
    ax4.set_title('Comparativa de Prima de Riesgo (Anterior vs. Actual)')
    ax4.set_xlabel('Prima de Riesgo Anterior')
    ax4.set_ylabel('Prima de Riesgo Actual')
    ax4.legend()
    st.pyplot(fig4)

    st.markdown(
        """
        <div style='background-color: #E0E7FF; padding: 15px; border-radius: 5px;'>
        Las primas de riesgo patronales son un componente crucial en la determinación de las cuotas 
        que los empleadores deben pagar al IMSS. Representan la probabilidad de ocurrencia de 
        accidentes de trabajo y enfermedades profesionales en una empresa. 
        <br><br>
        **¿Qué es la Prima de Riesgo para el IMSS?**
        Es un porcentaje que se aplica a la base de cotización de los salarios de los trabajadores 
        para calcular las cuotas del seguro de riesgos de trabajo. Su finalidad es financiar las 
        prestaciones en especie y en dinero derivadas de accidentes y enfermedades laborales.
        <br><br>
        **¿De qué depende la asignación de la Prima de Riesgo?**
        Depende de la clase de riesgo de la actividad económica de la empresa y de la siniestralidad 
        registrada en el periodo de revisión. Cada actividad económica tiene una clase de riesgo 
        establecida (de I a V, siendo V la de mayor riesgo). Además, anualmente, las empresas 
        revisan su siniestralidad para determinar si su prima debe ser ajustada.
        <br><br>
        **¿De qué depende que aumente o baje la Prima de Riesgo?**
        *   **Aumento:** Un aumento en la siniestralidad (mayor número de accidentes o enfermedades 
            de trabajo) en el periodo de cómputo resultará en un incremento de la prima. También 
            puede aumentar si la empresa cambia a una actividad económica de mayor riesgo.
        *   **Disminución:** Una reducción en la siniestralidad, es decir, menos accidentes y 
            enfermedades de trabajo, o la implementación de medidas de seguridad que mejoren las 
            condiciones laborales, puede llevar a una disminución de la prima. Cambiar a una 
            actividad de menor riesgo también la reduce.
        <br><br>
        Es fundamental para las empresas gestionar activamente la seguridad y salud en el trabajo 
        para mantener una prima de riesgo baja, lo que se traduce en menores costos y un mejor 
        ambiente laboral.
        </div>
        """, unsafe_allow_html=True
    )

with tab5:
    st.header("TRABAJADORES POR ACTIVIDAD")
    # Relationship between ACTIVIDAD and TRABAJADORES
    avg_workers_by_activity = df.groupby('ACTIVIDAD')['TRABAJADORES'].mean().sort_values(ascending=False)
    
    fig5, ax5 = plt.subplots(figsize=(10, 7))
    sns.barplot(x=avg_workers_by_activity.values, y=avg_workers_by_activity.index, palette='magma', ax=ax5)
    ax5.set_title('Número Promedio de Trabajadores por Actividad Económica')
    ax5.set_xlabel('Promedio de Trabajadores')
    ax5.set_ylabel('Actividad Económica')
    st.pyplot(fig5)

    st.markdown(
        """
        <div style='background-color: #E0E7FF; padding: 15px; border-radius: 5px;'>
        Este análisis relaciona el tipo de actividad económica con el número de trabajadores, 
        mostrando un promedio de empleados por sector. Permite identificar qué actividades 
        son más intensivas en mano de obra. Por ejemplo, sectores como la **CONSTRUCCIÓN** 
        o la **FABRICACIÓN** suelen requerir un mayor número de personal para sus operaciones, 
        lo que los clasifica como sectores intensivos en mano de obra. En contraste, 
        actividades de **CONSULTORÍA** o **SERVICIOS PROFESIONALES** pueden tener un promedio 
        de trabajadores menor, indicando una mayor dependencia de capital humano especializado.
        </div>
        """, unsafe_allow_html=True
    )

with tab6:
    st.header("MOVIMIENTOS AFILIATORIOS")

    st.subheader('Tipos de Movimientos Realizados')
    movimiento_counts = df['TIPO DE MOVIMIENTO'].value_counts()
    fig6a, ax6a = plt.subplots(figsize=(8, 8))
    ax6a.pie(movimiento_counts, labels=movimiento_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("cool"))
    ax6a.axis('equal')
    st.pyplot(fig6a)
    st.markdown(
        """
        <div style='background-color: #E0E7FF; padding: 15px; border-radius: 5px;'>
        Esta gráfica muestra la distribución de los diferentes tipos de movimientos afiliatorios 
        registrados para los patrones. Entender estos movimientos es clave para la gestión 
        administrativa en el IMSS.
        <br><br>
        **Explicación de los movimientos (ejemplos basados en datos comunes del IMSS):**
        *   **ALTA PATRONAL (1):** Este movimiento se registra cuando una persona física o moral 
            se inscribe por primera vez como patrón ante el IMSS, adquiriendo la obligación de 
            afiliar a sus trabajadores y pagar las cuotas obrero-patronales.
        *   **RENOVACIÓN DE TIP (4):** Se refiere a la actualización de la Tarjeta de Identificación 
            Patronal (TIP), un documento que acredita el registro del patrón ante el IMSS.
        *   **BAJA PATRONAL (2):** Indica la cancelación del registro patronal, lo que ocurre cuando 
            la empresa cesa sus actividades o cambia de régimen.
        *   **MODIFICACIÓN DE RAZÓN SOCIAL (3):** Se utiliza cuando el patrón realiza un cambio en 
            su denominación o razón social.
        <br><br>
        Es importante consultar la normativa oficial del IMSS para una descripción detallada y 
        completa de cada tipo de movimiento.
        </div>
        """, unsafe_allow_html=True
    )

    st.subheader('Frecuencia de Movimientos por Año')
    if 'ULTIMO MOVIMIENTO FECHA ULTIMO MOV' in df.columns:
        df['Año Movimiento'] = df['ULTIMO MOVIMIENTO FECHA ULTIMO MOV'].dt.year.astype('Int64') # Use Int64 to handle potential NaNs
        movimientos_por_año = df['Año Movimiento'].value_counts().sort_index()
        if not movimientos_por_año.empty:
            fig6b, ax6b = plt.subplots(figsize=(10, 6))
            sns.lineplot(x=movimientos_por_año.index, y=movimientos_por_año.values, marker='o', ax=ax6b, color='#8E44AD')
            ax6b.set_title('Frecuencia de Movimientos por Año')
            ax6b.set_xlabel('Año')
            ax6b.set_ylabel('Número de Movimientos')
            ax6b.grid(True)
            st.pyplot(fig6b)
            st.markdown(
                """
                <div style='background-color: #E0E7FF; padding: 15px; border-radius: 5px;'>
                Esta gráfica de línea muestra la tendencia en el número de movimientos afiliatorios 
                registrados a lo largo de los años. Puede revelar periodos de mayor actividad 
                administrativa o cambios en la base patronal.
                </div>
                """, unsafe_allow_html=True
            )
        else:
            st.info("No hay datos de 'ULTIMO MOVIMIENTO FECHA ULTIMO MOV' para analizar la frecuencia por año.")
    else:
        st.warning("La columna 'ULTIMO MOVIMIENTO FECHA ULTIMO MOV' no se encuentra en el DataFrame.")

    st.subheader('Medio de Realización de Movimientos')
    medio_counts = df['MEDIO'].value_counts()
    fig6c, ax6c = plt.subplots(figsize=(8, 8))
    ax6c.pie(medio_counts, labels=medio_counts.index, autopct='%1.1f%%', startangle=90, colors=['#3498DB', '#E74C3C'])
    ax6c.axis('equal')
    st.pyplot(fig6c)
    st.markdown(
        """
        <div style='background-color: #E0E7FF; padding: 15px; border-radius: 5px;'>
        Esta gráfica de pastel compara la proporción de movimientos realizados a través de 
        **INTERNET** frente a los realizados en **VENTANILLA**.
        <br><br>
        El Instituto Mexicano del Seguro Social (IMSS) ha estado impulsando activamente la 
        digitalización de sus trámites para facilitar a los patrones el cumplimiento de 
        sus obligaciones. La opción de realizar movimientos a través de INTERNET busca 
        optimizar tiempos, reducir la necesidad de traslados a las subdelegaciones y mejorar 
        la eficiencia administrativa. Esta tendencia forma parte de una estrategia más 
        amplia para modernizar los servicios y acercarlos a los usuarios, fomentando una 
        mayor adopción de las plataformas digitales para todos los trámites disponibles.
        </div>
        """, unsafe_allow_html=True
    )
