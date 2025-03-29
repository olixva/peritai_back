from app.dto.dtos import ImagenDTO, ResultadoDesperfectosImagenDTO, DesperfectoDTO, TipoImagen


def process_images(image_data: ImagenDTO) -> ResultadoDesperfectosImagenDTO:
    return ResultadoDesperfectosImagenDTO(
        url_image=image_data.url,
        tipo_imagen=TipoImagen.frontal,
        desperfectos=[
            DesperfectoDTO(
                localizacion="Faro derecho",
                tipo="Rayón",
                descripcion="Rayón en la parte del faro derecho",
                gravedad="Leve"
            ),
            DesperfectoDTO(
                localizacion="Capo",
                tipo="Abolladura",
                descripcion="Abolladura en la parte frontal del capo",
                gravedad="Grave"
            ),
        ]
    )
