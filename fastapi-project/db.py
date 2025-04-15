from dotenv import load_dotenv
import os
from sqlmodel import Session, create_engine
from typing import Annotated
from fastapi import Depends

load_dotenv()


engine = create_engine(f"postgresql://{os.getenv("FASTAPI_USR")}:{os.getenv("FASTAPI_PWD")}@{os.getenv("FASTAPI_SERVER")}/{os.getenv("FASTAPI_DATABASE_NAME")}")

def get_session():
    # cerrar la session una vez que se haya utilizado
    with Session(engine) as session:
        yield session
        
        
SessionDep = Annotated[Session, Depends(get_session)]