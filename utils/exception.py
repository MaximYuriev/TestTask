from fastapi.exceptions import HTTPException

iternal_server_error = HTTPException(status_code=500, detail='Непредвиденная ошибка!')

breed_not_exist = HTTPException(status_code=404, detail='Порода не найдена в базе данных!')

cat_not_found = HTTPException(status_code=404, detail='Котенок не найден!')