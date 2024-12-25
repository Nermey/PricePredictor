from fastapi import APIRouter, Cookie, HTTPException
from database.config import settings
from jose import jwt, JWTError
from datetime import datetime, timezone
from schemas.house import PredictionParams
from catboost import CatBoostRegressor
import pandas as pd

router = APIRouter(prefix="/price", tags=["Price predictor"])
model = CatBoostRegressor()
model.load_model("catboost_model.cbm")


@router.post("/")
def predict_price(users_access_token: str = Cookie(None), params: PredictionParams = None):
    if not users_access_token:
        raise HTTPException(status_code=400, detail="Cookie not found")

    try:
        decode_jwt = jwt.decode(users_access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    exp = decode_jwt.get("exp")

    if datetime.now(timezone.utc) >= datetime.fromtimestamp(exp, tz=timezone.utc):
        raise HTTPException(status_code=401, detail="Token expired")

    if params is None:
        raise HTTPException(status_code=400, detail="Prediction parameters not provided")

    input_data = pd.DataFrame([{
        "level": params.level,
        "levels": params.levels,
        "rooms": params.rooms,
        "area": params.area,
        "kitchen_area": params.kitchen_area,
        "geo_lat": params.geo_lat,
        "geo_lon": params.geo_lon,
        "building_type": params.building_type,
        "object_type": params.object_type,
        "id_region": params.id_region,
        "year": 2024,
        "month": 12,
        "day": 5
    }])

    try:
        predicted_price = model.predict(input_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

    return {"predicted_price": predicted_price[0]}
