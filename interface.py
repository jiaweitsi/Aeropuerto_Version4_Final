import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import subprocess

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from airport import *
from aircraft import *
from LEBL import *

# =====================================================================
# TRADUCCIONES
# =====================================================================

TEXTOS = {
    "es": {
        "titulo_app": "Airport Manager",
        "aeropuertos": "Aeropuertos",
        "anadir_borrar": "Añadir / Borrar Aeropuerto",
        "gestion_vuelos": "Gestión de Vuelos",
        "gestion_gates": "Gestión de Gates",
        "salidas_dinamica": "Salidas y Dinámica",
        "gestion_manual": "Gestión Manual de Gates",
        "consola": "Consola / Resultados",
        "visualizacion": "Visualización de Gráficas",
        "graficas": "Gráficas",
        "cargar_aeropuertos": "Cargar Aeropuertos",
        "guardar_schengen": "Guardar Schengen",
        "ver_google_earth": "Ver Puntos Google Earth",
        "icao_label": "ICAO (ej: LEBL):",
        "lat_label": "Latitud:",
        "lon_label": "Longitud:",
        "anadir": "Añadir",
        "borrar": "Borrar",
        "cargar_vuelos": "Cargar Vuelos",
        "trayectorias": "Trayectorias en Google Earth",
        "filtrar_largos": "Filtrar Vuelos Largos (>2000km)",
        "guardar_vuelos": "Guardar Vuelos",
        "exportar_largos": "Exportar Vuelos Largos a fichero",
        "cargar_estructura": "Cargar Estructura",
        "asignar_gates": "Asignar Gates a Vuelos",
        "ver_ocupacion": "Ver Ocupación de Gates",
        "cargar_salidas": "Cargar Salidas",
        "ver_nocturnos": "Ver Aviones Nocturnos",
        "asignar_nocturnos": "Asignar Gates Nocturnos",
        "hora_label": "Hora (hh:mm):",
        "asignar_hora": "Asignar Gates por Hora",
        "liberar_gate_label": "ID Avión a liberar:",
        "liberar_gate_btn": "🔓 Liberar Gate",
        "reasignar_titulo": "Reasignar Gate Manualmente",
        "reasignar_avion_label": "ID Avión:",
        "reasignar_gate_label": "Nuevo Gate (ej: T1AG3):",
        "reasignar_btn": "🔄 Reasignar Gate",
        "graf_schengen_ap": "Aeropuertos Schengen vs No Schengen",
        "graf_llegadas": "Llegadas por hora",
        "graf_aerolineas": "Vuelos por Aerolínea",
        "graf_schengen_v": "Vuelos Schengen vs No Schengen",
        "graf_gates": "Mapa de Gates",
        "graf_ocupacion": "Ocupación del Día",
        "borrar_grafica": "Borrar Gráfica",
        "msg_cargado": "Datos cargados correctamente",
        "msg_cargar_titulo": "Cargar",
        "msg_error_icao": "El código ICAO debe tener 4 LETRAS.",
        "msg_error_nums": "Introduce números válidos en Lat y Lon.",
        "msg_error_existe": "El aeropuerto ya existe en la lista.",
        "msg_aviso_icao": "Escribe el código ICAO a borrar.",
        "msg_schengen_ok": "Archivo Schengen_Only.txt creado",
        "msg_guardar": "Guardar",
        "msg_ge_ok": "Archivo generado y abierto en Google Earth Pro",
        "msg_ge_titulo": "Google Earth",
        "msg_ge_error": "Archivo generado pero no se pudo abrir Google Earth.\nAbre manualmente airports_map.kml",
        "msg_aviso": "Aviso",
        "msg_carga_primero_ap": "Carga los aeropuertos primero",
        "msg_vuelos_ok": "Vuelos cargados correctamente",
        "msg_vuelos_titulo": "Vuelos",
        "msg_carga_primero_v": "Carga los vuelos primero",
        "msg_tray_error": "Archivo generado pero no se pudo abrir Google Earth.\nAbre manualmente trayectorias.kml",
        "msg_largos_titulo": "--- VUELOS LARGA DISTANCIA (>2000km) ---\n",
        "msg_guardados": "Guardados ",
        "msg_vuelos_guardados": " vuelos.",
        "msg_exportar": "Exportar",
        "msg_no_largos": "No hay vuelos de más de 2000km",
        "msg_atencion": "Atención",
        "msg_no_vuelos": "No hay vuelos cargados",
        "msg_error": "Error",
        "msg_vuelos_guardados2": "Vuelos guardados en 'vuelos_guardados.txt'",
        "msg_no_pudo": "No se ha podido guardar el archivo",
        "msg_estructura_error": "No se pudo cargar Terminals.txt",
        "msg_aeropuerto": "Aeropuerto ",
        "msg_cargado_ok": " cargado correctamente",
        "msg_estructura_titulo": "Estructura",
        "msg_primero_estructura": "Primero carga la estructura (Terminals.txt)",
        "msg_primero_vuelos": "Primero carga los vuelos",
        "msg_asignados": "Asignados: ",
        "msg_no_asignados": "\nNo asignados: ",
        "msg_gates_titulo": "Gates",
        "msg_primero_estructura2": "Primero carga la estructura del aeropuerto",
        "msg_total_gates": "Total gates: ",
        "msg_libres": "Gates libres: ",
        "msg_ocupados": "Gates ocupados: ",
        "msg_dep_error": "No se encontró Departures.txt o está vacío",
        "msg_fusion_error": "Error al fusionar llegadas y salidas",
        "msg_salidas_ok": "Salidas cargadas y fusionadas correctamente",
        "msg_salidas_titulo": "Salidas",
        "msg_nocturnos_titulo": "--- AVIONES NOCTURNOS ---\n",
        "msg_no_nocturnos": "No hay aviones nocturnos\n",
        "msg_info": "Info",
        "msg_no_nocturnos2": "No hay aviones nocturnos",
        "msg_nocturnos_ok": "Gates asignados a aviones nocturnos",
        "msg_nocturnos_titulo2": "Nocturnos",
        "msg_hora_formato": "Formato incorrecto. Usa hh:mm (ej: 08:00)",
        "msg_hora_rango": "Hora fuera de rango (00:00 - 23:59)",
        "msg_hora_nums": "Introduce números válidos en la hora",
        "msg_hora_ok": "Periodo a partir de ",
        "msg_hora_ok2": " procesado.\nAviones no asignados: ",
        "msg_hora_titulo": "Asignación por hora",
        "msg_liberar_ok": "Gate liberado correctamente para el avión: ",
        "msg_liberar_error": "No se encontró el avión en ningún gate: ",
        "msg_liberar_vacio": "Introduce el ID del avión a liberar.",
        "msg_liberar_titulo": "Liberar Gate",
        "msg_reasignar_vacio": "Rellena el ID del avión y el nombre del gate.",
        "msg_reasignar_gate_nf": "Gate no encontrado: ",
        "msg_reasignar_ocupado": "Ese gate ya está ocupado por otro avión.",
        "msg_reasignar_avion_nf": "El avión no está asignado a ningún gate actualmente.\nSe asignará directamente al nuevo gate.",
        "msg_reasignar_ok": "Gate reasignado correctamente.\nAvión: ",
        "msg_reasignar_nuevo": "\nNuevo Gate: ",
        "msg_reasignar_titulo": "Reasignar Gate",
        "ocu_titulo": "=== OCUPACION DE GATES - ",
        "ocu_terminal": "\nTERMINAL ",
        "ocu_area": "  Area ",
        "avion_label": "Avión: ",
        "origen_label": " | Origen: ",
        "hora_llegada": " | Llegada: ",
        "destino_label": " | Destino: ",
        "hora_salida": " | Salida: ",
        "compania_label": " | Compañía: ",
        "hora_label2": " | Hora: ",
        "cod_label": "Cod: ",
        "lat_col": " | Lat: ",
        "lon_col": " | Lon: ",
        "schengen_col": " | Schengen: ",
        "si": "SI",
        "no": "NO",
        "ocupado": "Ocupado",
    },
    "en": {
        "titulo_app": "Airport Manager",
        "aeropuertos": "Airports",
        "anadir_borrar": "Add / Remove Airport",
        "gestion_vuelos": "Flight Management",
        "gestion_gates": "Gate Management",
        "salidas_dinamica": "Departures & Dynamics",
        "gestion_manual": "Manual Gate Management",
        "consola": "Console / Results",
        "visualizacion": "Chart Viewer",
        "graficas": "Charts",
        "cargar_aeropuertos": "Load Airports",
        "guardar_schengen": "Save Schengen",
        "ver_google_earth": "View in Google Earth",
        "icao_label": "ICAO (e.g. LEBL):",
        "lat_label": "Lat:",
        "lon_label": "Lon:",
        "anadir": "Add",
        "borrar": "Remove",
        "cargar_vuelos": "Load Flights",
        "trayectorias": "Trajectories in Google Earth",
        "filtrar_largos": "Filter Long Flights (>2000km)",
        "guardar_vuelos": "Save Flights",
        "exportar_largos": "Export Long Flights to file",
        "cargar_estructura": "Load Structure",
        "asignar_gates": "Assign Gates to Flights",
        "ver_ocupacion": "View Gate Occupancy",
        "cargar_salidas": "Load Departures",
        "ver_nocturnos": "View Night Aircraft",
        "asignar_nocturnos": "Assign Night Gates",
        "hora_label": "Time (hh:mm):",
        "asignar_hora": "Assign Gates by Time",
        "liberar_gate_label": "Aircraft ID to free:",
        "liberar_gate_btn": "🔓 Free Gate",
        "reasignar_titulo": "Manually Reassign Gate",
        "reasignar_avion_label": "Aircraft ID:",
        "reasignar_gate_label": "New Gate (e.g. T1AG3):",
        "reasignar_btn": "🔄 Reassign Gate",
        "graf_schengen_ap": "Airports Schengen vs Non-Schengen",
        "graf_llegadas": "Arrivals by hour",
        "graf_aerolineas": "Flights by Airline",
        "graf_schengen_v": "Flights Schengen vs Non-Schengen",
        "graf_gates": "Gate Map",
        "graf_ocupacion": "Day Occupancy",
        "borrar_grafica": "Clear Chart",
        "msg_cargado": "Data loaded successfully",
        "msg_cargar_titulo": "Load",
        "msg_error_icao": "ICAO code must have 4 LETTERS.",
        "msg_error_nums": "Enter valid numbers for Lat and Lon.",
        "msg_error_existe": "Airport already exists in the list.",
        "msg_aviso_icao": "Enter the ICAO code to remove.",
        "msg_schengen_ok": "File Schengen_Only.txt created",
        "msg_guardar": "Save",
        "msg_ge_ok": "File generated and opened in Google Earth Pro",
        "msg_ge_titulo": "Google Earth",
        "msg_ge_error": "File generated but could not open Google Earth.\nOpen airports_map.kml manually",
        "msg_aviso": "Warning",
        "msg_carga_primero_ap": "Load airports first",
        "msg_vuelos_ok": "Flights loaded successfully",
        "msg_vuelos_titulo": "Flights",
        "msg_carga_primero_v": "Load flights first",
        "msg_tray_error": "File generated but could not open Google Earth.\nOpen trayectorias.kml manually",
        "msg_largos_titulo": "--- LONG DISTANCE FLIGHTS (>2000km) ---\n",
        "msg_guardados": "Saved ",
        "msg_vuelos_guardados": " flights.",
        "msg_exportar": "Export",
        "msg_no_largos": "No flights over 2000km",
        "msg_atencion": "Attention",
        "msg_no_vuelos": "No flights loaded",
        "msg_error": "Error",
        "msg_vuelos_guardados2": "Flights saved to 'vuelos_guardados.txt'",
        "msg_no_pudo": "Could not save the file",
        "msg_estructura_error": "Could not load Terminals.txt",
        "msg_aeropuerto": "Airport ",
        "msg_cargado_ok": " loaded successfully",
        "msg_estructura_titulo": "Structure",
        "msg_primero_estructura": "Load the structure (Terminals.txt) first",
        "msg_primero_vuelos": "Load flights first",
        "msg_asignados": "Assigned: ",
        "msg_no_asignados": "\nNot assigned: ",
        "msg_gates_titulo": "Gates",
        "msg_primero_estructura2": "Load the airport structure first",
        "msg_total_gates": "Total gates: ",
        "msg_libres": "Free gates: ",
        "msg_ocupados": "Occupied gates: ",
        "msg_dep_error": "Departures.txt not found or empty",
        "msg_fusion_error": "Error merging arrivals and departures",
        "msg_salidas_ok": "Departures loaded and merged successfully",
        "msg_salidas_titulo": "Departures",
        "msg_nocturnos_titulo": "--- NIGHT AIRCRAFT ---\n",
        "msg_no_nocturnos": "No night aircraft\n",
        "msg_info": "Info",
        "msg_no_nocturnos2": "No night aircraft",
        "msg_nocturnos_ok": "Gates assigned to night aircraft",
        "msg_nocturnos_titulo2": "Night",
        "msg_hora_formato": "Wrong format. Use hh:mm (e.g. 08:00)",
        "msg_hora_rango": "Time out of range (00:00 - 23:59)",
        "msg_hora_nums": "Enter valid numbers for the time",
        "msg_hora_ok": "Period from ",
        "msg_hora_ok2": " processed.\nUnassigned aircraft: ",
        "msg_hora_titulo": "Assignment by time",
        "msg_liberar_ok": "Gate freed successfully for aircraft: ",
        "msg_liberar_error": "Aircraft not found in any gate: ",
        "msg_liberar_vacio": "Enter the aircraft ID to free.",
        "msg_liberar_titulo": "Free Gate",
        "msg_reasignar_vacio": "Fill in both the aircraft ID and the gate name.",
        "msg_reasignar_gate_nf": "Gate not found: ",
        "msg_reasignar_ocupado": "That gate is already occupied by another aircraft.",
        "msg_reasignar_avion_nf": "Aircraft is not currently assigned to any gate.\nIt will be assigned directly to the new gate.",
        "msg_reasignar_ok": "Gate reassigned successfully.\nAircraft: ",
        "msg_reasignar_nuevo": "\nNew Gate: ",
        "msg_reasignar_titulo": "Reassign Gate",
        "ocu_titulo": "=== GATE OCCUPANCY - ",
        "ocu_terminal": "\nTERMINAL ",
        "ocu_area": "  Area ",
        "avion_label": "Aircraft: ",
        "origen_label": " | Origin: ",
        "hora_llegada": " | Arrival: ",
        "destino_label": " | Destination: ",
        "hora_salida": " | Departure: ",
        "compania_label": " | Airline: ",
        "hora_label2": " | Time: ",
        "cod_label": "Code: ",
        "lat_col": " | Lat: ",
        "lon_col": " | Lon: ",
        "schengen_col": " | Schengen: ",
        "si": "YES",
        "no": "NO",
        "ocupado": "Occupied",
    },
    "zh": {
        "titulo_app": "机场管理器",
        "aeropuertos": "机场",
        "anadir_borrar": "添加 / 删除机场",
        "gestion_vuelos": "航班管理",
        "gestion_gates": "登机口管理",
        "salidas_dinamica": "出发与动态",
        "gestion_manual": "手动登机口管理",
        "consola": "控制台 / 结果",
        "visualizacion": "图表查看器",
        "graficas": "图表",
        "cargar_aeropuertos": "加载机场",
        "guardar_schengen": "保存申根区",
        "ver_google_earth": "在谷歌地球中查看",
        "icao_label": "ICAO代码 (如 LEBL):",
        "lat_label": "纬度:",
        "lon_label": "经度:",
        "anadir": "添加",
        "borrar": "删除",
        "cargar_vuelos": "加载航班",
        "trayectorias": "在谷歌地球中显示轨迹",
        "filtrar_largos": "筛选长途航班 (>2000km)",
        "guardar_vuelos": "保存航班",
        "exportar_largos": "导出长途航班到文件",
        "cargar_estructura": "加载结构",
        "asignar_gates": "为航班分配登机口",
        "ver_ocupacion": "查看登机口占用情况",
        "cargar_salidas": "加载出发航班",
        "ver_nocturnos": "查看夜间飞机",
        "asignar_nocturnos": "分配夜间登机口",
        "hora_label": "时间 (hh:mm):",
        "asignar_hora": "按时间分配登机口",
        "liberar_gate_label": "要释放的飞机ID:",
        "liberar_gate_btn": "🔓 释放登机口",
        "reasignar_titulo": "手动重新分配登机口",
        "reasignar_avion_label": "飞机ID:",
        "reasignar_gate_label": "新登机口 (如 T1AG3):",
        "reasignar_btn": "🔄 重新分配登机口",
        "graf_schengen_ap": "申根与非申根机场",
        "graf_llegadas": "按小时到达",
        "graf_aerolineas": "按航空公司分类航班",
        "graf_schengen_v": "申根与非申根航班",
        "graf_gates": "登机口地图",
        "graf_ocupacion": "全天占用情况",
        "borrar_grafica": "清除图表",
        "msg_cargado": "数据加载成功",
        "msg_cargar_titulo": "加载",
        "msg_error_icao": "ICAO代码必须为4个字母。",
        "msg_error_nums": "请输入有效的纬度和经度数字。",
        "msg_error_existe": "机场已存在于列表中。",
        "msg_aviso_icao": "请输入要删除的ICAO代码。",
        "msg_schengen_ok": "文件 Schengen_Only.txt 已创建",
        "msg_guardar": "保存",
        "msg_ge_ok": "文件已生成并在谷歌地球专业版中打开",
        "msg_ge_titulo": "谷歌地球",
        "msg_ge_error": "文件已生成但无法打开谷歌地球。\n请手动打开 airports_map.kml",
        "msg_aviso": "警告",
        "msg_carga_primero_ap": "请先加载机场",
        "msg_vuelos_ok": "航班加载成功",
        "msg_vuelos_titulo": "航班",
        "msg_carga_primero_v": "请先加载航班",
        "msg_tray_error": "文件已生成但无法打开谷歌地球。\n请手动打开 trayectorias.kml",
        "msg_largos_titulo": "--- 长途航班 (>2000km) ---\n",
        "msg_guardados": "已保存 ",
        "msg_vuelos_guardados": " 个航班。",
        "msg_exportar": "导出",
        "msg_no_largos": "没有超过2000km的航班",
        "msg_atencion": "注意",
        "msg_no_vuelos": "没有已加载的航班",
        "msg_error": "错误",
        "msg_vuelos_guardados2": "航班已保存到 'vuelos_guardados.txt'",
        "msg_no_pudo": "无法保存文件",
        "msg_estructura_error": "无法加载 Terminals.txt",
        "msg_aeropuerto": "机场 ",
        "msg_cargado_ok": " 加载成功",
        "msg_estructura_titulo": "结构",
        "msg_primero_estructura": "请先加载结构 (Terminals.txt)",
        "msg_primero_vuelos": "请先加载航班",
        "msg_asignados": "已分配: ",
        "msg_no_asignados": "\n未分配: ",
        "msg_gates_titulo": "登机口",
        "msg_primero_estructura2": "请先加载机场结构",
        "msg_total_gates": "登机口总数: ",
        "msg_libres": "空闲登机口: ",
        "msg_ocupados": "占用登机口: ",
        "msg_dep_error": "未找到 Departures.txt 或文件为空",
        "msg_fusion_error": "合并到达和出发时出错",
        "msg_salidas_ok": "出发航班加载并合并成功",
        "msg_salidas_titulo": "出发",
        "msg_nocturnos_titulo": "--- 夜间飞机 ---\n",
        "msg_no_nocturnos": "没有夜间飞机\n",
        "msg_info": "信息",
        "msg_no_nocturnos2": "没有夜间飞机",
        "msg_nocturnos_ok": "已为夜间飞机分配登机口",
        "msg_nocturnos_titulo2": "夜间",
        "msg_hora_formato": "格式错误，请使用 hh:mm (如 08:00)",
        "msg_hora_rango": "时间超出范围 (00:00 - 23:59)",
        "msg_hora_nums": "请输入有效的时间数字",
        "msg_hora_ok": "已处理从 ",
        "msg_hora_ok2": " 起的时段。\n未分配飞机: ",
        "msg_hora_titulo": "按时间分配",
        "msg_liberar_ok": "飞机登机口已成功释放: ",
        "msg_liberar_error": "在任何登机口都找不到飞机: ",
        "msg_liberar_vacio": "请输入要释放的飞机ID。",
        "msg_liberar_titulo": "释放登机口",
        "msg_reasignar_vacio": "请填写飞机ID和登机口名称。",
        "msg_reasignar_gate_nf": "未找到登机口: ",
        "msg_reasignar_ocupado": "该登机口已被其他飞机占用。",
        "msg_reasignar_avion_nf": "该飞机当前未分配到任何登机口。\n将直接分配到新登机口。",
        "msg_reasignar_ok": "登机口重新分配成功。\n飞机: ",
        "msg_reasignar_nuevo": "\n新登机口: ",
        "msg_reasignar_titulo": "重新分配登机口",
        "ocu_titulo": "=== 登机口占用 - ",
        "ocu_terminal": "\n航站楼 ",
        "ocu_area": "  区域 ",
        "avion_label": "飞机: ",
        "origen_label": " | 出发地: ",
        "hora_llegada": " | 到达: ",
        "destino_label": " | 目的地: ",
        "hora_salida": " | 出发: ",
        "compania_label": " | 航空公司: ",
        "hora_label2": " | 时间: ",
        "cod_label": "代码: ",
        "lat_col": " | 纬度: ",
        "lon_col": " | 经度: ",
        "schengen_col": " | 申根: ",
        "si": "是",
        "no": "否",
        "ocupado": "占用",
    }
}

idioma_actual = "es"

def T(clave):
    return TEXTOS[idioma_actual].get(clave, clave)


# =====================================================================
# PANTALLA DE BIENVENIDA
# =====================================================================

def mostrar_splash():
    splash = tk.Tk()
    splash.title("Airport Manager")
    splash.geometry("520x340")
    splash.resizable(False, False)
    splash.configure(bg="#F0EBF8")

    splash.update_idletasks()
    w = splash.winfo_screenwidth()
    h = splash.winfo_screenheight()
    x = (w - 520) // 2
    y = (h - 340) // 2
    splash.geometry(f"520x340+{x}+{y}")

    canvas_bg = tk.Canvas(splash, bg="#F0EBF8", highlightthickness=0)
    canvas_bg.place(relx=0, rely=0, relwidth=1, relheight=1)
    canvas_bg.create_oval(-60, -60, 200, 200, fill="#E4D9F5", outline="")
    canvas_bg.create_oval(360, 190, 590, 410, fill="#D9EEF5", outline="")
    canvas_bg.create_oval(190, -40, 390, 130, fill="#F5E6D9", outline="")

    lbl_icon = tk.Label(splash, text="✈", font=("Segoe UI", 44), bg="#F0EBF8", fg="#9B7EC8")
    lbl_icon.place(relx=0.5, y=54, anchor="center")

    lbl_title = tk.Label(splash, text="Airport Manager",
        font=("Segoe UI", 23, "bold"), bg="#F0EBF8", fg="#5C3D8F")
    lbl_title.place(relx=0.5, y=112, anchor="center")

    lbl_sub = tk.Label(splash,
        text="Select your language  /  Elige tu idioma  /  选择语言",
        font=("Segoe UI", 10), bg="#F0EBF8", fg="#9B7EC8")
    lbl_sub.place(relx=0.5, y=146, anchor="center")

    sep = tk.Frame(splash, height=1, bg="#D4C5E8")
    sep.place(relx=0.1, y=166, relwidth=0.8)

    idioma_elegido = [None]

    def elegir(lang):
        idioma_elegido[0] = lang
        splash.destroy()

    btn_frame = tk.Frame(splash, bg="#F0EBF8")
    btn_frame.place(relx=0.5, y=232, anchor="center")

    langs = [
        ("🇪🇸  Español", "es", "#D4EAC8", "#3A6020", "#BFE0AA"),
        ("🇬🇧  English", "en", "#C8DCF0", "#1E4A7A", "#A8C8EC"),
        ("🇨🇳  中文",    "zh", "#F5D0C8", "#7A2010", "#EBB0A0"),
    ]

    for txt, code, bg_col, fg_col, hover_col in langs:
        btn = tk.Button(btn_frame, text=txt,
            font=("Segoe UI", 11, "bold"),
            bg=bg_col, fg=fg_col,
            activebackground=hover_col, activeforeground=fg_col,
            relief="flat", bd=0, padx=18, pady=10,
            cursor="hand2", command=lambda c=code: elegir(c))
        btn.pack(side=tk.LEFT, padx=10)
        btn.bind("<Enter>", lambda e, b=btn, h=hover_col: b.configure(bg=h))
        btn.bind("<Leave>", lambda e, b=btn, n=bg_col: b.configure(bg=n))

    lbl_ver = tk.Label(splash, text="v4.0  |  Barcelona Airport",
        font=("Segoe UI", 8), bg="#F0EBF8", fg="#B8A8D0")
    lbl_ver.place(relx=0.5, y=314, anchor="center")

    splash.mainloop()
    return idioma_elegido[0]


# =====================================================================
# VARIABLES GLOBALES
# =====================================================================

lista_trabajo = []
lista_vuelos = []
bcn = None
simulacion_activa = False
hora_simulacion = 0
btn_play = None
btn_stop = None
lbl_hora_sim = None
row_idx = 0  # <-- añade esta
# =====================================================================
# FUNCIONES - AEROPUERTOS
# =====================================================================

def btn_cargar_click():
    global lista_trabajo
    lista_trabajo = LoadAirports("Airports.txt")
    actualizar_pantalla()
    messagebox.showinfo(T("msg_cargar_titulo"), T("msg_cargado"))

def btn_anadir_click():
    c = entrada_cod.get().upper()
    lat = entrada_lat.get()
    lon = entrada_lon.get()
    if len(c) != 4 or not c.isalpha():
        messagebox.showerror(T("msg_error"), T("msg_error_icao"))
        return
    try:
        lat = float(lat)
        lon = float(lon)
        nuevo = Airport(c, lat, lon)
        anadido = AddAirport(lista_trabajo, nuevo)
        if anadido:
            # Limpiar los campos después de añadir
            entrada_cod.delete(0, tk.END)
            entrada_lat.delete(0, tk.END)
            entrada_lon.delete(0, tk.END)
            actualizar_pantalla()
        else:
            messagebox.showerror(T("msg_error"), T("msg_error_existe"))
    except ValueError:
        messagebox.showerror(T("msg_error"), T("msg_error_nums"))

def btn_borrar_click():
    c = entrada_cod.get().upper()
    if c == "":
        messagebox.showwarning(T("msg_aviso"), T("msg_aviso_icao"))
        return
    RemoveAirport(lista_trabajo, c)
    actualizar_pantalla()

def btn_guardar_click():
    SaveSchengenAirports(lista_trabajo, "Schengen_Only.txt")
    messagebox.showinfo(T("msg_guardar"), T("msg_schengen_ok"))

def abrir_google_earth(archivo_kml):
    archivo_kml = os.path.abspath(archivo_kml)  # <-- añade esta línea
    if not os.path.exists(archivo_kml):
        return False
    try:
        rutas_windows = [
            "C:\\Program Files\\Google\\Google Earth Pro\\client\\googleearth.exe",
            "C:\\Program Files (x86)\\Google\\Google Earth Pro\\client\\googleearth.exe",
        ]
        encontrado = False
        i = 0
        while i < len(rutas_windows) and not encontrado:
            if os.path.exists(rutas_windows[i]):
                subprocess.Popen([rutas_windows[i], archivo_kml])
                encontrado = True
            i = i + 1
        if not encontrado:
            os.startfile(archivo_kml)
        return True
    except Exception as e:
        print("Error:", e)
        return False

def btn_mapa_aeropuertos_click():
    if len(lista_trabajo) == 0:
        messagebox.showwarning(T("msg_aviso"), T("msg_carga_primero_ap"))
        return
    MapAirports(lista_trabajo)
    exito = abrir_google_earth("airports_map.kml")
    if exito:
        messagebox.showinfo(T("msg_ge_titulo"), T("msg_ge_ok"))
    else:
        messagebox.showwarning(T("msg_aviso"), T("msg_ge_error"))

def actualizar_pantalla():
    caja.delete(1.0, tk.END)
    i = 0
    while i < len(lista_trabajo):
        a = lista_trabajo[i]
        SetSchengen(a)
        res = T("si") if a.schengen else T("no")
        caja.insert(tk.END,
            T("cod_label") + a.code +
            T("lat_col") + str(round(a.lat, 4)) +
            T("lon_col") + str(round(a.lon, 4)) +
            T("schengen_col") + res + "\n")
        i = i + 1


# =====================================================================
# FUNCIONES - VUELOS
# =====================================================================

def btn_cargar_vuelos_click():
    global lista_vuelos
    lista_vuelos = LoadArrivals("Arrivals.txt")
    actualizar_pantalla_vuelos()
    messagebox.showinfo(T("msg_vuelos_titulo"), T("msg_vuelos_ok"))

def btn_mapa_kml_click():
    if len(lista_vuelos) == 0:
        messagebox.showwarning(T("msg_aviso"), T("msg_carga_primero_v"))
        return
    if len(lista_trabajo) == 0:
        messagebox.showwarning(T("msg_aviso"), T("msg_carga_primero_ap"))
        return
    MapFlights(lista_vuelos, lista_trabajo)
    exito = abrir_google_earth("trayectorias.kml")
    if exito:
        messagebox.showinfo(T("msg_ge_titulo"), T("msg_ge_ok"))
    else:
        messagebox.showwarning(T("msg_aviso"), T("msg_tray_error"))

def btn_vuelos_largos_click():
    if len(lista_vuelos) == 0:
        messagebox.showwarning(T("msg_aviso"), T("msg_carga_primero_v"))
        return
    if len(lista_trabajo) == 0:
        messagebox.showwarning(T("msg_aviso"), T("msg_carga_primero_ap"))
        return
    vuelos_distantes = LongFlightArrivals(lista_vuelos, lista_trabajo)
    caja.delete(1.0, tk.END)
    caja.insert(tk.END, T("msg_largos_titulo"))
    i = 0
    while i < len(vuelos_distantes):
        v = vuelos_distantes[i]
        caja.insert(tk.END,
            T("avion_label") + str(v.aircraft) +
            T("origen_label") + str(v.origin) +
            T("hora_label2") + str(v.time) + "\n")
        i = i + 1

def btn_exportar_vuelos_largos_click():
    if len(lista_vuelos) == 0:
        messagebox.showwarning(T("msg_aviso"), T("msg_carga_primero_v"))
        return
    if len(lista_trabajo) == 0:
        messagebox.showwarning(T("msg_aviso"), T("msg_carga_primero_ap"))
        return
    vuelos_especiales = LongFlightArrivals(lista_vuelos, lista_trabajo)
    if len(vuelos_especiales) > 0:
        exito = SaveFlights(vuelos_especiales, "vuelos_largos.txt")
        if exito:
            messagebox.showinfo(T("msg_exportar"),
                T("msg_guardados") + str(len(vuelos_especiales)) + T("msg_vuelos_guardados"))
        else:
            messagebox.showerror(T("msg_error"), T("msg_no_pudo"))
    else:
        messagebox.showwarning(T("msg_atencion"), T("msg_no_largos"))

def actualizar_pantalla_vuelos():
    caja.delete(1.0, tk.END)
    i = 0
    while i < len(lista_vuelos):
        v = lista_vuelos[i]
        caja.insert(tk.END,
            T("avion_label") + str(v.aircraft) +
            T("origen_label") + str(v.origin) +
            T("hora_label2") + str(v.time) +
            T("compania_label") + str(v.company) + "\n")
        i = i + 1

def btn_guardar_vuelos_fichero_click():
    if len(lista_vuelos) == 0:
        messagebox.showwarning(T("msg_error"), T("msg_no_vuelos"))
        return
    exito = SaveFlights(lista_vuelos, "vuelos_guardados.txt")
    if exito:
        messagebox.showinfo(T("msg_guardar"), T("msg_vuelos_guardados2"))
    else:
        messagebox.showerror(T("msg_error"), T("msg_no_pudo"))


# =====================================================================
# FUNCIONES - GATES
# =====================================================================

def btn_cargar_estructura_click():
    global bcn
    resultado = LoadAirportStructure("Terminals.txt")
    if resultado is None:
        messagebox.showerror(T("msg_error"), T("msg_estructura_error"))
        return
    bcn = resultado
    actualizar_pantalla_gates()
    messagebox.showinfo(T("msg_estructura_titulo"),
        T("msg_aeropuerto") + bcn.code + T("msg_cargado_ok"))

def btn_asignar_gates_click():
    if bcn is None:
        messagebox.showerror(T("msg_error"), T("msg_primero_estructura"))
        return
    if len(lista_vuelos) == 0:
        messagebox.showerror(T("msg_error"), T("msg_primero_vuelos"))
        return
    asignados = 0
    no_asignados = 0
    i = 0
    while i < len(lista_vuelos):
        resultado = AssignGate(bcn, lista_vuelos[i])
        if resultado == 0:
            asignados += 1
        else:
            no_asignados += 1
        i += 1
    actualizar_pantalla_gates()
    messagebox.showinfo(T("msg_gates_titulo"),
        T("msg_asignados") + str(asignados) +
        T("msg_no_asignados") + str(no_asignados))

def btn_ver_ocupacion_click():
    if bcn is None:
        messagebox.showerror(T("msg_error"), T("msg_primero_estructura2"))
        return
    caja.delete(1.0, tk.END)
    ocupacion = GateOccupancy(bcn)
    total_gates = 0
    gates_libres = 0
    gates_ocupados = 0
    i = 0
    while i < len(ocupacion):
        gate = ocupacion[i]
        total_gates += 1
        if gate[3] == "Ocupado":
            gates_ocupados += 1
        else:
            gates_libres += 1
        i += 1
    caja.insert(tk.END, T("msg_total_gates") + str(total_gates) + "\n")
    caja.insert(tk.END, T("msg_libres") + str(gates_libres) + "\n")
    caja.insert(tk.END, T("msg_ocupados") + str(gates_ocupados) + "\n")

def actualizar_pantalla_gates():
    caja.delete(1.0, tk.END)
    if bcn is None:
        return
    ocupacion = GateOccupancy(bcn)
    caja.insert(tk.END, T("ocu_titulo") + bcn.code + " ===\n\n")
    terminal_actual = ""
    area_actual = ""
    i = 0
    while i < len(ocupacion):
        g = ocupacion[i]
        if g[0] != terminal_actual:
            terminal_actual = g[0]
            area_actual = ""
            caja.insert(tk.END, T("ocu_terminal") + terminal_actual + "\n")
        if g[1] != area_actual:
            area_actual = g[1]
            caja.insert(tk.END, T("ocu_area") + area_actual + ":\n")
        caja.insert(tk.END, "    " + g[2] + " -> " + g[3])
        if g[3] == "Ocupado":
            caja.insert(tk.END, " (" + g[4] + ")")
        caja.insert(tk.END, "\n")
        i += 1


# =====================================================================
# FUNCIONES - LIBERAR GATE (FreeGate UI)
# =====================================================================

def btn_liberar_gate_click():
    if bcn is None:
        messagebox.showerror(T("msg_error"), T("msg_primero_estructura2"))
        return
    aircraft_id = entrada_liberar.get().strip().upper()  # upper() aquí
    if aircraft_id == "":
        messagebox.showwarning(T("msg_aviso"), T("msg_liberar_vacio"))
        return
    resultado = FreeGate(bcn, aircraft_id)
    if resultado == 0:
        entrada_liberar.delete(0, tk.END)  # limpiar si éxito
        actualizar_pantalla_gates()
        messagebox.showinfo(T("msg_liberar_titulo"),
            T("msg_liberar_ok") + aircraft_id)
    else:
        messagebox.showerror(T("msg_error"),
            T("msg_liberar_error") + aircraft_id)


# =====================================================================
# FUNCIONES - REASIGNAR GATE MANUALMENTE
# =====================================================================

def btn_reasignar_gate_click():
    if bcn is None:
        messagebox.showerror(T("msg_error"), T("msg_primero_estructura2"))
        return

    aircraft_id = entrada_reasignar_avion.get().strip().upper()  # upper() aquí
    nuevo_gate_nombre = entrada_reasignar_gate.get().strip().upper()  # upper() aquí

    if aircraft_id == "" or nuevo_gate_nombre == "":
        messagebox.showwarning(T("msg_aviso"), T("msg_reasignar_vacio"))
        return

    gate_destino = None
    i = 0
    while i < len(bcn.terminals) and gate_destino is None:
        terminal = bcn.terminals[i]
        j = 0
        while j < len(terminal.boarding_areas) and gate_destino is None:
            area = terminal.boarding_areas[j]
            k = 0
            while k < len(area.gates) and gate_destino is None:
                if area.gates[k].name == nuevo_gate_nombre:
                    gate_destino = area.gates[k]
                k += 1
            j += 1
        i += 1

    if gate_destino is None:
        messagebox.showerror(T("msg_error"),
            T("msg_reasignar_gate_nf") + nuevo_gate_nombre)
        return

    if gate_destino.occupied and gate_destino.aircraft_id != aircraft_id:
        messagebox.showerror(T("msg_error"), T("msg_reasignar_ocupado"))
        return

    resultado_liberar = FreeGate(bcn, aircraft_id)
    if resultado_liberar != 0:
        messagebox.showinfo(T("msg_info"), T("msg_reasignar_avion_nf"))

    gate_destino.occupied = True
    gate_destino.aircraft_id = aircraft_id

    # Limpiar campos después de reasignar
    entrada_reasignar_avion.delete(0, tk.END)
    entrada_reasignar_gate.delete(0, tk.END)

    actualizar_pantalla_gates()
    messagebox.showinfo(T("msg_reasignar_titulo"),
        T("msg_reasignar_ok") + aircraft_id +
        T("msg_reasignar_nuevo") + nuevo_gate_nombre)


# =====================================================================
# FUNCIONES - VERSION 4
# =====================================================================

def btn_cargar_salidas_click():
    global lista_vuelos
    salidas = LoadDepartures("Departures.txt")
    if len(salidas) == 0:
        messagebox.showwarning(T("msg_aviso"), T("msg_dep_error"))
        return
    fusionados = MergeMovements(lista_vuelos, salidas)
    if len(fusionados) == 0:
        messagebox.showwarning(T("msg_aviso"), T("msg_fusion_error"))
        return
    lista_vuelos = fusionados
    actualizar_pantalla_vuelos_v4()
    messagebox.showinfo(T("msg_salidas_titulo"), T("msg_salidas_ok"))

def btn_aviones_nocturnos_click():
    if len(lista_vuelos) == 0:
        messagebox.showwarning(T("msg_aviso"), T("msg_carga_primero_v"))
        return
    nocturnos = NightAircraft(lista_vuelos)
    caja.delete(1.0, tk.END)
    caja.insert(tk.END, T("msg_nocturnos_titulo"))
    i = 0
    while i < len(nocturnos):
        ac = nocturnos[i]
        caja.insert(tk.END,
            T("avion_label") + str(ac.aircraft) +
            T("destino_label") + str(ac.destination) +
            T("hora_salida") + str(ac.departure_time) + "\n")
        i += 1
    if len(nocturnos) == 0:
        caja.insert(tk.END, T("msg_no_nocturnos"))

def btn_asignar_nocturnos_click():
    if bcn is None:
        messagebox.showerror(T("msg_error"), T("msg_primero_estructura2"))
        return
    if len(lista_vuelos) == 0:
        messagebox.showerror(T("msg_error"), T("msg_primero_vuelos"))
        return
    nocturnos = NightAircraft(lista_vuelos)
    if len(nocturnos) == 0:
        messagebox.showinfo(T("msg_info"), T("msg_no_nocturnos2"))
        return
    AssignNightGates(bcn, nocturnos)
    actualizar_pantalla_gates()
    messagebox.showinfo(T("msg_nocturnos_titulo2"), T("msg_nocturnos_ok"))

def btn_asignar_por_hora_click():
    if bcn is None:
        messagebox.showerror(T("msg_error"), T("msg_primero_estructura2"))
        return
    if len(lista_vuelos) == 0:
        messagebox.showerror(T("msg_error"), T("msg_primero_vuelos"))
        return
    hora = entrada_hora.get()
    partes = hora.split(":")
    if len(partes) != 2:
        messagebox.showerror(T("msg_error"), T("msg_hora_formato"))
        return
    try:
        h = int(partes[0])
        m = int(partes[1])
        if h < 0 or h > 23 or m < 0 or m > 59:
            messagebox.showerror(T("msg_error"), T("msg_hora_rango"))
            return
    except ValueError:
        messagebox.showerror(T("msg_error"), T("msg_hora_nums"))
        return
    no_asig = AssignGatesAtTime(bcn, lista_vuelos, hora)
    actualizar_pantalla_gates()
    messagebox.showinfo(T("msg_hora_titulo"),
        T("msg_hora_ok") + hora + T("msg_hora_ok2") + str(no_asig))

def actualizar_pantalla_vuelos_v4():
    caja.delete(1.0, tk.END)
    i = 0
    while i < len(lista_vuelos):
        v = lista_vuelos[i]
        linea = T("avion_label") + str(v.aircraft)
        if v.origin != "":
            linea += T("origen_label") + str(v.origin) + T("hora_llegada") + str(v.time)
        if v.destination != "":
            linea += T("destino_label") + str(v.destination) + T("hora_salida") + str(v.departure_time)
        caja.insert(tk.END, linea + "\n")
        i += 1


# =====================================================================
# GRÁFICOS
# =====================================================================

canvas_picture = None

def mostrar_grafico_en_interfaz(figura):
    global canvas_picture
    if canvas_picture is not None:
        canvas_picture.get_tk_widget().destroy()

    # Reactiva el espacio de visualización
    root.rowconfigure(1, weight=2)
    panel_graficas.grid_propagate(False)

    figura.set_size_inches(8, 6)
    canvas_obj = FigureCanvasTkAgg(figura, master=panel_graficas)
    canvas_obj.draw()
    canvas_picture = canvas_obj
    widget = canvas_obj.get_tk_widget()
    widget.grid(row=0, column=0, padx=5, pady=5)
    root.update_idletasks()

def btn_borrar_grafica_click():
    global canvas_picture
    if canvas_picture is not None:
        canvas_picture.get_tk_widget().destroy()
        canvas_picture = None

    # Colapsa la fila de visualización para que la consola recupere el espacio
    root.rowconfigure(1, weight=0, minsize=0)
    panel_graficas.configure(height=1)
    panel_graficas.grid_propagate(True)
    root.update_idletasks()

def btn_grafica_aeropuertos_click():
    if not lista_trabajo:
        messagebox.showwarning(T("msg_aviso"), T("msg_carga_primero_ap"))
        return
    figura = PlotAirports(lista_trabajo)
    mostrar_grafico_en_interfaz(figura)

def btn_grafica_llegadas_click():
    if len(lista_vuelos) == 0:
        messagebox.showwarning(T("msg_error"), T("msg_carga_primero_v"))
        return
    fig = PlotArrivals(lista_vuelos)
    if fig is not None:
        mostrar_grafico_en_interfaz(fig)

def btn_grafica_airlines_click():
    if len(lista_vuelos) == 0:
        messagebox.showwarning(T("msg_error"), T("msg_carga_primero_v"))
        return
    fig = PlotAirlines(lista_vuelos)
    if fig is not None:
        mostrar_grafico_en_interfaz(fig)

def btn_grafica_schengen_click():
    if len(lista_vuelos) == 0:
        messagebox.showwarning(T("msg_error"), T("msg_carga_primero_v"))
        return
    fig = PlotFlightsType(lista_vuelos)
    if fig is not None:
        mostrar_grafico_en_interfaz(fig)

def btn_grafica_gates_click():
    if bcn is None:
        messagebox.showerror(T("msg_error"), T("msg_primero_estructura2"))
        return
    fig = PlotGates(bcn)
    if fig is not None:
        mostrar_grafico_en_interfaz(fig)

def btn_grafica_ocupacion_dia_click():
    if bcn is None:
        messagebox.showerror(T("msg_error"), T("msg_primero_estructura2"))
        return
    if len(lista_vuelos) == 0:
        messagebox.showerror(T("msg_error"), T("msg_primero_vuelos"))
        return
    fig = PlotDayOccupancy(bcn, lista_vuelos)
    if fig is not None:
        mostrar_grafico_en_interfaz(fig)


# =====================================================================
# PALETA PASTEL
# =====================================================================

BG_APP      = "#F5F0FB"
BG_PANEL    = "#EDE6F7"
BG_CONSOLA  = "#FDFBFF"
C_TEXT_DARK = "#3D2B5A"
C_LABEL_FG  = "#5C4080"

C_AP_BG     = "#DFF0FF"; C_AP_FG  = "#1E4E7C"; C_AP_HOVER  = "#C5E3F8"
C_VU_BG     = "#FFE6EF"; C_VU_FG  = "#7A1E40"; C_VU_HOVER  = "#FFD0E2"
C_GA_BG     = "#EAE0FF"; C_GA_FG  = "#4A2878"; C_GA_HOVER  = "#D9C8FA"
C_V4_BG     = "#FFF3DC"; C_V4_FG  = "#7A4A10"; C_V4_HOVER  = "#FFE8BE"
C_GR_BG     = "#D8F5E8"; C_GR_FG  = "#1A5E3C"; C_GR_HOVER  = "#BEF0D4"
C_MN_BG     = "#FFE8D8"; C_MN_FG  = "#7A3010"; C_MN_HOVER  = "#FFD5B8"
C_DEL_BG    = "#FFD8D8"; C_DEL_FG = "#8A1A1A"; C_DEL_HOVER = "#FFC0C0"
C_ADD_BG    = "#D8EEFF"; C_ADD_FG = "#1A4E7A"; C_ADD_HOVER = "#BEE0F8"


# =====================================================================
# INICIO
# =====================================================================

idioma_actual = mostrar_splash() or "es"

root = tk.Tk()
root.title(T("titulo_app"))
root.geometry("1150x650")
root.configure(bg=BG_APP)

# ---- ESTILOS ----
style = ttk.Style()
style.theme_use("clam")

style.configure("Panel.TLabelframe",
    background=BG_PANEL, padding=4, relief="flat", borderwidth=1)
style.configure("Panel.TLabelframe.Label",
    font=("Microsoft YaHei", 8, "bold"), foreground=C_LABEL_FG, background=BG_PANEL)

style.configure("Light.TLabelframe",
    background=BG_APP, padding=4, relief="flat", borderwidth=1)
style.configure("Light.TLabelframe.Label",
    font=("Microsoft YaHei", 8, "bold"), foreground=C_LABEL_FG, background=BG_APP)

style.configure("TFrame", background=BG_APP)
style.configure("Scroll.TFrame", background=BG_PANEL)

def mk(name, bg, fg, hov):
    style.configure(name, background=bg, foreground=fg,
        font=("Microsoft YaHei", 8), padding=4, relief="flat", borderwidth=0)
    style.map(name, background=[("active", hov)], foreground=[("active", fg)])

mk("AP.TButton",  C_AP_BG,  C_AP_FG,  C_AP_HOVER)
mk("VU.TButton",  C_VU_BG,  C_VU_FG,  C_VU_HOVER)
mk("GA.TButton",  C_GA_BG,  C_GA_FG,  C_GA_HOVER)
mk("V4.TButton",  C_V4_BG,  C_V4_FG,  C_V4_HOVER)
mk("GR.TButton",  C_GR_BG,  C_GR_FG,  C_GR_HOVER)
mk("MN.TButton",  C_MN_BG,  C_MN_FG,  C_MN_HOVER)
mk("ADD.TButton", C_ADD_BG, C_ADD_FG, C_ADD_HOVER)
style.configure("DEL.TButton",
    background=C_DEL_BG, foreground=C_DEL_FG,
    font=("Microsoft YaHei", 8, "bold"), padding=4, relief="flat", borderwidth=0)
style.map("DEL.TButton",
    background=[("active", C_DEL_HOVER)], foreground=[("active", C_DEL_FG)])

style.configure("TLabel",
    font=("Microsoft YaHei", 8), background=BG_PANEL, foreground=C_LABEL_FG)
style.configure("TEntry",
    font=("Microsoft YaHei", 8), fieldbackground="#FFFFFF")

# ---- GRID PRINCIPAL ----
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)
root.rowconfigure(0, weight=3)
root.rowconfigure(1, weight=2)


# =====================================================================
# PANEL IZQUIERDO CON SCROLL
# =====================================================================

# Contenedor exterior que ocupa el espacio en el grid
outer_left = tk.Frame(root, bg=BG_APP, width=220)
outer_left.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=8, pady=8)
outer_left.grid_propagate(False)  # fija el ancho
outer_left.rowconfigure(0, weight=1)
outer_left.columnconfigure(0, weight=1)

# Canvas + scrollbar para hacer scroll vertical
left_canvas = tk.Canvas(outer_left, bg=BG_PANEL,
                         highlightthickness=0, bd=0)
left_scrollbar = tk.Scrollbar(outer_left, orient="vertical",
                               command=left_canvas.yview)
left_canvas.configure(yscrollcommand=left_scrollbar.set)

left_scrollbar.grid(row=0, column=1, sticky="ns")
left_canvas.grid(row=0, column=0, sticky="nsew")

# Frame interior que va dentro del canvas (aquí ponemos todos los widgets)
left_panel = tk.Frame(left_canvas, bg=BG_PANEL)
left_panel_window = left_canvas.create_window(
    (0, 0), window=left_panel, anchor="nw")

# Ajustar el ancho del frame interior al canvas y actualizar scrollregion
def _on_left_panel_configure(event):
    left_canvas.configure(scrollregion=left_canvas.bbox("all"))

def _on_left_canvas_configure(event):
    left_canvas.itemconfig(left_panel_window, width=event.width)

left_panel.bind("<Configure>", _on_left_panel_configure)
left_canvas.bind("<Configure>", _on_left_canvas_configure)

# Scroll con rueda del ratón
def _on_mousewheel(event):
    left_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

left_canvas.bind_all("<MouseWheel>", _on_mousewheel)
# Linux/Mac también:
left_canvas.bind_all("<Button-4>", lambda e: left_canvas.yview_scroll(-1, "units"))
left_canvas.bind_all("<Button-5>", lambda e: left_canvas.yview_scroll(1, "units"))

left_panel.columnconfigure(0, weight=1)

# Helper para crear LabelFrames dentro del panel con scroll
def make_section(parent, text_key, row):
    lf = tk.LabelFrame(parent, text=text_key,
        bg=BG_PANEL, fg=C_LABEL_FG,
        font=("Microsoft YaHei", 8, "bold"),
        relief="flat", bd=1, padx=4, pady=4)
    lf.grid(row=row, column=0, sticky="ew", pady=3, padx=2)
    lf.columnconfigure(0, weight=1)
    return lf

def make_btn(parent, text, style_name, command):
    """Crea un botón tk normal con el estilo de color correspondiente."""
    color_map = {
        "AP.TButton":  (C_AP_BG,  C_AP_FG,  C_AP_HOVER),
        "VU.TButton":  (C_VU_BG,  C_VU_FG,  C_VU_HOVER),
        "GA.TButton":  (C_GA_BG,  C_GA_FG,  C_GA_HOVER),
        "V4.TButton":  (C_V4_BG,  C_V4_FG,  C_V4_HOVER),
        "MN.TButton":  (C_MN_BG,  C_MN_FG,  C_MN_HOVER),
        "ADD.TButton": (C_ADD_BG, C_ADD_FG, C_ADD_HOVER),
        "DEL.TButton": (C_DEL_BG, C_DEL_FG, C_DEL_HOVER),
        "GR.TButton":  (C_GR_BG,  C_GR_FG,  C_GR_HOVER),
    }
    bg, fg, hov = color_map.get(style_name, (BG_PANEL, C_TEXT_DARK, BG_APP))
    btn = tk.Button(parent, text=text, bg=bg, fg=fg,
        activebackground=hov, activeforeground=fg,
        font=("Microsoft YaHei", 8), relief="flat", bd=0,
        padx=4, pady=4, cursor="hand2", command=command)
    btn.grid(sticky="ew", pady=2, padx=4)
    btn.bind("<Enter>", lambda e, b=btn, h=hov: b.configure(bg=h))
    btn.bind("<Leave>", lambda e, b=btn, n=bg: b.configure(bg=n))
    return btn

# ---- SECCIÓN: AEROPUERTOS ----
row_idx = 0
acciones = make_section(left_panel, "  ✈  " + T("aeropuertos"), row_idx)
row_idx += 1
for txt, cmd, sty in [
    (T("cargar_aeropuertos"), btn_cargar_click,           "AP.TButton"),
    (T("guardar_schengen"),   btn_guardar_click,           "AP.TButton"),
    (T("ver_google_earth"),   btn_mapa_aeropuertos_click,  "AP.TButton"),
]:
    make_btn(acciones, txt, sty, cmd)

# ---- SECCIÓN: AÑADIR / BORRAR ----
# ---- SECCIÓN: AÑADIR / BORRAR ----
datos = make_section(left_panel, "  +/-  " + T("anadir_borrar"), row_idx)
row_idx += 1

entrada_cod = None
entrada_lat = None
entrada_lon = None

fields = [("icao_label", 14), ("lat_label", 14), ("lon_label", 14)]
fila_num = 0
for key, w in fields:
    fila = tk.Frame(datos, bg=BG_PANEL)
    fila.grid(row=fila_num, column=0, sticky="ew", pady=2, padx=4)
    tk.Label(fila, text=T(key), width=14, anchor="w",
             bg=BG_PANEL, fg=C_LABEL_FG, font=("Microsoft YaHei", 8)).pack(side=tk.LEFT)
    e = ttk.Entry(fila, width=w)
    e.pack(side=tk.LEFT, padx=3)
    if key == "icao_label":
        entrada_cod = e
    elif key == "lat_label":
        entrada_lat = e
    else:
        entrada_lon = e
    fila_num += 1

fila_btns = tk.Frame(datos, bg=BG_PANEL)
fila_btns.grid(row=fila_num, column=0, sticky="ew", pady=4, padx=4)
tk.Button(fila_btns, text=T("anadir"), bg=C_ADD_BG, fg=C_ADD_FG,
    activebackground=C_ADD_HOVER, font=("Microsoft YaHei", 10),
    relief="flat", bd=0, padx=4, pady=4, cursor="hand2",
    command=btn_anadir_click).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
tk.Button(fila_btns, text=T("borrar"), bg=C_DEL_BG, fg=C_DEL_FG,
    activebackground=C_DEL_HOVER, font=("Microsoft YaHei", 10, "bold"),
    relief="flat", bd=0, padx=4, pady=4, cursor="hand2",
    command=btn_borrar_click).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
# ---- SECCIÓN: VUELOS ----
vuelos_frame = make_section(left_panel, "  🛬  " + T("gestion_vuelos"), row_idx)
row_idx += 1
for txt, cmd, sty in [
    (T("cargar_vuelos"),   btn_cargar_vuelos_click,        "VU.TButton"),
    (T("trayectorias"),    btn_mapa_kml_click,             "VU.TButton"),
    (T("filtrar_largos"),  btn_vuelos_largos_click,        "VU.TButton"),
    (T("guardar_vuelos"),  btn_guardar_vuelos_fichero_click,"VU.TButton"),
    (T("exportar_largos"), btn_exportar_vuelos_largos_click,"VU.TButton"),
]:
    make_btn(vuelos_frame, txt, sty, cmd)

# ---- SECCIÓN: GATES ----
gates_frame = make_section(left_panel, "  🚪  " + T("gestion_gates"), row_idx)
row_idx += 1
for txt, cmd, sty in [
    (T("cargar_estructura"), btn_cargar_estructura_click, "GA.TButton"),
    (T("asignar_gates"),     btn_asignar_gates_click,     "GA.TButton"),
    (T("ver_ocupacion"),     btn_ver_ocupacion_click,     "GA.TButton"),
]:
    make_btn(gates_frame, txt, sty, cmd)

# ---- SECCIÓN: V4 - SALIDAS Y DINÁMICA ----
v4_frame = make_section(left_panel, "  🌙  " + T("salidas_dinamica"), row_idx)
row_idx += 1
make_btn(v4_frame, T("cargar_salidas"),    "V4.TButton", btn_cargar_salidas_click)
make_btn(v4_frame, T("ver_nocturnos"),     "V4.TButton", btn_aviones_nocturnos_click)
make_btn(v4_frame, T("asignar_nocturnos"), "V4.TButton", btn_asignar_nocturnos_click)

fila_hora = tk.Frame(v4_frame, bg=BG_PANEL)
fila_hora.grid(sticky="ew", pady=2, padx=4)
tk.Label(fila_hora, text=T("hora_label"), bg=BG_PANEL, fg=C_LABEL_FG,
         font=("Segoe UI", 8)).pack(side=tk.LEFT)
entrada_hora = ttk.Entry(fila_hora, width=7)
entrada_hora.pack(side=tk.LEFT, padx=4)
entrada_hora.insert(0, "08:00")

make_btn(v4_frame, T("asignar_hora"), "V4.TButton", btn_asignar_por_hora_click)

# ---- SECCIÓN: GESTIÓN MANUAL DE GATES ----
manual_frame = make_section(left_panel, "  ✏️  " + T("gestion_manual"), row_idx)
row_idx += 1

# --- Sub-sección: Liberar Gate ---
sep_lib = tk.Frame(manual_frame, bg=BG_PANEL)
sep_lib.grid(sticky="ew", pady=(4, 2), padx=4)
tk.Label(sep_lib, text="🔓 " + T("liberar_gate_label"),
         bg=BG_PANEL, fg=C_LABEL_FG,
         font=("Segoe UI", 8, "bold")).pack(anchor="w")

fila_lib = tk.Frame(manual_frame, bg=BG_PANEL)
fila_lib.grid(sticky="ew", pady=2, padx=4)
entrada_liberar = ttk.Entry(fila_lib, width=14)
entrada_liberar.pack(side=tk.LEFT, padx=(0, 4))
tk.Button(fila_lib, text=T("liberar_gate_btn"),
    bg=C_MN_BG, fg=C_MN_FG, activebackground=C_MN_HOVER,
    font=("Segoe UI", 8), relief="flat", bd=0, padx=4, pady=3,
    cursor="hand2", command=btn_liberar_gate_click).pack(side=tk.LEFT, fill=tk.X, expand=True)

# Separador visual
tk.Frame(manual_frame, height=1, bg="#D4C5E8").grid(
    sticky="ew", pady=6, padx=6)

# --- Sub-sección: Reasignar Gate ---
sep_rea = tk.Frame(manual_frame, bg=BG_PANEL)
sep_rea.grid(sticky="ew", pady=(2, 2), padx=4)
tk.Label(sep_rea, text="🔄 " + T("reasignar_titulo"),
         bg=BG_PANEL, fg=C_LABEL_FG,
         font=("Segoe UI", 8, "bold")).pack(anchor="w")

fila_rea1 = tk.Frame(manual_frame, bg=BG_PANEL)
fila_rea1.grid(sticky="ew", pady=2, padx=4)
tk.Label(fila_rea1, text=T("reasignar_avion_label"), width=12, anchor="w",
         bg=BG_PANEL, fg=C_LABEL_FG, font=("Segoe UI", 8)).pack(side=tk.LEFT)
entrada_reasignar_avion = ttk.Entry(fila_rea1, width=14)
entrada_reasignar_avion.pack(side=tk.LEFT, padx=3)

fila_rea2 = tk.Frame(manual_frame, bg=BG_PANEL)
fila_rea2.grid(sticky="ew", pady=2, padx=4)
tk.Label(fila_rea2, text=T("reasignar_gate_label"), width=12, anchor="w",
         bg=BG_PANEL, fg=C_LABEL_FG, font=("Segoe UI", 8)).pack(side=tk.LEFT)
entrada_reasignar_gate = ttk.Entry(fila_rea2, width=14)
entrada_reasignar_gate.pack(side=tk.LEFT, padx=3)

make_btn(manual_frame, T("reasignar_btn"), "MN.TButton", btn_reasignar_gate_click)


# =====================================================================
# CONSOLA
# =====================================================================
consola = ttk.LabelFrame(root,
    text="  📋  " + T("consola"), style="Panel.TLabelframe")
consola.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)

scrollbar_caja = tk.Scrollbar(consola, bg=BG_PANEL, troughcolor=BG_APP)
scrollbar_caja.pack(side=tk.RIGHT, fill=tk.Y)

caja = tk.Text(consola,
    font=("Consolas", 9),
    bg=BG_CONSOLA, fg=C_TEXT_DARK,
    insertbackground=C_TEXT_DARK,
    selectbackground="#D8C8F0", selectforeground=C_TEXT_DARK,
    relief="flat", bd=0, padx=8, pady=6,
    yscrollcommand=scrollbar_caja.set)
caja.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
scrollbar_caja.config(command=caja.yview)


# =====================================================================
# PANEL GRÁFICAS
# =====================================================================
panel_graficas = ttk.LabelFrame(root,
    text="  📊  " + T("visualizacion"), style="Panel.TLabelframe")
panel_graficas.grid(row=1, column=1, padx=8, pady=4, sticky="nsew")
panel_graficas.rowconfigure(0, weight=1)
panel_graficas.columnconfigure(0, weight=1)


# =====================================================================
# BARRA BOTONES GRÁFICAS
# =====================================================================
graficas = ttk.LabelFrame(root,
    text="  " + T("graficas"), style="Light.TLabelframe")
graficas.grid(row=2, column=0, columnspan=2, sticky="ew", padx=8, pady=4)
graficas.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

botones_graficas = [
    (T("graf_schengen_ap"), btn_grafica_aeropuertos_click,  "GR.TButton"),
    (T("graf_llegadas"),    btn_grafica_llegadas_click,     "GR.TButton"),
    (T("graf_aerolineas"),  btn_grafica_airlines_click,     "GR.TButton"),
    (T("graf_schengen_v"),  btn_grafica_schengen_click,     "GR.TButton"),
    (T("graf_gates"),       btn_grafica_gates_click,        "GR.TButton"),
    (T("graf_ocupacion"),   btn_grafica_ocupacion_dia_click,"GR.TButton"),
    (T("borrar_grafica"),   btn_borrar_grafica_click,       "DEL.TButton"),
]

for i, (txt, cmd, est) in enumerate(botones_graficas):
    ttk.Button(graficas, text=txt, style=est,
               command=cmd).grid(row=0, column=i, sticky="ew", padx=3, pady=4)

#======FUNCIONES EXTRA======
# =====================================================================
# SIMULACIÓN ANIMADA — ventana flotante con mapa de gates en vivo
#
# INTEGRACIÓN EN main.py  (4 pasos):
#
# 1) En "VARIABLES GLOBALES" añade:
#       ventana_sim  = None
#       progreso_sim = None
#       canvas_sim   = None      ← canvas matplotlib de la ventana
#
# 2) Copia las FUNCIONES en la sección "FUNCIONES - GATES"
#
# 3) Copia el bloque UI justo después de los 3 botones de gates
#
# 4) Asegúrate de que LEBL.py tiene GetGateStateAtTime
# =====================================================================


# ─────────────────────────────────────────────────────────────────────
# NUEVAS VARIABLES GLOBALES
# ─────────────────────────────────────────────────────────────────────
ventana_sim  = None
progreso_sim = None
canvas_sim   = None      # FigureCanvasTkAgg dentro de la ventana


# ─────────────────────────────────────────────────────────────────────
# FUNCIONES
# ─────────────────────────────────────────────────────────────────────

def _hora_a_str(h):
    if h < 10:
        return "0" + str(h) + ":00"
    return str(h) + ":00"


def _dibujar_mapa_sim(estado, aviones, hora):
    """
    Redibuja el mapa de gates en la ventana de simulación.
    'estado' es la lista devuelta por GetGateStateAtTime:
      (terminal_name, area_name, gate_name, occupied, aircraft_id)
    """
    global canvas_sim
    if canvas_sim is None:
        return

    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    # ── Agrupar por terminal y área ───────────────────────────────
    estructura = {}       # {terminal: {area: [(gate_name, occupied, ac_id)]}}
    for t_name, a_name, g_name, ocupado, ac_id in estado:
        if t_name not in estructura:
            estructura[t_name] = {}
        if a_name not in estructura[t_name]:
            estructura[t_name][a_name] = []
        estructura[t_name][a_name].append((g_name, ocupado, ac_id))

    terminales = list(estructura.keys())
    num_t = len(terminales)
    if num_t == 0:
        return

    # ── Figura ────────────────────────────────────────────────────
    fig = canvas_sim.figure
    fig.clf()

    hora_str = _hora_a_str(hora)
    fig.suptitle("Mapa de gates  —  " + hora_str +
                 "    Aviones en tierra: " + str(aviones),
                 fontsize=11, fontweight="bold", color="#3D2B5A")

    axes = fig.subplots(1, num_t)
    if num_t == 1:
        axes = [axes]

    for t_idx, t_name in enumerate(terminales):
        ax = axes[t_idx]
        ax.set_title("Terminal " + t_name, fontsize=10,
                     fontweight="bold", color="#4A2878")
        ax.axis("off")

        areas = list(estructura[t_name].keys())
        # Altura total necesaria
        total_filas = 0
        for a_name in areas:
            gates = estructura[t_name][a_name]
            filas = (len(gates) + 9) // 10   # 10 gates por fila
            total_filas += filas + 1          # +1 para la etiqueta del área

        ax.set_xlim(-0.5, 10)
        ax.set_ylim(-0.5, max(total_filas * 1.2, 4))

        y_pos = max(total_filas * 1.2, 4) - 0.8

        for a_name in areas:
            gates = estructura[t_name][a_name]

            # Etiqueta del área
            ax.text(-0.3, y_pos, a_name,
                    fontsize=8, fontweight="bold", color="#5C3D8F")
            y_pos -= 0.7

            x_pos = 0
            for g_name, ocupado, ac_id in gates:
                color = "#e74c3c" if ocupado else "#2ecc71"

                rect = patches.FancyBboxPatch(
                    (x_pos + 0.05, y_pos - 0.45), 0.82, 0.38,
                    boxstyle="round,pad=0.04",
                    linewidth=0.8, edgecolor="#555",
                    facecolor=color, alpha=0.85)
                ax.add_patch(rect)

                label = ac_id[:4] if ocupado else "·"
                ax.text(x_pos + 0.46, y_pos - 0.26, label,
                        ha="center", va="center",
                        fontsize=6.5, fontweight="bold",
                        color="white")

                x_pos += 1
                if x_pos >= 10:
                    x_pos = 0
                    y_pos -= 0.7

            y_pos -= 0.9

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    canvas_sim.draw()


def _crear_ventana_simulacion():
    """Crea (o reactiva) la ventana flotante de simulación."""
    global ventana_sim, progreso_sim, canvas_sim
    global btn_play, btn_stop, lbl_hora_sim

    if ventana_sim is not None and tk.Toplevel.winfo_exists(ventana_sim):
        ventana_sim.lift()
        return

    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    ventana_sim = tk.Toplevel(root)
    ventana_sim.title("Simulación — " + (bcn.code if bcn else ""))
    ventana_sim.geometry("780x560")
    ventana_sim.configure(bg=BG_APP)
    ventana_sim.resizable(True, True)

    # ── Cabecera ──────────────────────────────────────────────────
    cab = tk.Frame(ventana_sim, bg=BG_PANEL, pady=8)
    cab.pack(fill=tk.X)

    tk.Label(cab, text="✈  Ocupación de gates en tiempo real",
             font=("Microsoft YaHei", 10, "bold"),
             bg=BG_PANEL, fg=C_TEXT_DARK).pack(side=tk.LEFT, padx=14)

    lbl_hora_sim = tk.Label(cab, text="00:00",
                             font=("Microsoft YaHei", 18, "bold"),
                             bg=BG_PANEL, fg="#5C3D8F")
    lbl_hora_sim.pack(side=tk.RIGHT, padx=14)

    # ── Leyenda ───────────────────────────────────────────────────
    ley = tk.Frame(ventana_sim, bg=BG_APP)
    ley.pack(fill=tk.X, padx=14, pady=(4, 0))

    for color, texto in [("#2ecc71", "Libre"), ("#e74c3c", "Ocupado")]:
        dot = tk.Label(ley, text="■", fg=color, bg=BG_APP,
                       font=("Microsoft YaHei", 12))
        dot.pack(side=tk.LEFT)
        tk.Label(ley, text=texto + "   ", bg=BG_APP, fg=C_LABEL_FG,
                 font=("Microsoft YaHei", 8)).pack(side=tk.LEFT)

    # ── Barra de progreso ─────────────────────────────────────────
    progreso_sim = ttk.Progressbar(ventana_sim, orient="horizontal",
                                    mode="determinate", maximum=100)
    progreso_sim.pack(fill=tk.X, padx=12, pady=4)

    # ── Botones ───────────────────────────────────────────────────
    bfr = tk.Frame(ventana_sim, bg=BG_APP)
    bfr.pack(fill=tk.X, padx=12, pady=(0, 6))

    btn_play = tk.Button(bfr, text="▶  Play",
        bg="#D8F5E8", fg="#1A5E3C",
        activebackground="#BEF0D4", activeforeground="#1A5E3C",
        font=("Microsoft YaHei", 9, "bold"),
        relief="flat", bd=0, padx=12, pady=6,
        cursor="hand2", command=_iniciar_simulacion)
    btn_play.pack(side=tk.LEFT, padx=(0, 6))

    btn_stop = tk.Button(bfr, text="⏹  Stop",
        bg="#FFD8D8", fg="#8A1A1A",
        activebackground="#FFC0C0", activeforeground="#8A1A1A",
        font=("Microsoft YaHei", 9, "bold"),
        relief="flat", bd=0, padx=12, pady=6,
        cursor="hand2", command=_parar_simulacion,
        state=tk.DISABLED)
    btn_stop.pack(side=tk.LEFT, padx=(0, 6))

    tk.Button(bfr, text="↺  Reiniciar",
        bg="#EDE6F7", fg="#5C3D8F",
        activebackground="#D9C8FA", activeforeground="#5C3D8F",
        font=("Microsoft YaHei", 9),
        relief="flat", bd=0, padx=12, pady=6,
        cursor="hand2", command=_reiniciar_simulacion).pack(side=tk.LEFT)

    # ── Canvas matplotlib ─────────────────────────────────────────
    fig = plt.Figure(figsize=(9, 5), facecolor="#F5F0FB")
    canvas_sim = FigureCanvasTkAgg(fig, master=ventana_sim)
    canvas_sim.get_tk_widget().pack(fill=tk.BOTH, expand=True,
                                     padx=10, pady=(0, 10))

    # Dibujo inicial vacío con mensaje
    ax = fig.add_subplot(111)
    ax.axis("off")
    ax.text(0.5, 0.5, "Pulsa  ▶ Play  para iniciar la simulación",
            ha="center", va="center", fontsize=13,
            color="#9B7EC8", transform=ax.transAxes)
    canvas_sim.draw()


def _tick_simulacion():
    global simulacion_activa, hora_simulacion

    if not simulacion_activa:
        return
    if bcn is None or len(lista_vuelos) == 0:
        _parar_simulacion()
        return

    hora_str = _hora_a_str(hora_simulacion)

    if lbl_hora_sim and tk.Toplevel.winfo_exists(ventana_sim):
        lbl_hora_sim.config(text=hora_str)
    if progreso_sim:
        progreso_sim.config(value=int(hora_simulacion * 100 / 23))

    estado, aviones = GetGateStateAtTime(bcn, lista_vuelos, hora_str)
    _dibujar_mapa_sim(estado, aviones, hora_simulacion)

    if hora_simulacion < 23:
        hora_simulacion += 1
        root.after(1500, _tick_simulacion)
    else:
        progreso_sim.config(value=100)
        _parar_simulacion()


def _iniciar_simulacion():
    global simulacion_activa, hora_simulacion
    if bcn is None:
        messagebox.showerror(T("msg_error"), T("msg_primero_estructura2"))
        return
    if len(lista_vuelos) == 0:
        messagebox.showerror(T("msg_error"), T("msg_primero_vuelos"))
        return
    simulacion_activa = True
    hora_simulacion   = 0
    if btn_play:
        btn_play.config(state=tk.DISABLED)
    if btn_stop:
        btn_stop.config(state=tk.NORMAL)
    _tick_simulacion()


def _parar_simulacion():
    global simulacion_activa
    simulacion_activa = False
    if btn_play:
        btn_play.config(state=tk.NORMAL)
    if btn_stop:
        btn_stop.config(state=tk.DISABLED)


def _reiniciar_simulacion():
    import matplotlib.pyplot as plt
    _parar_simulacion()
    global hora_simulacion
    hora_simulacion = 0
    if lbl_hora_sim:
        lbl_hora_sim.config(text="00:00")
    if progreso_sim:
        progreso_sim.config(value=0)
    if canvas_sim:
        fig = canvas_sim.figure
        fig.clf()
        ax = fig.add_subplot(111)
        ax.axis("off")
        ax.text(0.5, 0.5, "Pulsa  ▶ Play  para iniciar la simulación",
                ha="center", va="center", fontsize=13,
                color="#9B7EC8", transform=ax.transAxes)
        canvas_sim.draw()


def btn_abrir_simulacion_click():
    if bcn is None:
        messagebox.showerror(T("msg_error"), T("msg_primero_estructura2"))
        return
    if len(lista_vuelos) == 0:
        messagebox.showerror(T("msg_error"), T("msg_primero_vuelos"))
        return
    _crear_ventana_simulacion()


# ─────────────────────────────────────────────────────────────────────
# ▼ UI — pegar justo DESPUÉS del bloque de 3 botones de gates ▼
# ─────────────────────────────────────────────────────────────────────

sim_frame = make_section(left_panel, "  ▶  Simulación del día", row_idx)
row_idx += 1

make_btn(sim_frame, "▶  Abrir simulación", "GR.TButton", btn_abrir_simulacion_click)
root.mainloop()