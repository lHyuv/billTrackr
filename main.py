from fastapi import FastAPI, status
from routes.user_route import user_route_app
from routes.category_route import category_route_app
from routes.billing_route import billing_route_app

app = FastAPI()
@app.get('/', status_code = status.HTTP_200_OK)

async def home():
    return {"message": "Welcome to Billtrackr API! To get more details about the endpoints, you can access /docs",
            "routes" : "/user, /category, /billing"}

app.include_router(user_route_app, prefix = "/user")
app.include_router(category_route_app, prefix = "/category")
app.include_router(billing_route_app, prefix = "/billing")