from tkinter import Label, Toplevel, Text
from tkinter.ttk import Combobox, Entry, Button, Scrollbar
from cargar_archivos import *

def mostrar_reporte(resultado, reporte):
    ventana_reporte = Toplevel()
    ventana_reporte.state('zoomed')
    ventana_reporte.title("Reporte de Búsqueda")
    ventana_reporte.geometry("1000x500")

    Label(ventana_reporte, text="Reporte de Búsqueda", font=("Arial", 14, "bold")).pack(pady=10)

    frame_texto = Text(ventana_reporte, wrap="word", height=20, width=70)
    frame_texto.pack(expand=True, fill="both", padx=10, pady=5)

    scrollbar = Scrollbar(ventana_reporte, command=frame_texto.yview)
    scrollbar.pack(side="right", fill="y")
    frame_texto.config(yscrollcommand=scrollbar.set)

    # Cálculo de la población total
    poblacion_total = sum(info["valor"] for info in resultado.values())


    texto_completo = f"Total de Población Filtrada: {poblacion_total}\n\n{reporte}"

    frame_texto.insert("1.0", texto_completo)
    frame_texto.config(state="disabled")


def generar_filtros(root):
    data = cargar_poblacion_1()
    Label(root, text="Pais: ").pack(side="left", padx=5, pady=5)
    opciones_paises = Combobox(root, values=list(cargar_paises().keys()), state="readonly", width=12)
    opciones_paises.pack(side="left", padx=5, pady=5)
    
    Label(root, text="Año Inicio: ").pack(side="left", padx=5, pady=5)
    opciones_ano_inicio = Combobox(root, values=cargar_anos(), state="readonly", width=6)
    opciones_ano_inicio.pack(side="left", padx=5, pady=5)
    
    Label(root, text="Año Fin: ").pack(side="left", padx=5, pady=5)
    opciones_ano_fin = Combobox(root, values=cargar_anos(), state="readonly", width=6)
    opciones_ano_fin.pack(side="left", padx=5, pady=5)
    
    Label(root, text="Indicador: ").pack(side="left", padx=5, pady=5)
    opciones_indicador = Combobox(root, values=list(cargar_indicadores().keys()), state="readonly", width=15)
    opciones_indicador.pack(side="left", padx=5, pady=5)
    
    Label(root, text="Comparador: ").pack(side="left", padx=5, pady=5)
    opciones_comparador = Combobox(root, values=[">", "<", "="], state="readonly", width=3)
    opciones_comparador.pack(side="left", padx=5, pady=5)
    
    Label(root, text="Valor: ").pack(side="left", padx=5, pady=5)
    entry_valor = Entry(root, width=10)
    entry_valor.pack(side="left", padx=5, pady=5)
    
    def aplicar_filtro():
        filtros = {
            "pais": opciones_paises.get(),
            "ano_inicio": opciones_ano_inicio.get(),
            "ano_fin": opciones_ano_fin.get(),
            "indicador": opciones_indicador.get(),
            "comparador": opciones_comparador.get(),
            "valor": entry_valor.get()
        }
        resultado, reporte = filtrar_datos(data, filtros)
        mostrar_reporte(resultado,reporte)
    
    Button(root, text="Filtrar", command=aplicar_filtro).pack(side="left", padx=5, pady=5)

def filtrar_datos(data, filtros):

    resultado = {}
    detalles = []
    ano_min = min(item["ano"] for item in data)
    ano_max = max(item["ano"] for item in data)
    
    ano_inicio = int(filtros["ano_inicio"]) if filtros["ano_inicio"] else ano_min
    ano_fin = int(filtros["ano_fin"]) if filtros["ano_fin"] else ano_max
    
    for item in data:
        
        if filtros["pais"] and filtros["pais"] != "" and item["pais"] != filtros["pais"]:
            continue
        if item["ano"] < ano_inicio or item["ano"] > ano_fin:
            continue
        if filtros["indicador"] and filtros["indicador"] != "" and item["indicador_id"] != filtros["indicador"]:
            continue
        if filtros["valor"]:
            valor_filtro = float(filtros["valor"])
            if filtros["comparador"] == ">" and not (item["valor"] > valor_filtro):
                continue
            if filtros["comparador"] == "<" and not (item["valor"] < valor_filtro):
                continue
            if filtros["comparador"] == "=" and not (item["valor"] == valor_filtro):
                continue
        
        if item["pais"] in resultado:
            resultado[item["pais"]]["valor"] += int(item["valor"])
        else:
            resultado[item["pais"]] = {"valor": int(item["valor"])}
        
        detalles.append(f"Año: {item['ano']}, País: {item['pais']}, Indicador: {item['indicador_id']}, Valor: {item['valor']}")
    
    reporte = "\n".join([
        "--- Reporte de Búsqueda ---",
        f"Años: {ano_inicio} - {ano_fin}",
        f"Indicador: {filtros['indicador'] if filtros['indicador'] else 'Todos'}",
        f"Comparador: {filtros['comparador']} {filtros['valor']}" if filtros["valor"] else "Sin filtro de valor",
        "\nResumen por País:",
        "\n".join([f"{pais}: {info['valor']}" for pais, info in resultado.items()]),
        "\nDetalles:",
        "\n".join(detalles)
    ])
    
    return resultado, reporte

