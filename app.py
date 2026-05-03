import tkinter as tk
from tkinter import messagebox
import requests

# ------------------------------------
# CONFIGURACIÓN DEL CANAL THINGSPEAK
# ------------------------------------
try:
    from config_local import CHANNEL_ID, READ_API_KEY
except ImportError:
    CHANNEL_ID = "TU_CHANNEL_ID"
    READ_API_KEY = "TU_READ_API_KEY"



# ------------------------------------
# LECTURA DEL ÚLTIMO REGISTRO
# ------------------------------------
def consultar_ultimo():
    url = (
        f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json"
        f"?api_key={READ_API_KEY}&results=1"
    )

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            mostrar_un_registro(data)
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

    text_resultado.config(state="normal")
    text_resultado.delete("1.0", tk.END)

    text_resultado.insert(tk.END, "=== ÚLTIMO REGISTRO ===\n\n")
    text_resultado.insert(tk.END, f"Fecha: {registro.get('created_at', 'N/A')}\n")
    text_resultado.insert(tk.END, f"Entry ID: {registro.get('entry_id', 'N/A')}\n\n")

    for i in range(1, 9):
        valor = registro.get(f"field{i}")
        if valor is not None:
            text_resultado.insert(tk.END, f"Field{i}: {valor}\n")

    text_resultado.config(state="disabled")


# ------------------------------------
# LECTURA DE LOS ÚLTIMOS N REGISTROS
# ------------------------------------
def consultar_n_registros():
    n = entry_n.get().strip()

    if not n.isdigit():
        messagebox.showwarning("Valor inválido", "Introduce un número entero para N.")
        return

    url = (
        f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json"
        f"?api_key={READ_API_KEY}&results={n}"
    )

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            mostrar_varios_registros(data)
        else:
            messagebox.showerror("Error", f"Error al consultar el canal: {response.status_code}")

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a ThingSpeak.\n{e}")


def mostrar_varios_registros(data):
    feeds = data.get("feeds", [])

    if not feeds:
        messagebox.showwarning("Sin datos", "El canal no tiene registros todavía.")
        return

    text_resultado.config(state="normal")
    text_resultado.delete("1.0", tk.END)

    text_resultado.insert(tk.END, f"=== ÚLTIMOS {len(feeds)} REGISTROS ===\n\n")

    for idx, registro in enumerate(feeds, start=1):
        text_resultado.insert(tk.END, f"--- Registro {idx} ---\n")
        text_resultado.insert(tk.END, f"Fecha: {registro.get('created_at', 'N/A')}\n")
        text_resultado.insert(tk.END, f"Entry ID: {registro.get('entry_id', 'N/A')}\n")

        for i in range(1, 9):
            valor = registro.get(f"field{i}")
            if valor is not None:
                text_resultado.insert(tk.END, f"Field{i}: {valor}\n")

        text_resultado.insert(tk.END, "\n")

    text_resultado.config(state="disabled")


# ------------------------------------
# INTERFAZ GRÁFICA
# ------------------------------------
# ------------------------------------
# INTERFAZ GRÁFICA MEJORADA
# ------------------------------------
root = tk.Tk()
root.title("Lectura de Canal ThingSpeak")
root.geometry("700x600")
root.resizable(True, True)

# Paleta de colores suaves
COLOR_FONDO = "#f5f7fa"
COLOR_PANEL = "#ffffff"
COLOR_BOTON = "#d9e6f2"
COLOR_BOTON_HOVER = "#c7d9eb"
COLOR_TEXTO = "#2c3e50"

root.configure(bg=COLOR_FONDO)

# ---- FUNCIÓN PARA EFECTO HOVER EN BOTONES ----
def on_enter(e):
    e.widget["background"] = COLOR_BOTON_HOVER

def on_leave(e):
    e.widget["background"] = COLOR_BOTON

# ---- CONTENEDOR PRINCIPAL ----
main_frame = tk.Frame(root, bg=COLOR_FONDO, padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

# ---- TÍTULO ----
label_titulo = tk.Label(
    main_frame,
    text="📡 Lectura de datos desde ThingSpeak",
    font=("Arial", 18, "bold"),
    bg=COLOR_FONDO,
    fg=COLOR_TEXTO
)
label_titulo.pack(pady=(0, 20))

# ---- BOTÓN ÚLTIMO REGISTRO ----
btn_ultimo = tk.Button(
    main_frame,
    text="📄 Leer último registro",
    font=("Arial", 13),
    bg=COLOR_BOTON,
    fg=COLOR_TEXTO,
    relief="raised",
    width=25,
    command=consultar_ultimo
)
btn_ultimo.pack(pady=10)
btn_ultimo.bind("<Enter>", on_enter)
btn_ultimo.bind("<Leave>", on_leave)

# ---- SECCIÓN N REGISTROS ----
frame_n = tk.Frame(main_frame, bg=COLOR_FONDO)
frame_n.pack(pady=10)

label_n = tk.Label(frame_n, text="📚 Leer últimos N registros:", font=("Arial", 13), bg=COLOR_FONDO, fg=COLOR_TEXTO)
label_n.pack(side="left", padx=5)

entry_n = tk.Entry(frame_n, font=("Arial", 13), width=8)
entry_n.pack(side="left", padx=5)

btn_n = tk.Button(
    frame_n,
    text="🔍 Consultar",
    font=("Arial", 13),
    bg=COLOR_BOTON,
    fg=COLOR_TEXTO,
    relief="raised",
    command=consultar_n_registros
)
btn_n.pack(side="left", padx=5)
btn_n.bind("<Enter>", on_enter)
btn_n.bind("<Leave>", on_leave)

# ---- ÁREA DE RESULTADOS CON SCROLL ----
frame_texto = tk.Frame(main_frame, bg=COLOR_PANEL)
frame_texto.pack(fill="both", expand=True, pady=15)

scrollbar = tk.Scrollbar(frame_texto)
scrollbar.pack(side="right", fill="y")

text_resultado = tk.Text(
    frame_texto,
    font=("Arial", 12),
    wrap="word",
    yscrollcommand=scrollbar.set,
    bg="#ffffff",
    fg="#2c3e50",
    relief="flat"
)
text_resultado.pack(fill="both", expand=True)

scrollbar.config(command=text_resultado.yview)

root.mainloop()