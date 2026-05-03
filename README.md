# 📡 Lectura de Canal ThingSpeak  
Aplicación en Python para la consulta y visualización de datos almacenados en un canal IoT de ThingSpeak.

Este módulo forma parte de un proyecto académico orientado a la monitorización de parámetros cognitivos mediante un sistema IoT. La aplicación permite consultar el último registro disponible o los últimos *N* registros del canal, mostrando los datos en una interfaz gráfica desarrollada con Tkinter.

---

## 🚀 Funcionalidades principales

- Lectura del **último registro** del canal ThingSpeak.  
- Lectura de los **últimos N registros** mediante parámetro configurable.  
- Visualización estructurada de los campos `field1` a `field5`.  
- Interfaz gráfica moderna y redimensionable.  
- Scroll integrado para visualizar grandes volúmenes de datos.  
- Versión ejecutable para Windows (`appLecturaCanal.exe`).

---

## 🛠 Tecnologías utilizadas

- **Python 3.x**  
- **Tkinter** (interfaz gráfica)  
- **requests** (comunicación HTTPS con la API REST de ThingSpeak)  
- **PyInstaller** (generación del ejecutable)

---
## 🔧 Configuración del canal ThingSpeak

Antes de ejecutar la aplicación, es necesario configurar los parámetros del canal IoT. 
Estos valores deben corresponder al canal ThingSpeak desde el cual se van a leer los datos.
Por motivos de seguridad, no se incluyen credenciales reales en el repositorio.
Edite el archivo `app.py` y sustituya los valores:
````
CHANNEL_ID = "TU_CHANNEL_ID"
READ_API_KEY = "TU_READ_API_KEY"
````

---
## 🌐 Endpoints utilizados (HTTPS)

### Último registro 
````
https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=1
````

### Últimos N registros  
````
https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results={N}
````
---

## 📦 Instalación y ejecución

### 1. Clonar el repositorio
````
git clone https://github.com/mfernandez345/gestionarCanalLectura
cd gestionarCanalLectura
````
### 2. Instalar dependencias
````
pip install requests
````
### 3. Ejecutar la aplicación
````
python app.py
````
---

## 🖥 Ejecutable para Windows

El repositorio incluye un archivo ejecutable, generado con PyInstaller, en:
````
dist/appLecturaCanal.exe
````
Permite ejecutar la aplicación sin necesidad de instalar Python.

---

## 🧩 Estructura del proyecto
````
gestionarCanalLectura/
│
├── dist/                      # Carpeta con el ejecutable final
│   └── appLecturaCanal.exe    # Ejecutable generado para Windows
│
├── app.py                     # Código principal de la aplicación
├── .gitignore                 # Reglas para ignorar archivos en Git
└── README.md                  # Documentación del proyecto
````
---

## 📄 Licencia

Proyecto académico. Uso educativo.