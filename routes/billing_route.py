from models.billing_model import Billing
from models.user_model import User
from schemas.billing_schema import BillingBase
from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, extract
from datetime import datetime

billing_route_app = APIRouter()

#create
@billing_route_app.post("/")
async def create_billing(billing: BillingBase, db: Session = Depends(get_db) ):
    try:
        data = Billing(**billing.dict())
        db.add(data)
        db.commit()
        return { "message": "Success", "data": Billing(**billing.dict()) }
    except:
        return {"message":"Failed. Billing already exists."}

#read
@billing_route_app.get("/get_by_id/{id}")
async def get_billing_by_id(id: int, db: Session = Depends(get_db)):
    billing = db.query(Billing).filter(Billing.id == id).filter(Billing.deleted == 0).first()
    total = db.query(func.sum(Billing.amount)).filter(Billing.id == id).filter(
    Billing.deleted == 0).scalar()
    count = db.query(func.count(Billing.amount)).filter(Billing.id == id).filter(
    Billing.deleted == 0).scalar()
    if not billing == None:
        return {"message": "Success", "data": billing, "total": total, "count": count}
    else:
        return {"message": "Failed. Billing does not exist."} 
    
@billing_route_app.get("/")
async def get_billing(db: Session = Depends(get_db)):
    billing = db.query(Billing).filter(Billing.deleted == 0).all()
    total = db.query(func.sum(Billing.amount)).filter(Billing.deleted == 0).scalar()
    count = db.query(func.count(Billing.amount)).filter(Billing.deleted == 0).scalar()
    if not billing == None:
        return {"message": "Success", "data": billing, "total": total, "count": count}
    else:
        return {"message": "Failed. Billing does not exist."} 
    
#update
@billing_route_app.put("/{id}")
async def update_billing( billing: BillingBase, id: int, db: Session = Depends(get_db)):
    billing_data = db.query(Billing).filter(Billing.id == id).filter(Billing.deleted == 0).first()
    if not billing_data == None:
        try:
            billing_data = {
                "remarks": billing.remarks,
                "user_id": billing.user_id,
                "category_id": billing.category_id,
                "billing_date": billing.billing_date,
                "amount": billing.amount
            }
            db.query(Billing).filter(Billing.id == id).filter(Billing.deleted == 0).update(billing_data)
            db.commit()
            return {"message": "Success", "data": billing_data}
        except Exception as e:
            return {"message": "Failed.", "error": e}
    else:
        return {"message": "Failed. Billing does not exist."}
    

#delete
@billing_route_app.put("/delete/{id}")
async def update_billing( id: int, db: Session = Depends(get_db)):
    billing_data = db.query(Billing).filter(Billing.id == id).first()
    if not billing_data == None:
        try:
            billing_data = {
                "deleted": 1,
            }
            db.query(Billing).filter(Billing.id == id).update(billing_data)
            db.commit()
            return {"message": "Success", "data": billing_data}
        except Exception as e:
            return {"message": "Failed.", "error": e}
    else:
        return {"message": "Failed. Billing does not exist."}
    
#custom routes

@billing_route_app.get("/get_by_user_id/{user_id}")
async def get_by_user_id(user_id: int, db: Session = Depends(get_db)):
 #   billing = db.query(func.sum(Billing.amount)).filter(Billing.deleted == 0).first()
    try:
        billing = db.query(Billing).filter(Billing.user_id == user_id).filter(Billing.deleted == 0).all()
        total = db.query(func.sum(Billing.amount)).filter(Billing.deleted == 0).filter(
            Billing.user_id == user_id).scalar()
        count = db.query(func.count(Billing.amount)).filter(Billing.deleted == 0).filter(
            Billing.user_id == user_id).scalar()
        budget = db.query(User.budget).filter(User.id == user_id).scalar() - float(total)
        if not billing == []:
            return {"message": "Success", "data": billing, "total": total, "count": count, "budget": budget}
        else:
            return {"message": "Failed. Billing does not exist."} 
    except Exception as e:
        return {"message": "Failed", "error" : e} 
    
@billing_route_app.get("/get_by_user_id_and_date/{user_id}/datefrom/{datefrom}/dateto/{dateto}")
async def get_by_user_and_date(user_id: int, datefrom: datetime, dateto: datetime, db: Session = Depends(get_db)):
    try:
        billing = db.query(Billing).filter(Billing.user_id == user_id).filter(
        Billing.deleted == 0).filter(Billing.billing_date.between(datefrom, dateto)).all()
        total = db.query(func.sum(Billing.amount)).filter(Billing.deleted == 0).filter(
        Billing.user_id == user_id).filter(Billing.billing_date.between(datefrom, dateto)).scalar()
        count = db.query(func.count(Billing.amount)).filter(Billing.deleted == 0).filter(
        Billing.user_id == user_id).filter(Billing.billing_date.between(datefrom, dateto)).scalar()
        budget = db.query(User.budget).filter(User.id == user_id).scalar() - float(total)
        if not billing == []:
            return {"message": "Success", "data": billing, "total": total, "count": count, "budget": budget}
        else:
            return {"message": "Failed. Billing does not exist."} 
    except Exception as e:
        return {"message": "Failed", "error" : e} 
    
@billing_route_app.get("/get_by_user_id_and_current_month/{user_id}/")
async def get_by_user_and_current_month(user_id: int,  db: Session = Depends(get_db)):
    try:
        billing = db.query(Billing).filter(Billing.user_id == user_id).filter(
        Billing.deleted == 0).filter(extract('month',Billing.billing_date) == datetime.now().month).all()
        total = db.query(func.sum(Billing.amount)).filter(Billing.deleted == 0).filter(
        Billing.user_id == user_id).filter(extract('month',Billing.billing_date) == datetime.now().month).scalar()
        count = db.query(func.count(Billing.amount)).filter(Billing.deleted == 0).filter(
        Billing.user_id == user_id).filter(extract('month',Billing.billing_date) == datetime.now().month).scalar()
        budget = db.query(User.budget).filter(User.id == user_id).scalar() - float(total)
        if not billing == []:
            return {"message": "Success", "data": billing, "total": total, "count": count, "budget": budget}
        else:
            return {"message": "Failed. Billing does not exist."} 
    except Exception as e:
        return {"message": "Failed", "error" : e} 
    
@billing_route_app.get("/get_by_user_id_and_current_year/{user_id}/")
async def get_by_user_and_current_year(user_id: int,  db: Session = Depends(get_db)):
    try:
        billing = db.query(Billing).filter(Billing.user_id == user_id).filter(
        Billing.deleted == 0).filter(extract('year',Billing.billing_date) == datetime.now().year).all()
        total = db.query(func.sum(Billing.amount)).filter(Billing.deleted == 0).filter(
        Billing.user_id == user_id).filter(extract('year',Billing.billing_date) == datetime.now().year).scalar()
        count = db.query(func.count(Billing.amount)).filter(Billing.deleted == 0).filter(
        Billing.user_id == user_id).filter(extract('year',Billing.billing_date) == datetime.now().year).scalar()
        budget = db.query(User.budget).filter(User.id == user_id).scalar() - float(total)
        if not billing == []:
            return {"message": "Success", "data": billing, "total": total, "count": count, "budget": budget}
        else:
            return {"message": "Failed. Billing does not exist."} 
    except Exception as e:
        return {"message": "Failed", "error" : e} 


