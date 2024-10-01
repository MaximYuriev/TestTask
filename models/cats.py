from pydantic import BaseModel

class Cat(BaseModel):
    name: str
    age: int
    color: str
    description: str
    fk_breed: int

class NoneCat(Cat):
    name: str|None = None
    age: int|None = None
    color: str|None = None
    description: str|None = None
    fk_breed: int|None = None