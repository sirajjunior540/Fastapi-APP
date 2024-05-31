from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from app.crud import get_user_by_email, create_user, get_users, create_user_item, get_items, get_user
from app.database import engine, SessionLocal
from app.models import Base
import os
from app.schemas import UserSchema, UserCreate, ItemSchema, ItemCreate
# Base = declarative_base()
app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

Base.metadata.create_all(bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=UserSchema, status_code=201)
def get_create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='email already registered')
    return create_user(db=db, user=user)


@app.get("/users/", response_model=list[UserSchema], status_code=200)
def get_the_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user = get_users(db, limit=limit, skip=skip)
    return user


@app.get('/users/{user_id}', response_model=UserSchema, status_code=200)
def get_user_details(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail='user not found')
    return db_user


@app.post("/users/{user_id}/items/", response_model=ItemSchema, status_code=201)
def create_item_for_user(user_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    db_item = create_user_item(db, item=item, user_id=user_id)
    return db_item


@app.get('/items/', response_model=list[ItemSchema], status_code=200)
def get_items_list(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    db_items = get_items(db, skip=skip, limit=limit)
    return db_items


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
