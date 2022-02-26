import pandas as pd

class metodos:     

    def prepararDatos():     
        data = pd.read_csv("datos.csv")
        data.dropna(axis = 0, how = "all", inplace = True) 
        indexDepartamentos = data[data['DEPARTAMENTO']=='Bogotá, D.C.'].index    
        data.drop(indexDepartamentos, inplace=True)
        data = data.astype(str)
        return data.to_dict(orient="records")

    def departamentos():
        data = pd.read_csv("datos.csv")
        data.dropna(axis = 0, how = "all", inplace = True) 
        indexDepartamentos = data[data['DEPARTAMENTO']=='Bogotá, D.C.'].index    
        data.drop(indexDepartamentos, inplace=True)
        datos_agrupados_departamento = data.groupby(["DEPARTAMENTO"]).mean().reset_index().copy()
        indexDepartamentos = datos_agrupados_departamento[
                            (datos_agrupados_departamento['DEPARTAMENTO']=='Archipiélago de San Andrés. Providencia y Santa Catalina') |
                            (datos_agrupados_departamento['DEPARTAMENTO']== 'Bogotá D.C.')
                            ].index
        datos_agrupados_departamento.drop(indexDepartamentos, inplace=True)
        lista_departamentos = list(datos_agrupados_departamento["DEPARTAMENTO"].unique())
        return lista_departamentos


    def desercion_transicion():
        data = pd.read_csv("datos.csv")
        data.dropna(axis = 0, how = "all", inplace = True) 
        indexDepartamentos = data[data['DEPARTAMENTO']=='Bogotá, D.C.'].index    
        data.drop(indexDepartamentos, inplace=True)
        datos_agrupados_departamento_dt = data.groupby(["AÑO","DEPARTAMENTO"])['DESERCIÓN_TRANSICIÓN'].mean().reset_index().copy()
        datos_agrupados_departamento_dt = datos_agrupados_departamento_dt.astype(str)
        return datos_agrupados_departamento_dt.to_dict(orient="records")

    def desercion_primaria():
        data = pd.read_csv("datos.csv")
        data.dropna(axis = 0, how = "all", inplace = True) 
        indexDepartamentos = data[data['DEPARTAMENTO']=='Bogotá, D.C.'].index    
        data.drop(indexDepartamentos, inplace=True)
        datos_agrupados_departamento_dp = data.groupby(["AÑO","DEPARTAMENTO"])['DESERCIÓN_PRIMARIA'].mean().reset_index().copy()
        datos_agrupados_departamento_dp = datos_agrupados_departamento_dp.astype(str)        
        return datos_agrupados_departamento_dp.to_dict(orient="records")

    def desercion_secundaria():
        data = pd.read_csv("datos.csv")
        data.dropna(axis = 0, how = "all", inplace = True) 
        indexDepartamentos = data[data['DEPARTAMENTO']=='Bogotá, D.C.'].index    
        data.drop(indexDepartamentos, inplace=True)
        datos_agrupados_departamento_ds = data.groupby(["AÑO","DEPARTAMENTO"])['DESERCIÓN_SECUNDARIA'].mean().reset_index().copy()
        datos_agrupados_departamento_ds = datos_agrupados_departamento_ds.astype(str)       
        return datos_agrupados_departamento_ds.to_dict(orient="records")

    def desercion_media():
        data = pd.read_csv("datos.csv")
        data.dropna(axis = 0, how = "all", inplace = True) 
        indexDepartamentos = data[data['DEPARTAMENTO']=='Bogotá, D.C.'].index    
        data.drop(indexDepartamentos, inplace=True)
        datos_agrupados_departamento_dm = data.groupby(["AÑO","DEPARTAMENTO"])['DESERCIÓN_MEDIA'].mean().reset_index().copy()
        datos_agrupados_departamento_dm = datos_agrupados_departamento_dm.astype(str)       
        return datos_agrupados_departamento_dm.to_dict(orient="records")

    def cobertura():
        data = pd.read_csv("datos.csv")
        data.dropna(axis = 0, how = "all", inplace = True)
        indexDepartamentos = data[data['DEPARTAMENTO']=='Bogotá, D.C.'].index    
        data.drop(indexDepartamentos, inplace=True) 
        Fechas2 = []
        for i in data["AÑO"]:
            Fechas2.append( str(i)[:4] + "-01" )

        Fechas2 = pd.to_datetime(Fechas2)
        data.set_index(Fechas2, inplace = True)
        data_Cobertura = data["COBERTURA_NETA"].resample("Y").mean()
        data_Matriculacion = data["TASA_MATRICULACIÓN_5_16"].resample("Y").mean()
        Resumen = pd.concat([data_Cobertura, data_Matriculacion], axis = "columns", keys = ["Cobertura Neta", "Tasa de Matriculación"])
        return Resumen
    
    def sedes_conectadas():
        data = pd.read_csv("datos.csv")
        data.dropna(axis = 0, how = "all", inplace = True)
        indexDepartamentos = data[data['DEPARTAMENTO']=='Bogotá, D.C.'].index    
        data.drop(indexDepartamentos, inplace=True) 
        sedes = data.groupby(["DEPARTAMENTO"])['SEDES_CONECTADAS_A_INTERNET'].mean().reset_index().copy()
        sedes = sedes.astype(str)       
        return sedes.to_dict(orient="records")


    def Participacion(serie):
        Participacion = serie.sum()/len(serie)*0.01
        return(Participacion)
        
        
    data = pd.read_csv("datos.csv")
    data.dropna(axis = 0, how = "all", inplace = True) 
    Departamentos = ['Cauca', 'Córdoba', 'Guainía', 'Guaviare', 'Vaupés', 'Vichada', 'Sucre']
    Variables = ['COBERTURA_NETA', 'TASA_MATRICULACIÓN_5_16']
    Punto1 = data.pivot_table(index = ["DEPARTAMENTO"],
                        values = Variables, aggfunc = 
                        {'COBERTURA_NETA' : Participacion,
                        'TASA_MATRICULACIÓN_5_16' : Participacion}).loc[Departamentos]