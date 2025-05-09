from models.category_model import Category
from schemas.category_schema import CategoryBase
from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session

category_route_app = APIRouter()

#create
@category_route_app.post("/")
async def create_category(category: CategoryBase, db: Session = Depends(get_db) ):
    try:
        data = Category(**category.dict())
        db.add(data)
        db.commit()
        return { "message": "Success", "data": Category(**category.dict()) }
    except:
        return {"message":"Failed. Category already exists."}

#read
@category_route_app.get("/{id}")
async def get_category_by_id(id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == id).filter(Category.deleted == 0).first()
    if not category == None:
        return {"message": "Success", "data": category}
    else:
        return {"message": "Failed. Category does not exist."} 
    
@category_route_app.get("/")
async def get_category(db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.deleted == 0).all()
    if not category == None:
        return {"message": "Success", "data": category}
    else:
        return {"message": "Failed. Category does not exist."} 
    
#update
@category_route_app.put("/{id}")
async def update_category( category: CategoryBase, id: int, db: Session = Depends(get_db)):
    category_data = db.query(Category).filter(Category.id == id).filter(Category.deleted == 0).first()
    if not category_data == None:
        try:
            category_data = {
                "name": category.name,
            }
            db.query(Category).filter(Category.id == id).filter(Category.deleted == 0).update(category_data)
            db.commit()
            return {"message": "Success", "data": category_data}
        except Exception as e:
            return {"message": "Failed.", "error": e}
    else:
        return {"message": "Failed. Category does not exist."}
    

#delete
@category_route_app.put("/delete/{id}")
async def update_Category( id: int, db: Session = Depends(get_db)):
    category_data = db.query(Category).filter(Category.id == id).first()
    if not category_data == None:
        try:
            category_data = {
                "deleted": 1,
            }
            db.query(Category).filter(Category.id == id).update(category_data)
            db.commit()
            return {"message": "Success", "data": category_data}
        except Exception as e:
            return {"message": "Failed.", "error": e}
    else:
        return {"message": "Failed. Category does not exist."}
