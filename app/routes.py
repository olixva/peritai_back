from typing import List
from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.dto.dtos import EvaluationCreateDTO, EvaluationResponseDTO, EvaluacionDTO
from app.services.ai_service import process_images
from app.db import db

router = APIRouter(
    prefix="/evaluations",
    tags=["Evaluations"]
)


@router.post("", summary="Crea una nueva evaluación", response_model=EvaluationResponseDTO)
async def create_evaluation_endpoint(evaluation_data: EvaluationCreateDTO, background_tasks: BackgroundTasks):
    # Extraer los datos del vehículo
    vehicle_data = {
        "matricula": evaluation_data.matricula,
        "marca": evaluation_data.marca,
        "modelo": evaluation_data.modelo,
        "anio": evaluation_data.anio
    }

    # Registrar la evaluación en la base de datos
    evaluation_id = db.create_evaluation(vehicle_data)

    # Agregar tarea en background para procesar las imágenes con la IA
    background_tasks.add_task(process_images, evaluation_data.imagenes, evaluation_id)

    return EvaluationResponseDTO(
        message="Las imágenes se están procesando",
        evaluation_id=evaluation_id,
        status="Procesando imagenes"
    )


@router.get(
    "/{evaluation_id}",
    summary="Obtiene información de una evaluación específica",
    response_model=EvaluacionDTO
)
async def get_evaluation_details(evaluation_id: str):
    evaluation = db.get_evaluation(evaluation_id)
    if evaluation is None:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    return evaluation


@router.get(
    "",
    summary="Obtiene todas las evaluaciones",
    response_model=List[EvaluacionDTO]
)
async def get_all_evaluations():
    lista_evaluaciones = db.get_all_evaluations()

    if not lista_evaluaciones:
        raise HTTPException(status_code=404, detail="No hay evaluaciones registradas")
    return lista_evaluaciones
