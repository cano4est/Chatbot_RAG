#!/bin/bash

# Script para instalar dependencias del proyecto de chatbot con Gemini
echo "Instalando dependencias del proyecto..."

# Verificar el venv
if [ -z "$VIRTUAL_ENV" ]; then
    echo ""
    echo "ERROR: No estás en un entorno virtual."
    echo "Crea y activa uno primero:"
    echo ""
    echo "python3 -m venv venv"
    echo "source venv/bin/activate"
    echo ""
    echo "Luego vuelve a ejecutar este script."
    exit 1
fi

# Actualizar pip
python3 -m pip install --upgrade pip

# Instalar dependencias principales
python3 -m pip install fastapi uvicorn websockets python-multipart

# Instalar ChromaDB
python3 -m pip install chromadb

# Instalar SDK de Google para Gemini
python3 -m pip install google-generativeai

# Instalar dependencias adicionales
python3 -m pip install python-dotenv

# Verificar instalación
echo ""
echo "Dependencias instaladas:"
python3 -m pip list | grep -E "fastapi|uvicorn|websockets|chromadb|google-generativeai|python-dotenv"

echo ""
echo "¡Instalación completada!"
echo "Puedes iniciar el servidor con: uvicorn main:app --reload"
