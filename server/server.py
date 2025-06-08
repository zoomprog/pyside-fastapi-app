from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from datetime import datetime
from typing import List

# Создаем подключение к SQLite базе данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Определение модели данных для таблицы
class Data(Base):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    date = Column(String)
    time = Column(String)
    click_count = Column(Integer)

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Pydantic модель для валидации данных
class DataCreate(BaseModel):
    url: str
    date: str
    time: str
    click_count: int

# Создаем FastAPI приложение
app = FastAPI()

# Dependency для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <html>
        <head><title>Выбор действия</title></head>
        <body>
            <h1>Выберите действие:</h1>
            <ul>
                <li><a href="/submit">/submit - Отправить данные</a></li>
                <li><a href="/retrieve">/retrieve - Получить данные</a></li>
            </ul>
        </body>
    </html>
    """
    return html_content

# POST эндпоинт для добавления данных в базу данных
@app.post("/submit")
async def add_data(data: DataCreate, db: SessionLocal = Depends(get_db)):
    db_data = Data(**data.model_dump())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return {"status": "success", "data": data}

# GET эндпоинт для получения данных с пагинацией
@app.get("/retrieve")
async def get_data(skip: int = 0, limit: int = 10, db: SessionLocal = Depends(get_db)):
    data = db.query(Data).offset(skip).limit(limit).all()
    if not data:
        return {"message": "No data found", "data": []}
    return {"data": data}

# Запуск сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)