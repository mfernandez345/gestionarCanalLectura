# **📡 Lectura y Escritura de Canal ThingSpeak**

Aplicación en Python para la **lectura, escritura y visualización** de datos en un canal IoT de ThingSpeak.

Este módulo forma parte de un proyecto académico orientado a la monitorización de parámetros cognitivos mediante un sistema IoT. La aplicación permite **consultar registros**, **enviar nuevos datos al canal** y visualizar la información en una interfaz gráfica desarrollada con Tkinter.

---

## **🚀 Funcionalidades principales**

- **Lectura del último registro** del canal ThingSpeak.  
- **Lectura de los últimos N registros** mediante parámetro configurable.  
- **Visualización con etiquetas reales** de los campos configurados en el canal (field1–field5).  
- **Escritura de nuevos registros** en el canal mediante la API oficial.  
- Validación avanzada de datos antes del envío.  
- Interfaz gráfica moderna, redimensionable y con pestañas (lectura/escritura).  
- Scroll integrado para visualizar grandes volúmenes de datos.  
- Versión ejecutable para Windows (`appEscrituraLecturaCanal.exe`).  

---

## **🛠 Tecnologías utilizadas**

- **Python 3.x**  
- **Tkinter** (interfaz gráfica)  
- **requests** (comunicación HTTPS con la API REST de ThingSpeak)  
- **threading** (envío no bloqueante)  
- **PyInstaller** (generación del ejecutable)  

---

## **🔧 Configuración del canal ThingSpeak**

Antes de ejecutar la aplicación, es necesario configurar los parámetros del canal IoT.  
Por motivos de seguridad, **no se incluyen credenciales reales en el repositorio**.

Edite el archivo `app.py` y sustituya los valores:

```python
CHANNEL_ID = "TU_CHANNEL_ID"
READ_API_KEY = "TU_READ_API_KEY"
WRITE_API_KEY = "TU_WRITE_API_KEY"

```

---
## **🌐 Endpoints utilizados (HTTPS)**

---
### **📥 Lectura de datos**

**Último registro** 
```
https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=1
```

**Últimos N registros**  
```
https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results={N}
```

---

### **📤 Escritura de datos**

La aplicación permite enviar nuevos registros al canal ThingSpeak utilizando la API oficial de escritura.  
Los valores introducidos en el formulario se validan, se envían mediante una petición HTTPS y se registra el resultado en la interfaz.

---

### **🔎 Validación de datos**

Antes de enviar los valores:

- Se comprueba que cada campo contiene un número válido.  
- Se aceptan tanto puntos como comas decimales.  
- Si algún valor no es válido, el envío se cancela y se muestra un aviso.

---

### **🌐 Endpoint de escritura**
```
https://api.thingspeak.com/update?api_key={WRITE_API_KEY}&field1={VAL1}&field2={VAL2}&field3={VAL3}&field4={VAL4}&field5={VAL5}
```

**Donde:**

- `{WRITE_API_KEY}` es la clave de escritura del canal.  
- `{VAL1}` a `{VAL5}` son los valores enviados desde la interfaz.

---

### **📬 Respuesta del servidor**

ThingSpeak devuelve:

- Un **ID numérico** → el registro se ha enviado correctamente.  
- `"0"` → el envío ha fallado.  

La aplicación interpreta esta respuesta y actualiza:

- El **historial de registros enviados**  
- El **contador de envíos**  
- El **log de actividad** con colores (OK, advertencia o error)

---

### **⏱ Límite de 16 segundos**

La versión gratuita de ThingSpeak impone un límite de **1 actualización cada 15 segundos**.  
La aplicación gestiona este límite automáticamente:

- Tras un envío correcto, se inicia una cuenta atrás de **16 segundos**.  
- Durante ese tiempo, el botón de envío permanece deshabilitado.  
- Al finalizar, el sistema vuelve a estar listo para un nuevo registro.

---

### **📋 Historial y log de actividad**

Cada envío correcto se añade a:

- Una tabla con los valores enviados  
- Un log cronológico con mensajes de estado  

Esto permite llevar un seguimiento claro de todos los registros enviados durante la sesión.

---

### **🧪 Campos enviados**

Los cinco campos enviados corresponden a:

- **Carga cognitiva (%)**  
- **Nivel de coherencia (0–100)**  
- **Intensidad emocional (0–100)**  
- **Latencia de inferencia (ms)**  
- **Consumo energético (W)**  

Estos valores se asignan automáticamente a `field1`...`field5` del canal ThingSpeak.

---

## **📦 Instalación y ejecución**

### **1. Clonar el repositorio**
```
git clone https://github.com/mfernandez345/gestionarLecturaEscrituraCanal
cd gestionarLecturaEscrituraCanal
```
### **2. Instalar dependencias**
```
pip install requests
```
### **3. Ejecutar la aplicación**
```
python app.py
```
---

## **🖥 Ejecutable para Windows**

El repositorio incluye un archivo ejecutable, generado con PyInstaller, en:
```
dist/appLecturaEscrituraCanal.exe
```
Permite ejecutar la aplicación sin necesidad de instalar Python.

---

## **🧩 Estructura del proyecto**
```
gestionarLecturaEscrituraCanal/
│
├── dist/                      # Carpeta con el ejecutable final
│   └── appLecturaEscriturCanal.exe    # Ejecutable generado para Windows
│
├── app.py                     # Código principal de la aplicación
├── .gitignore                 # Reglas para ignorar archivos en Git
└── README.md                  # Documentación del proyecto
```
---

## 📄 Licencia

Proyecto académico. Uso educativo.