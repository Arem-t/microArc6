from fastapi import FastAPI, HTTPException, Depends, status, Form, Request, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import uvicorn
import os
from keycloak.keycloak_openid import KeycloakOpenID
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

KEYCLOAK_URL = "http://localhost:8180/"
KEYCLOAK_CLIENT_ID = "test_id"
KEYCLOAK_REALM = "test"
KEYCLOAK_CLIENT_SECRET = "Si4auFepVW08PEbgxUXeJ2cK6hjh6drG"

keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                 client_id=KEYCLOAK_CLIENT_ID,
                                 realm_name=KEYCLOAK_REALM,
                                 client_secret_key=KEYCLOAK_CLIENT_SECRET)

Instrumentator().instrument(app).expose(app)


@app.post("/get-token")
async def get_token(username: str = Form(...), password: str = Form(...)):
    try:
        token = keycloak_openid.token(grant_type=["password"],
                                      username=username,
                                      password=password)
        return token
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Не удалось получить токен")


def check_user_roles(token):
    try:
        token_info = keycloak_openid.introspect(token)
        if "test_role" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")


current_directory = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(current_directory, "test.db")
DATABASE_URL = f"sqlite:///{db_path}"
engine = create_engine(DATABASE_URL)

Base = declarative_base()


class Delivery(Base):
    __tablename__ = "deliveries"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, index=True)
    status = Column(String)


Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def simulate_payment(order_id: int):
    payment_status = "paid" if order_id % 2 == 0 else "pending"
    return {"order_id": order_id, "status": payment_status}


def create_delivery_and_record(db, order_id: int):
    payment_result = simulate_payment(order_id)
    delivery_status = "processed" if payment_result["status"] == "paid" else "not processed"

    db_delivery = Delivery(order_id=order_id, status=delivery_status)
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)

    return {"message": f"Processing delivery for order {order_id}", "delivery_id": db_delivery.id}


def get_access_token_from_header(request: Request):
    return request.headers["Authorization"]


@app.post("/delivery/{order_id}")
def create_delivery(order_id: int, token: str = Header(...)):
    if (check_user_roles(token)):
        db = SessionLocal()
        result = create_delivery_and_record(db, order_id)
        db.close()
        return result
    else:
        return "Wrong JWT Token"


@app.get("/delivery/{order_id}")
def read_delivery(order_id: int, token: str = Header(...)):
    if (check_user_roles(token)):
        db = SessionLocal()
        delivery = db.query(Delivery).filter(Delivery.order_id == order_id).first()
        db.close()

        if not delivery:
            raise HTTPException(status_code=404, detail="Delivery not found")

        return {"order_id": delivery.order_id, "status": delivery.status}
    else:
        return "Wrong JWT Token"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
