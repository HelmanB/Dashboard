import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.header("DASHBOARD")
st.sidebar.header("ESTADISTICA DE EDUCACION POR MUNICIPIO")
st.sidebar.markdown("---")
st.markdown("# APARTADO DE GRAFICAS Y TABLAS")



@st.cache
def cargar_datos(filename: str):
    return pd.read_csv(filename)


datos = cargar_datos("datos.csv")


#ACCION DEL BOTON
# if cargo_datos:
#     st.write("Estoy cargando datos (pero no)")


datos_agrupados_departamento = datos.groupby(["DEPARTAMENTO"]).mean().reset_index().copy()
datos_agrupados_año = datos.groupby(["AÑO"]).mean().reset_index().copy()
datos_agrupados_departamento_dt = datos.groupby(["AÑO","DEPARTAMENTO"])['DESERCIÓN_TRANSICIÓN'].mean().reset_index().copy()
datos_agrupados_departamento_dp = datos.groupby(["AÑO","DEPARTAMENTO"])['DESERCIÓN_PRIMARIA'].mean().reset_index().copy()
datos_agrupados_departamento_ds = datos.groupby(["AÑO","DEPARTAMENTO"])['DESERCIÓN_SECUNDARIA'].mean().reset_index().copy()
datos_agrupados_departamento_dm = datos.groupby(["AÑO","DEPARTAMENTO"])['DESERCIÓN_MEDIA'].mean().reset_index().copy()


st.dataframe(datos)

lista_departamentos = list(datos_agrupados_departamento["DEPARTAMENTO"].unique())
lista_anios = list(datos_agrupados_año["AÑO"].unique())
# st.write((lista_departamentos))
opcion_departamento = st.sidebar.selectbox(
    label="Seleccione un departamento", options=lista_departamentos
)

# opcion_anio = st.sidebar.selectbox(
#     label="Seleccione un un año", options=lista_anios
# )
st.markdown("---")
# st.dataframe(datos_agrupados_departamento[datos_agrupados_departamento["DEPARTAMENTO"] == opcion_departamento])

otras_variables = list(datos.columns)
otras_variables.pop(otras_variables.index("DEPARTAMENTO"))
otras_variables.pop(otras_variables.index("AÑO"))
# opcion_y = st.sidebar.selectbox(
#     label="Seleccione una variable", options=otras_variables
# )


# @st.cache
# def plot_simple(df, x, y, sales_filter):
#     data = df.copy()
#     data = data[data["DEPARTAMENTO"] == sales_filter]
#     fig = px.line(data, x=x, y=y)
#     return fig, data

# plot, d = plot_simple(datos, "DEPARTAMENTO", opcion_y, opcion_departamento)
# st.plotly_chart(plot)
# st.write(d)

# @st.cache
# def plot_anio(df, x, y, año):
#     data = df.copy()
#     data = data[data["AÑO"] == año]
#     fig = px.line(data, x=x, y=y)
#     return fig, data

# plot, d = plot_anio(datos, opcion_y, "AÑO", opcion_anio)
# st.plotly_chart(plot)
# st.write(d)
@st.cache
def plot_dp(df, x, y,departamento):
    data = df.copy()   
    data = data[data["DEPARTAMENTO"] == departamento]
    fig = px.line(data, x=x, y=y, title="MEDIA DE DESERCION EN PRIMARIA EN "+departamento.upper())
    return fig, data

@st.cache
def plot_dt(df, x, y,departamento):
    data = df.copy()   
    data = data[data["DEPARTAMENTO"] == departamento]
    fig = px.line(data, x=x, y=y, title="MEDIA DE DESERCION EN TRANSICION EN "+departamento.upper())
    return fig, data

plot1, d = plot_dt(datos_agrupados_departamento_dt, "AÑO", "DESERCIÓN_TRANSICIÓN", opcion_departamento)
plot2, d = plot_dp(datos_agrupados_departamento_dp, "AÑO", "DESERCIÓN_PRIMARIA", opcion_departamento)
colum1,colum2 =st.columns(2)
colum1.plotly_chart(plot1, use_container_width=True)
colum2.plotly_chart(plot2, use_container_width=True)
st.write(d)

st.markdown("---")







st.markdown("---")

@st.cache
def plot_ds(df, x, y,departamento):
    data = df.copy()   
    data = data[data["DEPARTAMENTO"] == departamento]
    fig = px.line(data, x=x, y=y, title="MEDIA DE DESERCION EN SECUNDARIA EN "+departamento.upper())
    return fig, data

plot, d = plot_ds(datos_agrupados_departamento_ds, "AÑO", "DESERCIÓN_SECUNDARIA", opcion_departamento)
st.plotly_chart(plot)
st.write(d)

st.markdown("---")

@st.cache
def plot_dm(df, x, y,departamento):
    data = df.copy()   
    data = data[data["DEPARTAMENTO"] == departamento]
    fig = px.line(data, x=x, y=y, title="MEDIA DE LA DESERCION MEDIA EN "+departamento.upper())
    return fig, data

plot, d = plot_dm(datos_agrupados_departamento_dm, "AÑO", "DESERCIÓN_MEDIA", opcion_departamento)
st.plotly_chart(plot)
st.write(d)


