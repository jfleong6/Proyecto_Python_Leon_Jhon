import json

def escribir_json(nombre_archivo, diccionario):
    try:
        with open(nombre_archivo,"w", encoding='utf-8') as archivo:
            json.dump(diccionario, archivo, indent=4)
        print(f"Los datos fueron escritos correctamente en el archivo {nombre_archivo}")
    except (KeyError, ValueError) as e:
        print(f"Error al escribir en el archivo {nombre_archivo} : {e}")
    except IOError as e:
        print(f"Ocurrio un error al escribir en el archivo {nombre_archivo} : {e}")

def leer_json(nombre_archivo):
    try:
        with open(nombre_archivo, "r", encoding='utf-8') as archivo:
            data = json.load(archivo)
            #print(f"Contenido de archivo json {nombre_archivo} : {data}")
            return data
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no fue encontrado")
    except json.JSONDecodeError:
        print(f"Los datos escritos en el archivo {nombre_archivo} no tienen formato JSON")
        return []
    except IOError as e:
        print(f"Hubo un error al leer el archivo {nombre_archivo}:{e}")

def agregar_nuevos_elementos_json(nombre_archivo,new_dicc):
    datos = leer_json(nombre_archivo)
    datos.append(new_dicc)
    escribir_json(nombre_archivo,datos)
    return leer_json(nombre_archivo)


