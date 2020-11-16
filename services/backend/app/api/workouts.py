from fastapi import APIRouter, HTTPException
from app.api import crud

from app.schemas import WorkoutSchema, WorkoutPayloadSchema
from typing import List

router = APIRouter()


@router.post("/", response_model=WorkoutSchema, status_code=201)
async def create_workout(payload: WorkoutPayloadSchema) -> WorkoutSchema:
    workout = await crud.post_workout(payload)
    return workout
