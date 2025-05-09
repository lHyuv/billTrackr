from models.billing_model import Billing
from schemas.billing_schema import BillingBase
from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session

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
@billing_route_app.get("/{id}")
async def get_billing_by_id(id: int, db: Session = Depends(get_db)):
    billing = db.query(Billing).filter(Billing.id == id).filter(Billing.deleted == 0).first()
    if not billing == None:
        return {"message": "Success", "data": billing}
    else:
        return {"message": "Failed. Billing does not exist."} 
    
@billing_route_app.get("/")
async def get_billing(db: Session = Depends(get_db)):
    billing = db.query(Billing).filter(Billing.deleted == 0).all()
    if not billing == None:
        return {"message": "Success", "data": billing}
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
                "date": billing.date
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
