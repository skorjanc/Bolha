from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
import json

router = APIRouter(prefix="/ads", tags=["ads"])

@router.get("/", response_model=List[schemas.AdWithPublished])
def get_all_ads(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user), Limit: int = 3, skip: int = 0, Category: Optional[str] = ""):
    #cursor.execute("""SELECT * FROM ads""")
    #ads = cursor.fetchall()
    ads = db.query(models.Ad).filter(models.Ad.user_id == current_user.id).filter(models.Ad.category.startswith(Category)).limit(Limit).offset(skip).all()
    return ads


@router.get("/{id}", response_model=schemas.AdWithPublished)
def get_ad_by_id(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM ads WHERE id = %s""", (str(id)))
    #ad = cursor.fetchone()
    ad = db.query(models.Ad).filter(models.Ad.id == id).first()
    if not ad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ad with id: {id} was not found")
    if ad.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    return ad


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Ad)
def post_ad(ad: schemas.AdCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    with open('app\categories.json') as json_file:
        categories =  json.load(json_file)

    category_exists = False
    for category in categories:
        if ad.category == category:
            category_exists = True
            break

    if category_exists == False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"category: {ad.category} does not exist")
    
    #cursor.execute("""INSERT INTO ads (title, content, price, category) VALUES (%s, %s, %s, %s) RETURNING *""", (ad.title, ad.content, ad.price, ad.category))
    #new_ad = cursor.fetchone()
    #conn.commit()
    new_ad = models.Ad(user_id = current_user.id, **ad.dict())
    db.add(new_ad)
    db.commit()
    db.refresh(new_ad)
    return new_ad


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ad(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM ads WHERE id = %s RETURNING *""", (str(id),))
    #deleted_ad = cursor.fetchone()
    #conn.commit()
    ad_query = db.query(models.Ad).filter(models.Ad.id == id)

    ad = ad_query.first()

    if ad == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ad with id: {id} not found")
    
    if ad.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    ad_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Ad)
def update_ad(new_ad: schemas.AdUpdate, id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    new_ad_dict = new_ad.dict()
    
    if new_ad_dict['title'] == None:
        new_ad_dict.pop('title', None)
    if new_ad_dict['content'] == None:
        new_ad_dict.pop('content', None)
    if new_ad_dict['price'] == None:
        new_ad_dict.pop('price', None)
    if new_ad_dict['phone'] == None:
        new_ad_dict.pop('phone', None)
    
    #cursor.execute("""UPDATE ads SET title=%s, content=%s, price=%s where id=%s RETURNING *""", (new_ad_dict['title'], new_ad_dict['content'], new_ad_dict['price'], id))
    #updated_ad = cursor.fetchone()
    #conn.commit()

    ad_query = db.query(models.Ad).filter(models.Ad.id == id)
    if ad_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ad with id: {id} not found")
    
    if ad_query.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    ad_query.update(new_ad_dict, synchronize_session=False)
    db.commit()
    return ad_query.first()
