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

    # definir el prompt
    prompt = f"""Eres un asistente altamente especializado en el análisis de imágenes de vehículos. Tu tarea es identificar y describir cualquier daño visible en la imagen, basándote en las zonas y tipos de daño predefinidos.

Instrucciones:
1. Analiza la imagen del vehículo proporcionada. La imagen corresponde a la zona **{imagen.tipo.value}**.
2. Detecta todos los desperfectos presentes, pero solo regístralos si estás 100% seguro de que se trata de un daño. En caso de duda, asume que la imagen no presenta daños.
3. Si no se detecta ningún daño (o si no estás 100% seguro de su existencia), responde con la lista vacía (es decir, `"response": []`).
4. Para cada desperfecto identificado con absoluta certeza, devuelve un objeto JSON con la siguiente estructura exacta:

   {{
       "localizacion": "Indica el área específica donde se encuentra el daño.",
       "tipo": "Especifica el tipo de daño identificado.",
       "gravedad": "Indica la gravedad del daño; debe ser 'leve', 'moderado' o 'grave' ('grave' implica alto costo de reparación).",
       "descripcion": "Ofrece una breve descripción (aproximadamente 12 palabras) que detalle la naturaleza, tipo y gravedad del daño."
   }}

5. Devuelve un único JSON con un array bajo la clave `response`, por ejemplo:

   {{
       "response": [
           {{
               "localizacion": "...",
               "tipo": "...",
               "gravedad": "...",
               "descripcion": "..."
           }},
           {{
               "localizacion": "...",
               "tipo": "...",
               "gravedad": "...",
               "descripcion": "..."
           }}
       ]
   }}

6. No incluyas información adicional ni hagas inferencias fuera de las categorías especificadas.
7. Asegúrate de no confundir desperfectos con reflejos.
8. Responde exclusivamente en español.
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
