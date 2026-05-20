import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    # Set page configuration for a formal, executive style
    st.set_page_config(
        page_title="DEPARTAMENTO DE AFILIACIÓN Y VIGENCIA SUB DELEGACIÓN 33 LA CEIBA",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for formal and executive style
    st.markdown(
        """
        <style>
        .reportview-container {
            background: #f0f2f6; /* Light gray background */
        }
        .sidebar .sidebar-content {
            background: #ffffff; /* White sidebar */
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50; /* Dark blue-gray for headers */
        }
        .stButton>button {
            background-color: #3498db; /* Blue button */
            color: white;
        }
        .stTextInput>div>div>input {
            border-radius: 5px;
            border: 1px solid #ccc;
            padding: 10px;
        }
        /* Custom background and formal font for the whole app */
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f0f2f6;
        }
        .main .block-container {
            padding-top: 2rem;
            padding-right: 2rem;
            padding-left: 2rem;
            padding-bottom: 2rem;
        }
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size: 1.2rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("DEPARTAMENTO DE AFILIACIÓN Y VIGENCIA SUB DELEGACIÓN 33 LA CEIBA")

    # Load the data
    file_path = 'DATOS/PATRONES PROYECTO FINAL.xlsx'
    df = pd.read_excel(file_path)

    # --- Data Preprocessing ---
    # Ensure 'REGISTRO PATRONAL' is string for consistent search
    df['REGISTRO PATRONAL'] = df['REGISTRO PATRONAL'].astype(str)
    # Convert date column to datetime
    df['FECHA ULTIMO MOV'] = pd.to_datetime(df['FECHA ULTIMO MOV'], errors='coerce')
    # Ensure numeric columns are actually numeric
    numeric_cols = ['TRABAJADORES', 'PRIMA DE RIESGO ANTERIOR', 'PRIMA DE RIESGO ACTUAL']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')


    st.write("---  \n### Búsqueda de Patrones \n---")
    search_term = st.text_input("Introduce el Registro Patronal para buscar:", key="search_box")

    if search_term:
        # Filter DataFrame based on search term
        filtered_df = df[df['REGISTRO PATRONAL'].str.contains(search_term, case=False, na=False)]
        
        if not filtered_df.empty:
            st.success(f"Resultados para Registro Patronal: **{search_term}**")
            for index, row in filtered_df.iterrows():
                st.json(row.to_dict())
                st.markdown(f"### **Ubicación del Archivo:** :blue[{row['UBICACIÓN DE ARCHIVO']}]")
                st.write("---")
        else:
            st.warning(f"No se encontraron resultados para el Registro Patronal: {search_term}")

    st.markdown("\n---  \n## Gráficos Ilustrativos \n---")
    
    # Create tabs
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
        estatus_counts = df['ESTATUS'].value_counts()

        fig1, ax1 = plt.subplots(figsize=(8, 8))
        ax1.pie(estatus_counts, labels=estatus_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Porcentaje de Patrones por Estatus (Alta/Baja)')
        st.pyplot(fig1)
        plt.close(fig1)

        st.markdown(
            """
            Esta gráfica de pastel muestra la distribución porcentual de los patrones clasificados por su estatus: 'ALTA' (activos) y 'BAJA' (inactivos). 
            Es una métrica crucial para entender la dinámica del padrón de afiliados del IMSS en la sección norte. 
            Un alto porcentaje de 'ALTA' indica crecimiento o estabilidad, mientras que un porcentaje significativo de 'BAJA' podría señalar desafíos 
            económicos o cambios en el mercado laboral que afectan la formalidad del empleo.
            """
        )

    with tab2:
        st.header("PRINCIPALES MOTIVOS DE BAJA PATRONAL")
        baja_df = df[df['ESTATUS'] == 'BAJA']
        motivo_baja_counts = baja_df['MOTIVO BAJA'].value_counts().head(5) # Top 5 motivos

        if not motivo_baja_counts.empty:
            fig2, ax2 = plt.subplots(figsize=(8, 8))
            ax2.pie(motivo_baja_counts, labels=motivo_baja_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('viridis'))
            ax2.axis('equal')
            plt.title('Principales Motivos de Baja Patronal')
            st.pyplot(fig2)
            plt.close(fig2)

            st.markdown(
                """
                Esta gráfica ilustra los principales motivos por los cuales los patrones son dados de baja en el sistema del IMSS. 
                Entre los motivos más comunes, 'DOMICILIO NO LOCALIZADO' es significativo. Según la Ley del Seguro Social, 
                un patrón puede ser dado de baja si el IMSS no puede verificar su domicilio, lo que dificulta la comunicación 
                y el cumplimiento de sus obligaciones. Otro motivo importante es el 'INPAGO DE SUS OBLIGACIONES', que se refiere al 
                incumplimiento en el pago de las cuotas obrero-patronales, lo que conlleva a sanciones y, eventualmente, a la baja del registro.
                Estos motivos reflejan desafíos en la fiscalización y en la disciplina de pago de los contribuyentes.
                """
            )
        else:
            st.info("No hay datos de patrones dados de baja para analizar los motivos.")

    with tab3:
        st.header("PRINCIPALES ACTIVIDADES ECONOMICAS DE PATRONES EN LA DELEGACIÓN NORTE")
        actividad_counts = df['ACTIVIDAD'].value_counts().head(10)

        fig3, ax3 = plt.subplots(figsize=(10, 6))
        sns.barplot(x=actividad_counts.index, y=actividad_counts.values, palette='mako', ax=ax3)
        ax3.set_title('Top 10 Actividades Económicas de Patrones')
        ax3.set_xlabel('Actividad Económica')
        ax3.set_ylabel('Número de Patrones')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close(fig3)

        st.markdown(
            """
            Esta gráfica de barras muestra las principales actividades económicas en las que se desempeñan los patrones afiliados en la delegación norte.
            Por ejemplo:
            *   **CONSTRUCCIÓN:** Este sector abarca desde la edificación de viviendas y edificios comerciales hasta obras de infraestructura, siendo un motor importante de empleo.
            *   **FABRICACIÓN:** Incluye la transformación de materias primas en productos elaborados, desde alimentos hasta maquinaria, contribuyendo significativamente a la producción industrial.
            *   **COMERCIO:** Comprende todas las actividades de compra y venta de bienes, tanto al por mayor como al por menor, vital para la distribución de productos.
            *   **SERVICIOS:** Este amplio grupo incluye actividades destinadas a brindar un tipo de servicio para satisfacer necesidades diversas, como consultoría, educación, salud, turismo, etc., generando un gran número de puestos de trabajo indirectos y directos.

            **Información estadística de Yucatán:** Yucatán ha experimentado un crecimiento notable en sectores como el turismo, la manufactura y la logística. La diversidad de actividades aquí mostradas refleja la composición económica de la región, que busca la diversificación para fortalecer su desarrollo económico.
            """
        )

    with tab4:
        st.header("PRIMAS DE RIESGO PATRONALES")
        
        # Drop rows with NaN in risk premium columns to ensure calculations are accurate
        df_primas = df.dropna(subset=['PRIMA DE RIESGO ANTERIOR', 'PRIMA DE RIESGO ACTUAL']).copy()
        df_primas['CAMBIO DE PRIMA'] = df_primas['PRIMA DE RIESGO ACTUAL'] - df_primas['PRIMA DE RIESGO ANTERIOR']

        st.subheader("10 Patrones con Mayor Aumento en Primas de Riesgo")
        top_increase = df_primas.sort_values(by='CAMBIO DE PRIMA', ascending=False).head(10)
        st.dataframe(top_increase[['NOMBRE', 'REGISTRO PATRONAL', 'ACTIVIDAD', 'PRIMA DE RIESGO ANTERIOR', 'PRIMA DE RIESGO ACTUAL', 'CAMBIO DE PRIMA']])

        st.subheader("10 Patrones con Mayor Decremento en Primas de Riesgo")
        top_decrease = df_primas.sort_values(by='CAMBIO DE PRIMA', ascending=True).head(10)
        st.dataframe(top_decrease[['NOMBRE', 'REGISTRO PATRONAL', 'ACTIVIDAD', 'PRIMA DE RIESGO ANTERIOR', 'PRIMA DE RIESGO ACTUAL', 'CAMBIO DE PRIMA']])

        st.subheader("Tendencia de Primas de Riesgo (Anterior vs. Actual)")
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        sns.scatterplot(x='PRIMA DE RIESGO ANTERIOR', y='PRIMA DE RIESGO ACTUAL', data=df_primas, alpha=0.6, ax=ax4)
        ax4.plot([df_primas['PRIMA DE RIESGO ANTERIOR'].min(), df_primas['PRIMA DE RIESGO ANTERIOR'].max()], 
                 [df_primas['PRIMA DE RIESGO ANTERIOR'].min(), df_primas['PRIMA DE RIESGO ANTERIOR'].max()], 
                 'r--', label='Sin cambio')
        ax4.set_title('Comparación de Prima de Riesgo Anterior vs. Actual')
        ax4.set_xlabel('Prima de Riesgo Anterior')
        ax4.set_ylabel('Prima de Riesgo Actual')
        ax4.legend()
        plt.tight_layout()
        st.pyplot(fig4)
        plt.close(fig4)

        st.markdown(
            """
            Esta sección analiza la evolución de las primas de riesgo de los patrones. Hemos identificado los 10 patrones con el mayor aumento y los 10 con el mayor decremento en sus primas, 
            lo que puede indicar cambios significativos en su siniestralidad o en su clasificación de actividad económica. 
            La gráfica de dispersión compara la prima de riesgo anterior con la actual, mostrando la tendencia general: los puntos por encima de la línea roja 
            indican un aumento en la prima, mientras que los que están por debajo sugieren una disminución.

            ### ¿Qué es una Prima de Riesgo para el IMSS?
            La prima de riesgo de trabajo es un porcentaje que cada empresa paga al Instituto Mexicano del Seguro Social (IMSS) 
            para cubrir las prestaciones en especie y en dinero derivadas de los accidentes y enfermedades de trabajo. 
            Esta prima se calcula anualmente y se ajusta según la siniestralidad de la empresa.

            ### ¿De qué depende la asignación de la Prima de Riesgo?
            La asignación inicial de la prima de riesgo depende de la clasificación de la actividad económica de la empresa, 
            establecida en el Catálogo de Actividades para la Clasificación de Empresas del IMSS. Esta clasificación se basa en 
            el grado de riesgo inherente a cada tipo de trabajo.

            ### ¿De qué depende que aumente o baje la Prima de Riesgo?
            La prima de riesgo se revisa anualmente y puede aumentar o disminuir dependiendo de la siniestralidad de la empresa 
            durante el periodo de revisión. Si una empresa registra más accidentes o enfermedades de trabajo, su prima tiende a subir. 
            Por el contrario, si implementa medidas de seguridad y salud en el trabajo que resultan en una menor siniestralidad, 
            su prima puede disminuir. El objetivo es incentivar la prevención de riesgos laborales.
            """
        )

    with tab5:
        st.header("TRABAJADORES POR ACTIVIDAD")
        
        trabajadores_por_actividad = df.groupby('ACTIVIDAD')['TRABAJADORES'].sum().sort_values(ascending=False).head(10)
        promedio_trabajadores_por_actividad = df.groupby('ACTIVIDAD')['TRABAJADORES'].mean().sort_values(ascending=False).head(10)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Número Total de Trabajadores por Actividad")
            fig5_1, ax5_1 = plt.subplots(figsize=(10, 6))
            sns.barplot(x=trabajadores_por_actividad.index, y=trabajadores_por_actividad.values, palette='rocket', ax=ax5_1)
            ax5_1.set_xlabel('Actividad')
            ax5_1.set_ylabel('Total de Trabajadores')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig5_1)
            plt.close(fig5_1)

        with col2:
            st.subheader("Promedio de Trabajadores por Patrón en la Actividad")
            fig5_2, ax5_2 = plt.subplots(figsize=(10, 6))
            sns.barplot(x=promedio_trabajadores_por_actividad.index, y=promedio_trabajadores_por_actividad.values, palette='magma', ax=ax5_2)
            ax5_2.set_xlabel('Actividad')
            ax5_2.set_ylabel('Promedio de Trabajadores')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig5_2)
            plt.close(fig5_2)

        st.markdown(
            """
            Esta sección analiza la relación entre el tipo de actividad económica y el número de trabajadores. 
            La primera gráfica muestra el **número total de trabajadores** agrupados por actividad, identificando 
            los sectores que más empleo generan en la región. La segunda gráfica presenta el **promedio de trabajadores por patrón** 
            en cada actividad, lo que nos permite inferir qué sectores son más intensivos en mano de obra. 
            Por ejemplo, una actividad con un alto promedio de trabajadores por patrón podría indicar que las empresas en ese sector 
            son, en general, de mayor tamaño o requieren una gran cantidad de personal para su operación, como la construcción 
            o ciertas manufacturas.
            """
        )

    with tab6:
        st.header("MOVIMIENTOS AFILIATORIOS")

        # Gráfica de tipos de movimiento
        movimiento_counts = df['TIPO DE MOVIMIENTO'].value_counts()
        fig6_1, ax6_1 = plt.subplots(figsize=(10, 6))
        sns.barplot(x=movimiento_counts.index, y=movimiento_counts.values, palette='cubehelix', ax=ax6_1)
        ax6_1.set_title('Frecuencia de Tipos de Movimientos Afiliatorios')
        ax6_1.set_xlabel('Tipo de Movimiento')
        ax6_1.set_ylabel('Frecuencia')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig6_1)
        plt.close(fig6_1)

        st.markdown(
            """
            Esta gráfica muestra la frecuencia de los diferentes tipos de movimientos afiliatorios registrados en el DataFrame. 
            Los tipos de movimiento más comunes pueden dar una idea de la actividad administrativa predominante en el IMSS. 
            A continuación, una breve explicación de los movimientos que aparecen en el dataset:
            *   **ALTA PATRONAL:** Se refiere al registro inicial de una empresa o patrón ante el IMSS para dar de alta su obligación de seguridad social.
            *   **RENOVACIÓN DE TIP:** Corresponde a la actualización o renovación de la Tarjeta de Identificación Patronal (TIP), un documento esencial para el patrón.
            *   **BAJA PATRONAL:** Es el proceso por el cual un patrón deja de tener obligaciones con el IMSS, ya sea por cese de actividades, fusión, etc.
            """
        )

        # Gráfica de frecuencia de movimientos por año
        df_with_date = df.dropna(subset=['FECHA ULTIMO MOV'])
        if not df_with_date.empty:
            movimientos_por_año = df_with_date['FECHA ULTIMO MOV'].dt.year.value_counts().sort_index()
            fig6_2, ax6_2 = plt.subplots(figsize=(10, 6))
            sns.lineplot(x=movimientos_por_año.index, y=movimientos_por_año.values, marker='o', ax=ax6_2)
            ax6_2.set_title('Frecuencia de Movimientos Afiliatorios por Año')
            ax6_2.set_xlabel('Año')
            ax6_2.set_ylabel('Número de Movimientos')
            ax6_2.set_xticks(movimientos_por_año.index)
            plt.grid(True)
            plt.tight_layout()
            st.pyplot(fig6_2)
            plt.close(fig6_2)

            st.markdown(
                """
                Esta gráfica de línea muestra cómo ha variado la cantidad de movimientos afiliatorios a lo largo de los años. 
                Una tendencia ascendente podría indicar un aumento en la actividad económica o en la formalización de empresas, 
                mientras que una descendente podría señalar lo contrario o una mayor eficiencia en los procesos.
                """
            )
        else:
            st.info("No hay datos de fecha para analizar la frecuencia de movimientos por año.")

        # Gráfica de medio de movimientos
        medio_counts = df['MEDIO'].value_counts()
        if not medio_counts.empty:
            fig6_3, ax6_3 = plt.subplots(figsize=(8, 8))
            ax6_3.pie(medio_counts, labels=medio_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('rocket'))
            ax6_3.axis('equal')
            plt.title('Medio Preferente para Realizar Movimientos')
            st.pyplot(fig6_3)
            plt.close(fig6_3)

            st.markdown(
                """
                Esta gráfica de pastel ilustra la proporción de movimientos que se realizan a través de 'INTERNET' versus 'VENTANILLA'. 
                El IMSS ha estado impulsando activamente la digitalización de sus trámites para facilitar a los patrones 
                el cumplimiento de sus obligaciones desde cualquier lugar y en cualquier momento. 
                Un mayor porcentaje de movimientos por internet indica el éxito de estas iniciativas, reduciendo la carga 
                administrativa presencial y mejorando la eficiencia.
                """
            )
        else:
            st.info("No hay datos de medio para analizar los movimientos.")

if __name__ == '__main__':
    main()
