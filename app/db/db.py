# Simulación de "base de datos" en memoria para evaluaciones
from typing import List

from app.dto.dtos import EvaluacionDTO, DatosVehiculoDTO, ResultadoDesperfectosImagenDTO, ImagenDTO

evaluations_db: List[EvaluacionDTO] = []


def create_evaluation(vehicle_data: dict, status: str = "Procesando imagenes") -> str:
    evaluation_id: str = str(len(evaluations_db) + 1)

    # Añadimos la evaluación a la base de datos
    evaluations_db.append(
        EvaluacionDTO(
            id=evaluation_id,
            status=status,
            datos_vehiculo=DatosVehiculoDTO(**vehicle_data),
            danios_detectados=[]
        )
    )
    return evaluation_id


def update_evaluation_status(evaluation_id: str, status: str):
    for evaluation in evaluations_db:
        if evaluation.id == evaluation_id:
            evaluation.status = status
            break


def add_danio_to_evaluation(evaluation_id: str, result: ResultadoDesperfectosImagenDTO):
    for evaluation in evaluations_db:
        if evaluation.id == evaluation_id:
            evaluation.danios_detectados.append(result)
            break


def get_evaluation(evaluation_id: str) -> EvaluacionDTO | None:
    for evaluation in evaluations_db:
        if evaluation.id == evaluation_id:
            return evaluation
    return None


def get_all_evaluations() -> List[EvaluacionDTO]:
    return evaluations_db
