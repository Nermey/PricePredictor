from pydantic import BaseModel


class PredictionParams(BaseModel):
    level: float
    levels: float
    rooms: float
    area: float
    kitchen_area: float
    geo_lat: float
    geo_lon: float
    building_type: int
    object_type: int
    id_region: int
