# Simulación de "base de datos" en memoria para evaluaciones
from typing import List

from app.dto.dtos import EvaluacionDTO, DatosVehiculoDTO, ResultadoDesperfectosImagenDTO

evaluations_db: List[EvaluacionDTO] = []


def create_evaluation(vehicle_data: dict, images_urls: list, status: str = "In process") -> int:
    evaluation_id: int = len(evaluations_db) + 1

    """
    Creamos una lista de objetos ResultadoDesperfectosImagenDTO con los datos de las 
    imágenes que luego se añadirán los desperfectos detectados en cada imagen.
    """
    danios_detectados = [
        ResultadoDesperfectosImagenDTO
        (
            url_image=image.url,
            tipo_imagen=image.tipo_imagen,
            desperfectos=[]
        )
        for image in images_urls
    ]

    # Añadimos la evaluación a la base de datos
    evaluations_db.append(
        EvaluacionDTO(
            id=evaluation_id,
            status=status,
            datos_vehiculo=DatosVehiculoDTO(**vehicle_data),
            danios_detectados=danios_detectados
        )
    )
    return evaluation_id


def get_evaluation(evaluation_id: int) -> EvaluacionDTO | None:
    for evaluation in evaluations_db:
        if evaluation.id == evaluation_id:
            return evaluation
    return None
