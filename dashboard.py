from pandas import json_normalize
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.header("DASHBOARD")
st.sidebar.header("ESTADISTICA DE EDUCACION EN COLOMBIA POR DEPARTAMENTO")
st.sidebar.markdown("---")
st.markdown("# APARTADO DE GRAFICAS Y TABLAS")

servidor = 'http://ec2-44-198-126-182.compute-1.amazonaws.com'

@st.cache
def cargar_datos():
    response = requests.get(servidor + '/datos')
    info = json.loads(response.text)    
    datos = json_normalize(info)
    return datos

def get_desersion_transicion():
    response = requests.get(servidor + '/desercion_transicion')
    info = json.loads(response.text)    
    datos = json_normalize(info)
    return datos

def get_desersion_primaria():
    response = requests.get(servidor + '/desercion_primaria')
    info = json.loads(response.text)    
    datos = json_normalize(info)
    return datos

def get_desersion_secundaria():
    response = requests.get(servidor + '/desercion_secundaria')
    info = json.loads(response.text)    
    datos = json_normalize(info)
    return datos

def get_desersion_media():
    response = requests.get(servidor + '/desercion_media')
    info = json.loads(response.text)    
    datos = json_normalize(info)
    return datos

def get_participacion():
    response = requests.get(servidor + '/participacion')
    info = json.loads(response.text)    
    info = json.dumps(info)
    datos = pd.read_json(info, orient='index')
    return datos

def get_cobertura():
    response = requests.get(servidor + '/cobertura')
    info = json.loads(response.text)    
    info = json.dumps(info)
    datos = pd.read_json(info, orient='index')
    return datos

def get_conectadas():
    response = requests.get(servidor + '/sedes_conectadas')
    info = json.loads(response.text)    
    datos = json_normalize(info)
    return datos

datos = cargar_datos()
participacion = get_participacion()
cobertura = get_cobertura()
radio_button = st.sidebar.radio(
    label="Tabla de datos", options=["Mostrar", "No mostrar"]
)

if radio_button == "Mostrar":
    st.dataframe(datos)


datos_agrupados_departamento_dt = get_desersion_transicion()
datos_agrupados_departamento_dt[['DESERCIÓN_TRANSICIÓN']] = datos_agrupados_departamento_dt[['DESERCIÓN_TRANSICIÓN']].astype(float)
datos_agrupados_departamento_dt[['AÑO']] = datos_agrupados_departamento_dt[['AÑO']].astype(int)

datos_agrupados_departamento_dp = get_desersion_primaria()
datos_agrupados_departamento_dp[['DESERCIÓN_PRIMARIA']] = datos_agrupados_departamento_dp[['DESERCIÓN_PRIMARIA']].astype(float)
datos_agrupados_departamento_dp[['AÑO']] = datos_agrupados_departamento_dp[['AÑO']].astype(int)

datos_agrupados_departamento_ds = get_desersion_secundaria()
datos_agrupados_departamento_ds[['DESERCIÓN_SECUNDARIA']] = datos_agrupados_departamento_ds[['DESERCIÓN_SECUNDARIA']].astype(float)
datos_agrupados_departamento_ds[['AÑO']] = datos_agrupados_departamento_ds[['AÑO']].astype(int)

datos_agrupados_departamento_dm = get_desersion_media()
datos_agrupados_departamento_dm[['DESERCIÓN_MEDIA']] = datos_agrupados_departamento_dm[['DESERCIÓN_MEDIA']].astype(float)
datos_agrupados_departamento_dm[['AÑO']] = datos_agrupados_departamento_dm[['AÑO']].astype(int)

sedes_conectadas = get_conectadas()
sedes_conectadas[['SEDES_CONECTADAS_A_INTERNET']] = sedes_conectadas[['SEDES_CONECTADAS_A_INTERNET']].astype(float)
sedes_conectadas[['SEDES_CONECTADAS_A_INTERNET']] = round(sedes_conectadas[['SEDES_CONECTADAS_A_INTERNET']], 2)


lista_departamentos = requests.get(servidor + '/departamentos')
lista_departamentos = json.loads(lista_departamentos.text)

opcion_departamento = st.sidebar.selectbox(
    label="Seleccione un departamento", options=lista_departamentos
)

opciones = ["Desercion por niveles de educacion",
            "Comparacion entre cobertura neta y T.de matriculacion", 
            "Evolución de cobertura neta y tasa de matriculación",
            "Sedes conectadas a internet por departamento"]

radio_button_grafica = st.sidebar.radio(
    label="Ver graficas", options=opciones
)

st.markdown("---")

def plot_dp(df, x, y,departamento):
    data = df.copy()   
    data = data[data["DEPARTAMENTO"] == departamento]
    fig = px.line(data, x=x, y=y, title="DESERCION PRIMARIA EN "+departamento.upper())
    fig.update_traces(line_color='#f4a582')
    return fig, data

def plot_dt(df, x, y,departamento):
    data = df.copy()   
    data = data[data["DEPARTAMENTO"] == departamento]
    fig = px.line(data, x=x, y=y, title="DESERCION TRANSICION EN "+departamento.upper())
    fig.update_traces(line_color='#f4a582')
    return fig, data

def plot_ds(df, x, y,departamento):
    data = df.copy()   
    data = data[data["DEPARTAMENTO"] == departamento]
    fig = px.line(data, x=x, y=y, title="DESERCION SECUNDARIA EN "+departamento.upper())
    fig.update_traces(line_color='#f4a582')
    return fig, data

def plot_dm(df, x, y,departamento):
    data = df.copy()   
    data = data[data["DEPARTAMENTO"] == departamento]
    fig = px.line(data, x=x, y=y, title="DESERCION MEDIA EN "+departamento.upper())
    fig.update_traces(line_color='#f4a582')
    return fig, data

if radio_button_grafica == opciones[0]:
    plot1, d = plot_dt(datos_agrupados_departamento_dt, "AÑO", "DESERCIÓN_TRANSICIÓN", opcion_departamento)
    plot2, d = plot_dp(datos_agrupados_departamento_dp, "AÑO", "DESERCIÓN_PRIMARIA", opcion_departamento)
    colum1,colum2 =st.columns(2)
    colum1.plotly_chart(plot1, use_container_width=True)
    colum2.plotly_chart(plot2, use_container_width=True)

    st.markdown("---")

    plot3, d = plot_ds(datos_agrupados_departamento_ds, "AÑO", "DESERCIÓN_SECUNDARIA", opcion_departamento)
    plot4, d = plot_dm(datos_agrupados_departamento_dm, "AÑO", "DESERCIÓN_MEDIA", opcion_departamento)
    colum3,colum4 =st.columns(2)
    colum3.plotly_chart(plot3, use_container_width=True)
    colum4.plotly_chart(plot4, use_container_width=True)

    st.markdown("---")
    st.write("""Desercion: Puede entenderse como el abandono del sistema escolar 
                por parte de los estudiantes, provocado por la combinación de factores que se 
                generan tanto al interior del sistema como en contextos de tipo social, familiar, individual y del entorno. 
                La tasa de deserción intra-anual solo tiene en cuenta a los alumnos que abandonan la escuela durante el año escolar, ésta se complementa con la tasa de deserción interanual que calcula aquellos que desertan al terminar el año escolar.
                """)

elif radio_button_grafica == opciones[1]:


    Figura1 = go.Figure()
    MyColors = ["#d1e5f0", "#f7f7f7", "#fddbc7", "#f4a582", "#d6604d", "#b2182b", "#67001f"]
    Temp = participacion.transpose()
    for i, color in zip(Temp.columns, MyColors):
        Figura1.add_bar(x = Temp.index, y = Temp[i], marker_color = color, name = i)

    Figura1.update_layout(
        # Usando una tema por defecto (https://plotly.com/python/templates/)
        template = "plotly_dark",
        # Personalización de Títulos
        title_text = "COMPARACION ENTRE COBERTURA NETA Y TASA DE MATRICULACION/DEPARTAMENTOS",
        # Personalización de Ejes
        xaxis = dict(
            tickmode = "array",
            tickvals = [0, 1, 2],
            ticktext = ["Cobertura Neta","Tasa de Matriculación"]
        )
    )    
    Figura1.update_xaxes(
        title_text = "Variable",
        #title_font = dict(size = 20, family = "Balto", color = "#28F618"),
        # Tickes
        tickangle = 0,
        tickfont = dict(size = 16, family = "Overpass", color = "#FFFFFF"),
        # Línea Base
        showline = True, linewidth = 2, linecolor = "#FFFFFF",
    )
    Figura1.update_yaxes(
        tickformat = "%",    
        tickfont = dict(size = 16, family = "Overpass", color = "#FFFFFF"),
        showline = True, linewidth = 2, linecolor = "#FFFFFF", mirror = True
    )
    st.plotly_chart(Figura1, use_container_width=True)

    st.markdown("---")

    st.write("""Covertura neta: Cantidad o porcentaje de estudiantes matriculados en el sistema educativo; 
                sin contar los que están en extraedad (por encima de la edad correspondiente para cada grado).               
            """)

    st.write("""Tasa de matriculacion: Número de alumnos en las edades normativas inscritos para cursar el nivel
                o tipo educativo del que se trate, respecto a la población de la misma edad, expresado en porcentaje.  
            """)

elif radio_button_grafica == opciones[2]:
    Figura3 = go.Figure()
    Figura3.add_scatter(
        x = cobertura["Cobertura Neta"].index,y=cobertura["Cobertura Neta"],
            mode = "lines", line =  dict(color = "#b2182b", width = 3),
            name = "Cobertura Neta", showlegend = True
    )
    Figura3.add_scatter(
        x = cobertura["Tasa de Matriculación"].index, y = cobertura["Tasa de Matriculación"],
            mode = "lines", line = dict(color = "#d1e5f0", width = 3),
            name = "Tasa de Matriculación", showlegend = True
    )

    Figura3.update_traces(mode = "markers+lines", hovertemplate = None)
    Figura3.update_layout(
        template = "simple_white",
        hovermode = "x", # (https://plotly.com/python/hover-text-and-formatting/)
        title_text = "EVOLUCIÓN HISTÓRICA DE LA COBERTURA NETA Y LA TASA DE MATRICULACIÓN<BR>EN PROMEDIO DE 2011 A 2020",
        legend = dict(orientation = "h", yanchor = "bottom", y = 1.02, xanchor = "right", x = 1)
    )    
    Figura3.update_xaxes(
        title_text = "Año",
        title_font = dict(size = 20, family = "Rockwell"),
        # Línea Base
        showline = True, linewidth = 2, linecolor = "#FFFFFF",
    )
    Figura3.update_yaxes(
        title_text = "Tasa (%)",
        title_font = dict(size = 20, family = "Rockwell"),
        # Línea Base
        showline = True, linewidth = 2, linecolor = "#FFFFFF"
    )
    st.plotly_chart(Figura3, use_container_width=True)

    st.markdown("---")
    st.write("""Covertura neta: Cantidad o porcentaje de estudiantes matriculados en el sistema educativo; 
                sin contar los que están en extraedad (por encima de la edad correspondiente para cada grado).               
            """)

    st.write("""Tasa de matriculacion: Número de alumnos en las edades normativas inscritos para cursar el nivel
                o tipo educativo del que se trate, respecto a la población de la misma edad, expresado en porcentaje.  
            """)
elif radio_button_grafica == opciones[3]:

    Figura4 = px.pie(sedes_conectadas, values="SEDES_CONECTADAS_A_INTERNET", names="DEPARTAMENTO", 
                color_discrete_sequence=px.colors.sequential.RdBu,
                opacity=1, hole=0.3, title="PORCENTAJE DE SEDES CONECTADAS A INTERNET POR DEPARTAMENTO")
    Figura4.update_traces(textinfo="value")
    st.plotly_chart(Figura4, use_container_width=True)
    st.markdown("---")




