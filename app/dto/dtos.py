from pydantic import BaseModel
from enum import Enum
from typing import List


# Endpoint de /evaluations
class TipoImagen(str, Enum):
    frontal = "frontal"
    lateral_izquierdo = "lateral izquierdo"
    lateral_derecho = "lateral derecho"
    parte_trasera = "parte trasera"


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


# Interaccion con la IA
class DesperfectoDTO(BaseModel):
    localizacion: str
    tipo: str
    descripcion: str
    gravedad: str


class ResultadoDesperfectosImagenDTO(BaseModel):
    url_image: str
    tipo_imagen: str
    desperfectos: List[DesperfectoDTO]


# Endpoint de /evaluations/{evaluation_id}
class DatosVehiculoDTO(BaseModel):
    matricula: str
    marca: str
    modelo: str
    anio: str


class EvaluacionDTO(BaseModel):
    id: str
    status: str
    datos_vehiculo: DatosVehiculoDTO
    danios_detectados: List[ResultadoDesperfectosImagenDTO]
