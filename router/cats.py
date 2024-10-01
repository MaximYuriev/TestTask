from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from db import get_session
from models.cats import Cat as PyCat, NoneCat
from schemas.cats import Breed, Cat
from utils.exception import breed_not_exist, iternal_server_error, cat_not_found

cat_router = APIRouter(prefix='/cat',tags=['Cat'])

async def check_breed_exist(pycat:PyCat|NoneCat,db:Session=Depends(get_session)): #проверка на наличие породы в базе данных
    if pycat.fk_breed is None:
        return pycat
    query = select(Breed).where(Breed.id == pycat.fk_breed)
    breed = await db.scalar(query)
    if breed is None:
        raise breed_not_exist
    return pycat

async def get_cat_by_id(cat_id:int,db:Session=Depends(get_session)):
    query = select(Cat).where(Cat.id == cat_id)
    cat = await db.scalar(query)
    if cat is None:
        raise cat_not_found
    return cat


@cat_router.post('/add')
async def add_new_cat(pycat:PyCat=Depends(check_breed_exist),db:Session=Depends(get_session)): #добавление нового котенка
    new_cat = Cat(
        name=pycat.name,
        age=pycat.age,
        color=pycat.color,
        description=pycat.description,
        fk_breed=pycat.fk_breed
    )

    try:
        db.add(new_cat)
        await db.commit()
    except SQLAlchemyError:
        await db.rollback()
        raise iternal_server_error

    return {"detail":"Котенок добавлен!","data":None}

@cat_router.get('/all')
async def get_all_cats(db:Session=Depends(get_session), breed_id:int=None): #получение списка всех котят и получение котят определенной породы
    if breed_id is None:
        query = select(Cat)
    else:
        breed = await db.scalar(select(Breed).where(Breed.id == breed_id))
        if breed is None:
            raise breed_not_exist
        query = select(Cat).where(Cat.fk_breed == breed_id)
    result = await db.execute(query)
    cats = result.scalars().all()
    return {"detail": "Список всех Котят", "data": cats}


@cat_router.get('/{cat_id}')
async def get_cat(cat:Annotated[Cat,Depends(get_cat_by_id)]): #получение информации о котенке по id
    return {"detail":"Информация о котенке", "data":cat}


@cat_router.delete('/{cat_id}')
async def delete_cat(cat:Annotated[Cat,Depends(get_cat_by_id)], db:Session=Depends(get_session)): #удаление котенка из базы данных
    try:
        await db.delete(cat)
        await db.commit()
    except SQLAlchemyError:
        await db.rollback()
        raise iternal_server_error
    return {"detail":"Котенок удален!", "data":None}


@cat_router.put('/{cat_id}')
async def edit_cat(cat:Annotated[Cat,Depends(get_cat_by_id)], pycat:NoneCat=Depends(check_breed_exist),
                   db:Session=Depends(get_session)): #Изменение информации о котенке(частичное и полное)

    update_data = pycat.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(cat, key, value)

    try:
        await db.commit()
    except SQLAlchemyError:
        await db.rollback()
        raise iternal_server_error
    return {"detail":"Информация о котенке изменена", "data":None}

