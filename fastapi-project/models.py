from pydantic import BaseModel
from sqlmodel import SQLModel


class CustomerBase(SQLModel):
    name: str
    description: str | None
    email: str
    age: int


class CustomerCreate(CustomerBase):
    pass


# se crea un sql model de customer base, heredando los demas campos y crea una tabla junto con id
class Customer(CustomerBase, table=True):
    id: int | None = None


class Transaction(BaseModel):
    id: int
    amount: float
    description: str


class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]  # se agrega una lista de transacciones
    total: float

    @property  # propiedad para el mismo
    def total(self):
        # hacer una suma de todos los mount en transactions
        return sum(transaction.amount for transaction in self.transactions)
