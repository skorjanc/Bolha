from fastapi import status, HTTPException, APIRouter
import json

router = APIRouter(prefix="/ads/categories", tags=["categories"])

@router.get("/",)
def get_all_categories():
    with open('app\categories.json') as json_file:
        categories =  json.load(json_file)
    return categories


@router.get("/{subcategory}")
def get_categories_id(subcategory: str):
    
    with open('app\categories.json') as json_file:
        categories =  json.load(json_file)
    
    all_categories = {}
    for category in categories:
        full_category_name = categories[category]
        category_name = full_category_name.split(' > ')[-1]
        if category_name == subcategory:
            all_categories[full_category_name] = category
    
    if len(all_categories) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"category: {subcategory} does not exist")
    
    return all_categories
