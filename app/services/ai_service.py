from app.dto.dtos import ImagenDTO, ResultadoDesperfectosImagenDTO, DesperfectoDTO, TipoImagen
from app.db import db

import requests
import base64
import json
from ollama import Client


def process_images(images: list[ImagenDTO], evaluation_id: str):
    desperfecto: bool = False
    for image in images:
        result = process_image(image)

        if result.desperfectos:
            # Si se detectaron desperfectos, actualizamos la evaluación
            desperfecto = True
            db.add_danio_to_evaluation(evaluation_id, result)

    if desperfecto:
        db.update_evaluation_status(evaluation_id, "Desperfectos detectados")
    else:
        db.update_evaluation_status(evaluation_id, "Sin desperfectos")


def process_image(imagen: ImagenDTO) -> ResultadoDesperfectosImagenDTO:
    # Conectarse al servidor Ollama
    client = Client(
        host="https://ollama.nest0r.dev",
        headers={"Authorization": "Basic bmVzdG9yOm5lc3RvcjEy"}
    )

    # descargar imagen y pasar a bytes
    image_bytes = requests.get(imagen.url).content
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # Cargar localizaciones
    diccionario = {
        "frontal": [
            "parabrisas", "luna delantera", "matrícula delantera",
            "faro derecho", "faro izquierdo", "guardabarros derecho", "guardabarros izquierdo",
            "parachoques delantero", "capó"
        ],
        "parte trasera": [
            "luna trasera", "matrícula trasera", "maletero",
            "faro trasero derecho", "faro trasero izquierdo",
            "parachoques trasero"
        ],
        "lateral izquierdo": [
            "puerta delantera izquierda", "puerta trasera izquierda",
            "retrovisor izquierdo", "guardabarros trasero izquierdo", "guardabarros delantero izquierdo",
            "ventana delantera izquierda", "ventana trasera izquierda"
        ],
        "lateral derecho": [
            "puerta delantera derecha", "puerta trasera derecha",
            "retrovisor derecho", "guardabarros trasero derecho", "guardabarros delantero derecho",
            "ventana delantera derecha", "ventana trasera derecha"
        ]
    }
    localizaciones = diccionario[imagen.tipo.value]

    # Cargar tipos de daño
    tipos_de_dano = ["abolladura", "rayón", "rotura", "desprendimiento de pintura", "fisura", "desgaste", "oxido"]

    # definir el prompt
    prompt = f"""
        Eres un asistente útil que analiza imágenes de vehículos e identifica daños basándose en zonas y tipos de daño predefinidos.
        Analiza el vehículo en la imagen proporcionada teniendo en cuenta que estás viendo la zona {imagen.tipo.value} de un vehículo.
        Devuelve una lista de JSONs con la siguiente estructura:
        {{
        response:
        [{{
            "localizacion": "Debes indicar dónde está el desperfecto. Las únicas posibles opciones son: {localizaciones}.",
            "tipo": "Debes indicar de qué tipo es el desperfecto. La únicas posibles opciones son: {tipos_de_dano}.",
            "gravedad": "Debes indicar la gravedad del desperfecto: sólo puede ser leve o grave. Grave indica caro de reparar.",
            "descripcion": "Explicación de aproximadamente 12 palabras detallando la naturaleza, el tipo y la gravedad del desperfecto.",
        }}
        {{
        otro desperfecto...,
        }}
        ]
        }}
        El tamaño de esta lista variará dependiendo del número de desperfectos detectados.
        No incluyas información adicional ni hagas inferencias fuera de las categorías especificadas.
        Responde exclusivamente en español.
        Asegúrate de que no confundes desperfectos con reflejos.
    """

    # llamar al modelo
    response = client.generate(
        model="gemma3:12b",
        format="json",
        prompt=prompt,
        images=[image_base64]
    )

    response = json.loads(response['response'])
    # Convertir cada diccionario en una instancia de DesperfectoDTO
    desperfectos = []
    for item in response['response']:
        print(item)
        desperfectos.append(DesperfectoDTO(**item))

    # Crear una instancia de ResultadoDesperfectosImagenDTO
    return ResultadoDesperfectosImagenDTO(
        url_image=imagen.url,
        tipo_imagen=imagen.tipo.value,
        desperfectos=desperfectos
    )
