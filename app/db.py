# Simulación de "base de datos" en memoria para evaluaciones
evaluations_db = []


def create_evaluation(vehicle_data: dict, images_urls: list, status: str = "In process") -> int:
    evaluation_id = len(evaluations_db) + 1
    evaluations_db.append({
        "id": evaluation_id,
        "vehicle_data": vehicle_data,
        "images_urls": images_urls,
        "status": status
    })
    return evaluation_id


def get_evaluations() -> list:
    return evaluations_db


def get_evaluation(evaluation_id: int):
    for evaluation in evaluations_db:
        if evaluation["id"] == evaluation_id:
            return evaluation
    return None