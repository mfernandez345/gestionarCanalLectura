import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading
import time

# =============================================================
# CONFIGURACIÓN DEL CANAL THINGSPEAK
# =============================================================
try:
    from config_local import CHANNEL_ID, READ_API_KEY, WRITE_API_KEY
except ImportError:
    CHANNEL_ID = "TU_CHANNEL_ID"
    READ_API_KEY = "TU_READ_API_KEY"
    WRITE_API_KEY = "TU_WRITE_API_KEY"

# =============================================================
# PALETA DE COLORES
# =============================================================
COLOR_FONDO        = "#f5f7fa"
COLOR_PANEL        = "#ffffff"
COLOR_BOTON        = "#d9e6f2"
COLOR_BOTON_HOVER  = "#c7d9eb"
COLOR_BOTON_OK     = "#d4edda"
COLOR_BOTON_OK_H   = "#c3e6cb"
COLOR_TEXTO        = "#2c3e50"
COLOR_ERROR        = "#e74c3c"
COLOR_OK           = "#27ae60"
COLOR_WARN         = "#f39c12"

# =============================================================
# UTILIDADES
# =============================================================

def validar_numero(valor, nombre_campo):
    """Valida números, acepta coma decimal y evita vacíos."""
    valor = valor.replace(",", ".").strip()
    if valor == "":
        messagebox.showwarning("Valor vacío", f"El campo '{nombre_campo}' no puede estar vacío.")
        return None
    try:
        return float(valor)
    except ValueError:
        messagebox.showwarning("Valor inválido", f"El campo '{nombre_campo}' debe ser un número válido.")
        return None


def obtener_etiquetas(data):
    """Obtiene etiquetas reales de ThingSpeak o usa fallback."""
    channel = data.get("channel", {})
    return {f"field{i}": channel.get(f"field{i}", f"Field{i}") for i in range(1, 9)}


def mostrar_registro(registro, etiquetas, destino):
    """Imprime un registro en el widget destino."""
    destino.insert(tk.END, f"Fecha: {registro.get('created_at', 'N/A')}\n")
    destino.insert(tk.END, f"Entry ID: {registro.get('entry_id', 'N/A')}\n")

    for i in range(1, 9):
        campo = f"field{i}"
        valor = registro.get(campo)
        if valor is not None:
            destino.insert(tk.END, f"{etiquetas[campo]}: {valor}\n")


# =============================================================
# LECTURA DE DATOS
# =============================================================

def consultar_ultimo():
    url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=1"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            mostrar_un_registro(response.json())
        else:
            messagebox.showerror("Error", f"Error al consultar el canal: {response.status_code}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a ThingSpeak.\n{e}")


def mostrar_un_registro(data):
    feeds = data.get("feeds", [])
    if not feeds:
        messagebox.showwarning("Sin datos", "El canal no tiene registros todavía.")
        return

    registro = feeds[0]
    etiquetas = obtener_etiquetas(data)

    text_resultado.config(state="normal")
    text_resultado.delete("1.0", tk.END)

    text_resultado.insert(tk.END, "=== ÚLTIMO REGISTRO ===\n\n")
    mostrar_registro(registro, etiquetas, text_resultado)

    text_resultado.config(state="disabled")


def consultar_n_registros():
    n = entry_n.get().strip()
    if not n.isdigit():
        messagebox.showwarning("Valor inválido", "Introduce un número entero para N.")
        return

    url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results={n}"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            mostrar_varios_registros(response.json())
        else:
            messagebox.showerror("Error", f"Error al consultar el canal: {response.status_code}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a ThingSpeak.\n{e}")


def mostrar_varios_registros(data):
    feeds = data.get("feeds", [])
    if not feeds:
        messagebox.showwarning("Sin datos", "El canal no tiene registros todavía.")
        return

    etiquetas = obtener_etiquetas(data)

    text_resultado.config(state="normal")
    text_resultado.delete("1.0", tk.END)

    text_resultado.insert(tk.END, f"=== ÚLTIMOS {len(feeds)} REGISTROS ===\n\n")

    for idx, registro in enumerate(feeds, start=1):
        text_resultado.insert(tk.END, f"--- Registro {idx} ---\n")
        mostrar_registro(registro, etiquetas, text_resultado)
        text_resultado.insert(tk.END, "\n")

    text_resultado.config(state="disabled")


# =============================================================
# ESCRITURA DE DATOS
# =============================================================

contador_registros = 0

def enviar_registro_escritura():
    global contador_registros

    valores = {
        "Carga cognitiva": entry_f1.get().strip(),
        "Nivel de coherencia": entry_f2.get().strip(),
        "Intensidad emocional": entry_f3.get().strip(),
        "Latencia de inferencia": entry_f4.get().strip(),
        "Consumo energético": entry_f5.get().strip()
    }

    nums = {}
    for nombre, valor in valores.items():
        resultado = validar_numero(valor, nombre)
        if resultado is None:
            return
        nums[nombre] = resultado

    btn_enviar_escritura.config(state="disabled", text="Enviando…")

    threading.Thread(target=_enviar_en_hilo, args=(list(nums.values()),), daemon=True).start()


def _enviar_en_hilo(valores):
    global contador_registros

    params = {
        "api_key": WRITE_API_KEY,
        "field1": valores[0],
        "field2": valores[1],
        "field3": valores[2],
        "field4": valores[3],
        "field5": valores[4],
    }

    try:
        respuesta = requests.get("https://api.thingspeak.com/update", params=params, timeout=10)
        texto = respuesta.text.strip()

        if respuesta.status_code == 200 and texto != "0":
            contador_registros += 1
            root.after(0, lambda: _envio_exitoso(texto, valores))
        else:
            root.after(0, lambda: _envio_error(f"ThingSpeak devolvió: {texto}"))

    except requests.exceptions.RequestException as e:
        root.after(0, lambda: _envio_error(str(e)))


def _envio_exitoso(entry_id, valores):
    anadir_log_escritura(f"[OK] Registro {contador_registros} enviado correctamente (ID: {entry_id})", COLOR_OK)
    label_contador.config(text=f"Registros enviados: {contador_registros}")

    historial_tree.insert("", "end", values=(contador_registros, *valores))

    limpiar_formulario()

    continuar = messagebox.askyesno("Registro enviado", f"Registro {contador_registros} enviado.\n¿Deseas introducir otro?")
    if continuar:
        anadir_log_escritura("[ESPERA] Esperando 16 segundos (límite ThingSpeak)...", COLOR_WARN)
        btn_enviar_escritura.config(state="disabled", text="Esperando…")
        threading.Thread(target=_esperar_y_habilitar, daemon=True).start()
    else:
        btn_enviar_escritura.config(state="normal", text="Enviar registro")


def _esperar_y_habilitar():
    for s in range(16, 0, -1):
        root.after(0, lambda s=s: btn_enviar_escritura.config(text=f"Esperando {s}s…"))
        time.sleep(1)
    root.after(0, lambda: btn_enviar_escritura.config(state="normal", text="Enviar registro"))
    anadir_log_escritura("[OK] Listo para el siguiente registro.", COLOR_OK)


def _envio_error(mensaje):
    anadir_log_escritura(f"[ERROR] Error al enviar: {mensaje}", COLOR_ERROR)
    btn_enviar_escritura.config(state="normal", text="Enviar registro")
    messagebox.showerror("Error de envío", f"No se pudo enviar el registro.\n{mensaje}")


def limpiar_formulario():
    for entry in [entry_f1, entry_f2, entry_f3, entry_f4, entry_f5]:
        entry.delete(0, tk.END)


def anadir_log_escritura(mensaje, color=COLOR_TEXTO):
    hora = time.strftime("%H:%M:%S")
    text_log_escritura.config(state="normal")
    text_log_escritura.insert(tk.END, f"[{hora}] {mensaje}\n")
    text_log_escritura.tag_add(f"color_{color}", "end-2l", "end-1l")
    text_log_escritura.tag_config(f"color_{color}", foreground=color)
    text_log_escritura.see(tk.END)
    text_log_escritura.config(state="disabled")


# =============================================================
# INTERFAZ GRÁFICA
# =============================================================

root = tk.Tk()
root.title("NeuroBotics - Monitor de Estabilidad Cognitiva")
root.geometry("750x650")
root.configure(bg=COLOR_FONDO)

def on_enter(e): e.widget["background"] = COLOR_BOTON_HOVER
def on_leave(e): e.widget["background"] = COLOR_BOTON
def on_enter_ok(e): e.widget["background"] = COLOR_BOTON_OK_H
def on_leave_ok(e): e.widget["background"] = COLOR_BOTON_OK

label_titulo = tk.Label(root, text="NeuroBotics - Monitor de Estabilidad Cognitiva",
                        font=("Arial", 16, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO)
label_titulo.pack(pady=(15, 5))

label_subtitulo = tk.Label(root, text="Gestión de datos IoT mediante ThingSpeak",
                           font=("Arial", 11), bg=COLOR_FONDO, fg="#7f8c8d")
label_subtitulo.pack(pady=(0, 10))

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=15, pady=5)

style = ttk.Style()
style.configure("TNotebook.Tab", font=("Arial", 12), padding=[10, 5])

# =============================================================
# PESTAÑA 1: ESCRITURA
# =============================================================

tab_escritura = tk.Frame(notebook, bg=COLOR_FONDO)
notebook.add(tab_escritura, text="Escritura de datos")

frame_escritura = tk.Frame(tab_escritura, bg=COLOR_FONDO, padx=20, pady=15)
frame_escritura.pack(fill="both", expand=True)

label_form = tk.Label(frame_escritura, text="Introduce los valores del registro:",
                      font=("Arial", 13, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO)
label_form.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")

campos = [
    ("Carga cognitiva (%):", "entry_f1"),
    ("Nivel de coherencia (0-100):", "entry_f2"),
    ("Intensidad emocional (0-100):", "entry_f3"),
    ("Latencia de inferencia (ms):", "entry_f4"),
    ("Consumo energético (W):", "entry_f5")
]

entries = []
for i, (nombre, _) in enumerate(campos):
    lbl = tk.Label(frame_escritura, text=nombre, font=("Arial", 12),
                   bg=COLOR_FONDO, fg=COLOR_TEXTO)
    lbl.grid(row=i+1, column=0, sticky="w", pady=4)
    ent = tk.Entry(frame_escritura, font=("Arial", 12), width=15)
    ent.grid(row=i+1, column=1, sticky="w", padx=10, pady=4)
    entries.append(ent)

entry_f1, entry_f2, entry_f3, entry_f4, entry_f5 = entries

frame_botones_escritura = tk.Frame(frame_escritura, bg=COLOR_FONDO)
frame_botones_escritura.grid(row=7, column=0, columnspan=2, pady=15, sticky="w")

btn_enviar_escritura = tk.Button(frame_botones_escritura, text="Enviar registro",
                                 font=("Arial", 12), bg=COLOR_BOTON_OK, fg=COLOR_TEXTO,
                                 relief="raised", width=18, command=enviar_registro_escritura)
btn_enviar_escritura.pack(side="left", padx=(0, 10))
btn_enviar_escritura.bind("<Enter>", on_enter_ok)
btn_enviar_escritura.bind("<Leave>", on_leave_ok)

btn_limpiar = tk.Button(frame_botones_escritura, text="Limpiar campos",
                        font=("Arial", 12), bg=COLOR_BOTON, fg=COLOR_TEXTO,
                        relief="raised", width=15, command=limpiar_formulario)
btn_limpiar.pack(side="left")
btn_limpiar.bind("<Enter>", on_enter)
btn_limpiar.bind("<Leave>", on_leave)

label_contador = tk.Label(frame_escritura, text="Registros enviados: 0",
                          font=("Arial", 11, "italic"), bg=COLOR_FONDO, fg="#7f8c8d")
label_contador.grid(row=8, column=0, columnspan=2, sticky="w")

label_historial = tk.Label(frame_escritura, text="Historial de registros enviados:",
                           font=("Arial", 12, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO)
label_historial.grid(row=9, column=0, columnspan=2, sticky="w", pady=(15, 5))

columnas_hist = ("#", "Carga cog.", "Coherencia", "Int. emoc.", "Latencia", "Consumo")
historial_tree = ttk.Treeview(frame_escritura, columns=columnas_hist,
                              show="headings", height=4)
for col in columnas_hist:
    historial_tree.heading(col, text=col)
    historial_tree.column(col, width=100, anchor="center")
historial_tree.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(0, 10))

label_log = tk.Label(frame_escritura, text="Registro de actividad:",
                     font=("Arial", 12, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO)
label_log.grid(row=11, column=0, columnspan=2, sticky="w", pady=(5, 3))

text_log_escritura = tk.Text(frame_escritura, font=("Arial", 10), height=5,
                             bg=COLOR_PANEL, fg=COLOR_TEXTO, relief="flat", state="disabled")
text_log_escritura.grid(row=12, column=0, columnspan=2, sticky="ew")

anadir_log_escritura("Sistema listo. Introduce los datos y pulsa 'Enviar registro'.")

# =============================================================
# PESTAÑA 2: LECTURA
# =============================================================

tab_lectura = tk.Frame(notebook, bg=COLOR_FONDO)
notebook.add(tab_lectura, text="Lectura de datos")

frame_lectura = tk.Frame(tab_lectura, bg=COLOR_FONDO, padx=20, pady=20)
frame_lectura.pack(fill="both", expand=True)

btn_ultimo = tk.Button(frame_lectura, text="Leer último registro",
                       font=("Arial", 13), bg=COLOR_BOTON, fg=COLOR_TEXTO,
                       relief="raised", width=25, command=consultar_ultimo)
btn_ultimo.pack(pady=10)
btn_ultimo.bind("<Enter>", on_enter)
btn_ultimo.bind("<Leave>", on_leave)

frame_n = tk.Frame(frame_lectura, bg=COLOR_FONDO)
frame_n.pack(pady=10)

label_n = tk.Label(frame_n, text="Leer últimos N registros:",
                   font=("Arial", 13), bg=COLOR_FONDO, fg=COLOR_TEXTO)
label_n.pack(side="left", padx=5)

entry_n = tk.Entry(frame_n, font=("Arial", 13), width=8)
entry_n.pack(side="left", padx=5)

btn_n = tk.Button(frame_n, text="Consultar", font=("Arial", 13),
                  bg=COLOR_BOTON, fg=COLOR_TEXTO, relief="raised",
                  command=consultar_n_registros)
btn_n.pack(side="left", padx=5)
btn_n.bind("<Enter>", on_enter)
btn_n.bind("<Leave>", on_leave)

frame_texto = tk.Frame(frame_lectura, bg=COLOR_PANEL)
frame_texto.pack(fill="both", expand=True, pady=15)

scrollbar = tk.Scrollbar(frame_texto)
scrollbar.pack(side="right", fill="y")

text_resultado = tk.Text(frame_texto, font=("Arial", 12), wrap="word",
                         yscrollcommand=scrollbar.set, bg=COLOR_PANEL,
                         fg=COLOR_TEXTO, relief="flat")
text_resultado.pack(fill="both", expand=True)

scrollbar.config(command=text_resultado.yview)

# =============================================================
# ARRANQUE
# =============================================================

root.mainloop()
