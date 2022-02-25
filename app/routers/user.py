from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from ..encryption import encrypt

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    encrypted_password = encrypt(user.bolha_password)
    user.bolha_password = encrypted_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    return user


@router.get("/", response_model=List[schemas.UserOut])
def get_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.put("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Ad)
def post_ad(user: schemas.UserUpdatePassword, db: Session = Depends(get_db)):
    pass
    user_dict = user.dict()
    user_dict['password'] = user_dict["new_password"]
    new_ad = models.Ad(**user.dict())
    db.add(new_ad)
    db.commit()
    db.refresh(new_ad)
    return new_ad