import zoneinfo
from fastapi import FastAPI
from datetime import datetime
from models import Customer, CustomerCreate, Transaction, Invoice
from db import SessionDep

# app que contendra los endpoints
app = FastAPI()

COUNTRY_TMZ = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}


@app.get("/")
async def root():
    return {"message": "Hola FastAPI"}


@app.get("/time/{iso_code}")
async def time(iso_code: str):
    """
    ARGS: Tomar como parametro el codigo del pais
    RETURN: la hora actual de ese pais
    """
    iso = iso_code.upper()
    tmz_str = COUNTRY_TMZ.get(iso)
    tmz_str = zoneinfo.ZoneInfo(tmz_str)

    return {"message": datetime.now(tmz_str)}


current_id: int = 0
db_customer: list[Customer] = []


# crear un costumer
@app.post("/customers", response_model=Customer)  # pasarle el id del customer ya que create no lo mantiene
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    # crear un customer pasando el dict de los datos
    customer = Customer.model_validate(customer_data.model_dump())
    # esto se elabora en la db
    # customer.id = current_id + 1
    # agregar un id personalizado con la lista
    customer.id = len(db_customer)
    db_customer.append(customer)
    return customer


# obtener un listado de customers
@app.get("/customers", response_model=list[Customer])
async def list_customer():
    return db_customer


# obtener un solo customer con id
@app.get(
    "/customers/{id}", response_model=Customer
)  # se deja customer solo porque se va a obtener uno solo y no una lista
async def get_customer_id(id: int):
    # se obtiene la instancia de la clase de customer
    return next((item for item in db_customer if item.id == id))


@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data


@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data
