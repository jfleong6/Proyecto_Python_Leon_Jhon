from funciones_r_w_json import *

def cargar_indicadores(nombre_archivo = "indicadores.json"):
    indicadores  = leer_json(nombre_archivo)
    lista_indicadores = {i["id_indicador"]:i["descripcion"] for i in indicadores}
    return lista_indicadores
def cargar_indicadores_lista(nombre_archivo = "indicadores.json"):
    indicadores  = leer_json(nombre_archivo)
    lista_indicadores = [[i["id_indicador"],i["descripcion"]] for i in indicadores]
    return lista_indicadores
def cargar_paises(nombre_archivo = "paises.json"):
    paises  = leer_json(nombre_archivo)
    lista_paises = {i["nombre"]:[i["codigo_iso"],i["codigo_iso3"]]for i in paises}
    return lista_paises
def cargar_paises_lista(nombre_archivo = "paises.json"):
    paises  = leer_json(nombre_archivo)
    lista_paises = [[i["nombre"], i["codigo_iso"], i["codigo_iso3"]] for i in paises]
    return lista_paises
def cargar_anos(nombre_archivo = "poblacion.json"):
    poblacion = leer_json(nombre_archivo)
    anos = [str(i["ano"]) for i in poblacion]
    con = set(anos)
    return sorted(con)

def cargar_poblacion(nombre_archivo = "poblacion.json"):
    poblacion = leer_json(nombre_archivo)
    poblaciones = {i:j for i,j in enumerate(poblacion)}
    return poblaciones
def cargar_poblacion_1(nombre_archivo = "poblacion.json"):
    poblacion = leer_json(nombre_archivo)
    poblaciones = [i for i in poblacion]
    return poblaciones

def cargar_estado(nombre_archivo = "poblacion.json"):
    poblacion = leer_json(nombre_archivo)
    anos = [str(i["estado"]) for i in poblacion]
    con = set(anos)
    return sorted(con)

def cargar_por_pais(poblacion):
    poblacion_paises = {}
    for item in poblacion:
        if item["pais"] in poblacion_paises:
            poblacion_paises[item["pais"]]["valor"] += item["valor"]
        else:
            poblacion_paises[item["pais"]]={"valor":item["valor"]}
        if item["indicador_id"] in poblacion_paises[item["pais"]]:
            poblacion_paises[item["pais"]][item["indicador_id"]] += item["valor"]
        else:
            poblacion_paises[item["pais"]][item["indicador_id"]] = item["valor"]
        if item["ano"] in poblacion_paises[item["pais"]]:
            poblacion_paises[item["pais"]][item["ano"]] += item["valor"]
        else:
            poblacion_paises[item["pais"]][item["ano"]] = item["valor"]
        
    return poblacion_paises
