from models.user_model import User
from schemas.user_schema import UserBase
from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session

user_route_app = APIRouter()

#create
@user_route_app.post("/")
async def create_user(user: UserBase, db: Session = Depends(get_db) ):
    try:
        data = User(**user.dict())
        db.add(data)
        db.commit()
        return { "message": "Success", "data": User(**user.dict()) }
    except Exception as e:
        return {"message":"Failed.", "error": e}

#read
@user_route_app.get("/{id}")
async def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).filter(User.deleted == 0).first()
    if not user == None:
        return {"message": "Success", "data": user}
    else:
        return {"message": "Failed. User does not exist."} 
    
@user_route_app.get("/")
async def get_user(db: Session = Depends(get_db)):
    user = db.query(User).filter(User.deleted == 0).all()
    if not user == None:
        return {"message": "Success", "data": user}
    else:
        return {"message": "Failed. User does not exist."} 
    
#update
@user_route_app.put("/update/{id}")
async def update_user( user: UserBase, id: int, db: Session = Depends(get_db)):
    user_data = db.query(User).filter(User.id == id).filter(User.deleted == 0).first()
    if not user_data == None:
        try:
            user_data = {
                "username": user.username,
                "password": user.password,
                "budget": user.budget
            }
            db.query(User).filter(User.id == id).filter(User.deleted == 0).update(user_data)
            db.commit()
            return {"message": "Success", "data": user_data}
        except Exception as e:
            return {"message": "Failed.", "error": e}
    else:
        return {"message": "Failed. User does not exist."}
    

#delete
@user_route_app.put("/delete/{id}")
async def delete_user( id: int, db: Session = Depends(get_db)):
    user_data = db.query(User).filter(User.id == id).first()
    if not user_data == None:
        try:
            user_data = {
                "deleted": 1,
            }
            db.query(User).filter(User.id == id).update(user_data)
            db.commit()
            return {"message": "Success", "data": user_data}
        except Exception as e:
            return {"message": "Failed.", "error": e}
    else:
        return {"message": "Failed. User does not exist."}



