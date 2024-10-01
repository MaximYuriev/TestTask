from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()

intpk = Annotated[int, mapped_column(primary_key=True)]

class Breed(Base): #Порода
    __tablename__ = 'breed'
    id: Mapped[intpk]
    breed_name: Mapped[str] = mapped_column(unique=True) #Название породы

class Cat(Base):
    __tablename__ = 'cat'
    id: Mapped[intpk]
    name: Mapped[str] #Кличка котенка
    age: Mapped[int] #Возраст котенка
    color: Mapped[str] #Цвет котенка
    description: Mapped[str] #Описание котенка
    fk_breed: Mapped[int] = mapped_column(ForeignKey(Breed.id, ondelete="CASCADE")) #Внешний ключ на таблицу Breed