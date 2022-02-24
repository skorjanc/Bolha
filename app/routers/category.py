from fastapi import status, HTTPException, APIRouter
import json

router = APIRouter(prefix="/ads/categories", tags=["categories"])

@router.get("/")
def get_all_categories():
    with open('app\categories.json') as json_file:
        categories =  json.load(json_file)
    return categories


@router.get("/{keyword}")
def get_categories_id(keyword: str):
    
    with open('app\categories.json') as json_file:
        categories =  json.load(json_file)
    
    all_categories = {}
    for category in categories:
        full_category_name = categories[category]
        if keyword in full_category_name:
            all_categories[full_category_name] = category
    
    if len(all_categories) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"category: {keyword} does not exist")
    
    return all_categories
