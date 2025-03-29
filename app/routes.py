from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.dto.dtos import EvaluationCreateDTO, EvaluationResponseDTO, EvaluacionDTO
from app.services.ai_service import process_images
from app.db.db import create_evaluation, get_evaluation

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
    evaluation_id = create_evaluation(vehicle_data, evaluation_data.imagenes)

    # Agregar tarea en background para procesar las imágenes con la IA
    for image in evaluation_data.imagenes:
        background_tasks.add_task(process_images, image)

    return EvaluationResponseDTO(
        message="Las imágenes se están procesando",
        evaluation_id=evaluation_id,
        status="En proceso"
    )


@router.get(
    "/{evaluation_id}",
    summary="Obtiene información de una evaluación específica",
    response_model=EvaluacionDTO
)
async def get_evaluation_details(evaluation_id: int):
    evaluation = get_evaluation(evaluation_id)
    if evaluation is None:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    return evaluation
