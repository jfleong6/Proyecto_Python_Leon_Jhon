from tkinter import simpledialog
from tkinter.ttk import *
from tkinter import messagebox
import tkinter as tk
from tkinter import  ttk , filedialog
from tkinter import *
from cargar_archivos import *

from opciones_filtro_interfaz import *
from scroboll import *

def top_level_modificar(archivo, datos, editar = "si"):
    
    def guardar_cambios(i):
        # Recopilar los valores modificados
        valores_modificados = {dato: int(entry.get()) if dato in ["valor", "ano"] else entry.get() for dato, entry in entries.items()}

        datos_antes = leer_json(archivo)
        datos_antes.pop(i)
        datos_antes.insert(i,valores_modificados)
        escribir_json(archivo,datos_antes)

        messagebox.showinfo("Modificaciones", "Registro Actulizado")
        actulizar_registros(frame_paises)

        ventana_modificar_registro.destroy()
    
    def nuevo_registro():
        valores_nuevos = {dato: int(entry.get()) if dato in ["valor", "ano"] else entry.get() for dato, entry in entries.items()}
        agregar_nuevos_elementos_json(archivo,valores_nuevos)
        messagebox.showinfo("Nuevo", "Registro agragado")
        actulizar_registros(frame_paises)
        ventana_modificar_registro.destroy()
    
    try:
        global ventana_modificar_registro
        ventana_modificar_registro.destroy()
    except:
        pass

    ventana_modificar_registro = Toplevel(root)
    ventana_modificar_registro.title("Gestiion de registro")
    
    # Diccionario para almacenar las variables de entrada
    entries = {}
    
    for dato, valor in datos[1].items():
        # Contenedor para cada fila
        frame_dato = Frame(ventana_modificar_registro)
        frame_dato.pack(anchor="w", padx=10, pady=5, fill="x")
        
        # Etiqueta del dato
        Label(frame_dato, text=f"{dato.upper()}: ", 
              font=("Arial", 10, "bold"), 
              width=15, 
              anchor="w").pack(side="left")
        
        # Mapeo de claves a funciones que devuelven valores posibles para el Combobox
        opciones_combobox = {
            "pais": lambda: list(cargar_paises().keys()),
            "codigo_iso": lambda: [i[0] for i in cargar_paises().values()],
            "codigo_iso3": lambda: [i[1] for i in cargar_paises().values()],
            "indicador_id": lambda: list(cargar_indicadores().keys()),
            "descripcion": lambda: list(cargar_indicadores().values()),
        }

        if dato in opciones_combobox:
            valores = opciones_combobox[dato]()  # Obtener los valores dinámicamente
            entry_dato = ttk.Combobox(frame_dato, values=valores)
            entry_dato.set(valor)
            entry_dato.pack(side="left", expand=True, fill="x")
        else:
            # Variable de control para el Entry
            entry_dato = StringVar(value=str(valor))  # Convertir a string explícitamente
            
            # Entry con la variable de control
            entry_widget = ttk.Entry(frame_dato, 
                                    textvariable=entry_dato, 
                                    font=("Arial", 10),
                                    justify="right",
                                    width=30)
            entry_widget.pack(side="left", expand=True, fill="x")
                
                # Guardar la referencia a la variable de control
        entries[dato] = entry_dato
    
    # Botón de guardar
    if editar == "si":
        btn_guardar = ttk.Button(ventana_modificar_registro, 
                             text="Actulizar Cambios", 
                             command=lambda Id=datos[0]:guardar_cambios(Id))
    else:
        btn_guardar = ttk.Button(ventana_modificar_registro, 
                             text="Guardar Registro", 
                             command=nuevo_registro)
    btn_guardar.pack(pady=10)
    
def cargar_interfaz(root, datos, columnas=5):
    
    for i, key in enumerate(datos):
               # Contenedor de contenido
        frame_contenido = Frame(root)
        frame_contenido.grid(row=i // columnas, column=i % columnas, padx=10, pady=10, sticky="nesw")

        # Mostrar los datos con mejor formato
        for dato, valor in datos[key].items():
            Label(frame_contenido, text=f"{dato.upper()}: ", font=("Arial", 10, "bold"), anchor="w", wraplength=150,justify="left").pack(anchor="w")
            Label(frame_contenido, text=f"{valor}", font=("Arial", 10), anchor="w", wraplength=150,justify="left").pack(anchor="w", padx=10, pady=(0, 5))

        # Botón estilizado
        ttk.Button(frame_contenido, text="Modificar", command=lambda archivo="poblacion.json", datos=[i, datos[key]]: top_level_modificar(archivo, datos)).pack(fill="x", padx=5, pady=10)

        #lambda pais=pais: alquilar(pais)

def actulizar_registros(frame_paises):
    global scroll_frame
    try: 
        scroll_frame.destroy()
        print()
    except:
        pass
    scroll_frame = ScrollableFrame(frame_paises)
    scroll_frame.config(bg = "white")
    scroll_frame.pack(fill="both", expand=True)

    poblacion = cargar_poblacion()
    crear_tabla_paises()
    crear_tabla_indicadores()
    cargar_interfaz(scroll_frame.inner_frame, poblacion,columnas)

def top_level_nueva_poblacion():
    top_level_modificar("poblacion.json",["",formato_new_poblacion],"no")

def top_level_nuevo_indicador():    
    top_level_modificar("indicadores.json",["",formato_new_indicador],"no")

def top_level_nuevo_pais():    
    top_level_modificar("paises.json",["",formato_new_pais],"no")

def crear_treeview_con_scroll(root, columnas, datos, formato, archivo):

    def on_double_click(event,formato,archivo):
        """
        Función de ejemplo para manejar el doble clic en el Treeview.
        """
        item = tree.selection()  # Obtener el ítem seleccionado
        dato= {}
        
        if item:
            item_id = item[0]
            valores = tree.item(item_id, "values")
            for clave, valor in zip(formato, valores):
                dato[clave] = valor
            
            top_level_modificar(archivo, [int(item_id),dato])
            
    # Frame contenedor
    
    frame = ttk.Frame(root)
    frame.pack(fill="both", expand=True)

    # Scrollbar vertical
    scrollbar_y = ttk.Scrollbar(frame, orient="vertical")
    scrollbar_y.pack(side="right", fill="y")

    # Treeview
    tree = ttk.Treeview(frame, columns=columnas, show="headings", yscrollcommand=scrollbar_y.set)
    
    # Configurar scrollbar
    scrollbar_y.config(command=tree.yview)

    # Configurar columnas
    for col in columnas:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, anchor="center", width=100)

    for id, dato in enumerate(datos):
        tree.insert("", "end", iid=id, values=dato)


    tree.pack(fill="both", expand=True)

    # Asociar evento de doble clic
    tree.bind("<Double-1>", lambda event: on_double_click(tree, formato, archivo))


    return tree

def crear_tabla_paises():
    limpiar_frame(frame_lista_paises)
    lista_paises = crear_treeview_con_scroll(frame_lista_paises,["Nombre","Codigo ISO","Codigo ISO3"], cargar_paises_lista(), formato_new_pais, "paises.json")

def crear_tabla_indicadores():
    limpiar_frame(frame_lista_indicadores)
    lista_indicadores = crear_treeview_con_scroll(frame_lista_indicadores,["Id Indicador","Descripcion"], cargar_indicadores_lista(), formato_new_indicador, "indicadores.json")

def limpiar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

filtros = [
        "Rango Años",  # Filtra datos dentro de un período específico.
        "Pais",  # Selecciona uno o varios países.
        "Indicador",  # Filtra por tipo de indicador (ej: total de población).
        "Estado",  # Filtra por datos disponibles o no.
        "Crecimiento %",  # Filtra países con crecimiento poblacional mayor a un porcentaje.
        "Valor poblacion",  # Filtra por umbrales de población (> , < , =).
        #"Comparacion interanual",  # Filtra años con cambios significativos respecto al anterior.
        "Cantidad Registros",  # Filtra por cantidad de datos disponibles por país o año.
    ]
formato_new_poblacion = {
        "ano":"",
        "pais":"",
        "codigo_iso3":"",
        "indicador_id": "",
        "descripcion":"",
        "valor":"",
        "estado":"",
        "unidad":""}
formato_new_indicador = {
        "id_indicador": "",
        "descripcion": ""
    }
formato_new_pais = {
        "nombre": "",
        "codigo_iso": "",
        "codigo_iso3": ""
    }

if "__main__" == __name__:
    root = tk.Tk()
    root.state('zoomed')

    ancho = root.winfo_screenwidth()
    print(ancho) 
    
    frame_filtro = LabelFrame(root)
    frame_filtro.pack(side = "top", fill="x",anchor="nw")
    
    generar_filtros(frame_filtro)

    frame_gestion = Frame(root)
    frame_gestion.pack(fill="y",side="left",padx=5,pady=5)

    frame_ver_paises_indicadores = Frame(root)
    frame_ver_paises_indicadores.pack(fill="y",side="right",padx=5,pady=5)

    frame_lista_paises = LabelFrame(frame_ver_paises_indicadores,text="Paises", labelanchor="n", bd=0, font=("Times",25,"bold"))
    frame_lista_paises.pack(fill="y", expand=True, side="top",padx=5,pady=5)
    crear_tabla_paises()

    frame_lista_indicadores = LabelFrame(frame_ver_paises_indicadores,text="Indicadores", labelanchor="n", bd=0, font=("Times",25,"bold"))
    frame_lista_indicadores.pack(fill="both", expand=True, side="top",padx=5,pady=5)
    crear_tabla_indicadores()


    ttk.Button(frame_gestion, text = "Nueva población  ", command=top_level_nueva_poblacion).pack(fill="x",padx=2, pady=2)
    ttk.Button(frame_gestion, text = "Nuevo Indicacador", command=top_level_nuevo_indicador).pack(fill="x",padx=2, pady=2)

    ttk.Button(frame_gestion, text = "Nuevo Pais", command=top_level_nuevo_pais).pack(fill="x",padx=2, pady=2)
    columnas = (ancho - frame_gestion.winfo_height()- frame_ver_paises_indicadores.winfo_height())//250
    print(columnas)
    frame_paises = Frame(root,bg="white")
    frame_paises.pack(fill="both",expand=True,padx=5,pady=5)
    actulizar_registros(frame_paises)
    
    root.mainloop()