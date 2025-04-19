from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import google.generativeai as genai  
from websockets.exceptions import ConnectionClosed

import chromadb
import json
import uvicorn

from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "models/gemini-1.5-flash-latest"  
genai.configure(api_key=GEMINI_API_KEY)

client = chromadb.Client()
collection = client.create_collection("all-my-documents")

collection.add(
    documents=[
        "Bienvenido a Home Burgers, una hamburguesería especializada en ofrecer un menú simple pero de alta calidad. Nos enfocamos en ingredientes frescos y carne cien por ciento de res para brindar una experiencia gourmet en cada bocado. Nuestro local está ubicado en el Centro Comercial Viva Envigado, un lugar de fácil acceso donde puedes disfrutar en familia o pedir a domicilio. El servicio es rápido, amable y centrado en tu comodidad. ¡Estamos listos para tomar tu orden y hacer que disfrutes de una buena hamburguesa sin complicaciones!",

        "En Home Burgers Viva Envigado puedes disfrutar de nuestra clásica Hamburguesa Sencilla Queso, preparada con 115 gramos de carne cien por ciento de res, acompañada de queso fundido, lechuga fresca, tomate y nuestra inconfundible salsa Home. Es una opción perfecta si buscas algo sabroso pero ligero. Esta hamburguesa es una de las favoritas por su equilibrio entre sabor y sencillez. Precio: 19.4. Disponible para consumo en el local o para entrega a domicilio con la misma frescura.",

        "¿Quieres algo más contundente? Prueba nuestra Hamburguesa Doble Queso. Viene con dos carnes de 115g, doble queso, tomate, lechuga y salsa Home. Es perfecta para quienes tienen buen apetito o quieren disfrutar de todo el sabor que Home Burgers puede ofrecer. Precio: 26.4. También puedes pedir la versión con tocineta: Hamburguesa Doble Queso Tocineta por 30.6. Ambos productos están disponibles para pedidos a domicilio desde nuestro punto en Viva Envigado.",

        "Para los amantes del pollo, Home Burgers ofrece dos sánduches únicos. El Sánduche de Pollo está hecho con pechuga marinada en yogurt y especias, apanada y servida con ensalada de repollo. Precio: 20.6. Si prefieres algo más picante, prueba el Sánduche de Pollo Picante, que incluye la misma preparación con el toque especial de salsa picante. Ambos están disponibles para llevar o pedir a domicilio desde Viva Envigado. Una excelente alternativa a la hamburguesa tradicional.",

        "Pensando en quienes prefieren opciones sin carne, tenemos la Hamburguesa Veggie, una hamburguesa vegetariana de portobellos apanados rellenos de queso cheddar y mozzarella, acompañada de lechuga, tomate y nuestra salsa Home. Precio: 22.5. También está la Hamburguesa NotBurger Sencilla, con patty de 100 gramos a base de plantas, con sabor a carne, lechuga y tomate por 23.9, y su versión doble por 37.1. Todos disponibles en Viva Envigado o para delivery rápido en tu zona.",

        "Home Burgers Viva Envigado está diseñado para ser más que un restaurante: es una experiencia. Con ingredientes de alta calidad, procesos artesanales y un menú que cubre gustos clásicos y modernos, estamos listos para atender tus antojos. Hacemos entregas a domicilio desde el centro comercial para que puedas disfrutar desde casa u oficina. Ya sea carne, pollo o vegetariano, tenemos una opción perfecta para ti. ¿Qué se te antoja hoy?",
    ],
    ids=["id1", "id2", "id3", "id4", "id5", "id6"]
)

system_prompt = """
Eres un asistente virtual de Home Burgers, sede Viva Envigado. Estás diseñado para ofrecer una atención al cliente rápida, clara y útil a los visitantes que desean información sobre el menú, los productos, servicios, promociones y proceso de compra en este punto de venta específico. Tu principal objetivo es guiar al cliente durante su experiencia, resolviendo dudas y ayudando a completar el pedido.

Sigue estas instrucciones cuidadosamente para mantener la coherencia y calidad del servicio:

1. Comunicación:
   - Usa un tono amable, profesional y cercano.
   - Mantén respuestas cortas y precisas, de máximo 25 palabras por mensaje.
   - Evita lenguaje técnico o complicado. Sé claro y directo.
   - No uses emojis, jerga o abreviaturas innecesarias.

2. Contenido:
   - Solo menciona productos, servicios o promociones que estén disponibles en el restaurante Home Burgers de Viva Envigado.
   - Si un cliente pregunta por algo que no se ofrece en esta sede, responde cortésmente indicando que no está disponible.
   - No promociones marcas externas, menús de otras sedes, ni servicios de terceros (por ejemplo, domicilios de otras plataformas).
   - Si el cliente desea conocer el menú, preséntalo en secciones organizadas: hamburguesas, acompañamientos, bebidas, combos, opciones vegetarianas, etc.

3. Funcionalidades:
   - Puedes ayudar al cliente a personalizar su pedido: elegir hamburguesa, tipo de pan, ingredientes adicionales o retirados, acompañamientos y bebidas.
   - Si el cliente tiene restricciones alimentarias o alergias, ofrece una guía básica sobre ingredientes, pero nunca hagas afirmaciones médicas o de salud.
   - Si el cliente solicita recomendaciones, pregúntale primero por sus preferencias (carne, pollo, vegetariano, picante, etc.) antes de sugerir algo.
   - Puedes indicar métodos de pago aceptados, tiempos de espera promedio y opciones de consumo en sitio o para llevar.

4. Flujo de conversación:
   - Siempre guía la conversación hacia completar un pedido o brindar la información que el cliente busca.
   - Evita respuestas abiertas o ambiguas que puedan generar confusión.
   - Cuando el cliente esté listo, recopila su pedido paso a paso y confírmalo al final.
   - Si hay promociones activas o combos especiales en Viva Envigado, puedes mencionarlos solo si son solicitados o relevantes para el pedido.

5. Restricciones:
   - No compartas enlaces externos.
   - No des opiniones personales ni hables en primera persona (por ejemplo, “yo creo”, “a mí me gusta”).
   - Nunca uses nombres de empleados ni proporciones información de contacto personal.

Eres un asistente entrenado específicamente para operar dentro del contexto del restaurante Home Burgers ubicado en Viva Envigado. Tu prioridad es garantizar una experiencia simple, rápida y satisfactoria para cada cliente, desde la consulta hasta el cierre del pedido.
"""


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return RedirectResponse("/static/index.html")

@app.websocket("/init")
async def init(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_json()

            await websocket.send_json({"action": "init_system_response"})
            response = await process_messages(data, websocket)
            await websocket.send_json({"action": "finish_system_response"})
    except (WebSocketDisconnect, ConnectionClosed):
        print("Conexión cerrada")

async def process_messages(messages, websocket):
    results = collection.query(
        query_texts=[messages[-1]["content"]], 
        n_results=2
    )

    # Preparamos el contexto para Gemini
    context = system_prompt + str(results["documents"][0])
    user_message = messages[-1]["content"]
    
    # Configuramos el modelo Gemini
    model = genai.GenerativeModel(MODEL_NAME)
    
    # Generamos la respuesta con Gemini
    response = model.generate_content(
        context + "\n\n" + user_message,
        generation_config={
            "temperature": 0.6,
            "top_p": 0.9,
            "max_output_tokens": 100  # Limitamos la longitud de la respuesta
        }
    )
    
    # Enviamos la respuesta al cliente
    await websocket.send_json({
        "action": "append_system_response",
        "content": response.text
    })

    return response.text

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)