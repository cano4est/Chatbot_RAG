# Home Burgers Chatbot

Este es un chatbot interactivo basado en un restaurante de hamburguesas, fue construido con FastAPI, WebSockets y el modelo de IA Gemini de Google, ademas de usar la base de datos vectorizada ChromaDB. El chatbot proporciona información sobre el menú, opciones de comida y servicios disponibles.

![Diagrama de arquitectura del sistema](/home/asus/Documentos/Agent_project/Diagrama de flujo - chatbot.png)

## Requisitos previos

- Python 3.8+
- Cuenta de Google AI Studio con acceso a la API de Gemini

## Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/cano4est/Chatbot_RAG
cd Chatbot_RAG
```

### 2. Crear un entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  
```

### 3. Instalar dependencias

El proyecto incluye un script que instala todas las dependencias necesarias:

```bash
chmod +x install_dependencies.sh  # Dar permisos de ejecución
./install_dependencies.sh
```

El script `install_dependencies.sh` instalará:
- FastAPI y Uvicorn para el servidor web
- WebSockets para comunicación en tiempo real
- ChromaDB para la base de datos vectorial
- Google Generative AI SDK para interactuar con Gemini
- Python-dotenv para manejar variables de entorno

### 4. Configurar la API Key de Gemini

Crea un archivo `.env` en la raíz del proyecto con tu clave API de Gemini:

```
GEMINI_API_KEY=tu_clave_api_aqui
```

También puedes exportar la variable de entorno directamente en tu terminal:

```bash
export GEMINI_API_KEY="tu_clave_api_aqui"
```

Para obtener una clave API de Gemini, regístrate en [Google AI Studio](https://makersuite.google.com/).

## Estructura del proyecto

```
.
├── bot_rag.py           # Archivo principal del servidor
├── install_dependencies.sh  # Script para instalar dependencias
├── static/              # Archivos estáticos para el frontend
│   ├── css/
│   │   └── app.css      # Estilos de la aplicación
│   ├── img/
│   │   └── bg3.jpg      # Imagen de fondo
│   ├── js/
│   │   └── app.js       # Lógica JavaScript del cliente
│   └── index.html       # Página principal HTML
└── .env                 # Archivo de variables de entorno (no incluido en el repo)
```

### Frontend

El frontend incluye:

- Una interfaz simple de chat con un fondo personalizado
- Área de texto para enviar mensajes
- Visualización de mensajes con estilos diferenciados para usuario y sistema
- Indicador de carga durante la generación de respuestas

## Ejecutar la aplicación

Para iniciar el servidor:

```bash
python bot_rag.py
```

La aplicación estará disponible en: http://localhost:8000

## Funcionamiento

1. El chatbot utiliza ChromaDB para almacenar información sobre el menú y servicios de la hamburguesería
2. El sistema emplea un enfoque RAG (Retrieval-Augmented Generation) para buscar información relevante
3. La API de Gemini procesa las consultas y genera respuestas naturales y útiles
4. La comunicación entre cliente y servidor se realiza mediante WebSockets para una experiencia fluida

## Personalización

Puedes modificar la información del menú editando la sección `collection.add()` en el archivo `bot_rag.py`. También puedes ajustar los parámetros de generación como temperatura y longitud máxima de respuesta en la función `process_messages()`.

