from pydantic import BaseModel
from enum import Enum
from typing import List


class TipoImagen(str, Enum):
    frontal = "frontal"
    lateral_izquierdo = "lateral izquierdo"
    lateral_derecho = "lateral derecho"
    parte_trasera = "parte trasera"
    parte_alta = "parte alta"


class ImagenDTO(BaseModel):
    url: str
    tipo: TipoImagen


class EvaluationCreateDTO(BaseModel):
    matricula: str
    marca: str
    modelo: str
    anio: str
    imagenes: List[ImagenDTO]


class EvaluationResponseDTO(BaseModel):
    message: str
    evaluation_id: int
    status: str


class DesperfectoDTO(BaseModel):
    localizacion: str
    tipo: str
    descripcion: str
    gravedad: str


class ResultadoEvaluacionDTO(BaseModel):
    url_image: str
    status: str
    desperfectos: List[DesperfectoDTO]
