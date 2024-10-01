from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from db import get_session
from models.breed import Breed as PyBreed
from schemas.cats import Breed
from utils.exception import iternal_server_error

breed_router = APIRouter(prefix='/breed', tags=["Breed"])

@breed_router.post("/add")
async def add_new_breed(add_breed:PyBreed,db:Session=Depends(get_session)): #Добавляет новую породу в базу данных
    breed_is_not_unique = HTTPException(
        status_code=400,
        detail="Эта порода уже добавлена в базу данных!"
    )

    query = select(Breed).where(Breed.breed_name == add_breed.breed_name)
    breed = await db.scalar(query)
    if breed is not None:
        raise breed_is_not_unique

    breed = Breed(breed_name=add_breed.breed_name)
    try:
        db.add(breed)
        await db.commit()
    except SQLAlchemyError:
        await db.rollback()
        raise iternal_server_error

    return {"detail":"Порода успешно добавлена","data":None}

@breed_router.get("/all")
async def get_all_breeds(db:Session=Depends(get_session)): #Выводит все породы
    result = await db.execute(select(Breed))
    breed = result.scalars().all()
    return {"detail":"Список всех пород","data":breed}
