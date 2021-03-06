from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Medicines, MedicinesCreate, MedicinesUpdate, MedicinesBase
from services import medicine_services, get_by_name
from db.engine import create_session
from handler.error_code import *

router = APIRouter()

# get all medicines from database
@router.get("/medicines", tags=["medicine"], response_model=list[Medicines])
def read_medicines(
    skip: int = 0, limit: int = 200, session: Session = Depends(create_session)
):
    medicines = medicine_services.get_all(session, skip=skip, limit=limit)
    return medicines


# get 1 medicine from database
@router.get("/medicine/{id}", tags=["medicine"], response_model=MedicinesBase)
def read_medicine(id: int, session: Session = Depends(create_session)):
    medicine = medicine_services.get_one(session, id)
    if not medicine:
        raise HTTPException(status_code = 400, detail=HTTP_400_BAD_REQUEST.get(400002))
    return medicine


# create a brand new medicine
@router.post("/medicine", tags=["medicine"], response_model=MedicinesCreate)
def create_medicine(
    medicine_schemas: MedicinesCreate, session: Session = Depends(create_session)
):
    medicine = get_by_name(session, name=medicine_schemas.name)
    if medicine:
        raise HTTPException(
            status_code=400, detail="Medicine with this name already exist in database"
        )

    medicine = medicine_services.create_one(session, medicine_schemas)
    return medicine


# update some thing in a medicine
@router.put("/medicine/{id}", tags=["medicine"], response_model=MedicinesUpdate)
def update_medicine(
    id: int,
    mecdicine_schemas: MedicinesUpdate,
    session: Session = Depends(create_session),
):
    medicine = medicine_services.update(session, id=id, data=mecdicine_schemas)
    if not medicine:
        raise HTTPException(status_code=400, detail="ID not exist in database!")

    return medicine


# delete a medicine with ID
@router.delete("/medicine/{id}", tags=["medicine"])
def delete_medicine(id: int, session: Session = Depends(create_session)):
    medicine = medicine_services.get_one(session, id)
    if not medicine:
        raise HTTPException(status_code=404, detail=f"medicine with id {id} not found")

    else:
        medicine = medicine_services.delete_one(session, id)
        return f"Succesfully delete medicine with id: {id}"
