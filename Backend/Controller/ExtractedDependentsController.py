from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Config.database import get_db
from Service import ExtractedDependentService
from Model.ExtractedDependentModel import ExtractedDependentResponse, ExtractedDependentCreateRequest, ExtractedDependentUpdateRequest

router = APIRouter()

@router.post("/extracted-dependents", response_model=ExtractedDependentResponse)
async def create_extracted_dependent(create_request: ExtractedDependentCreateRequest, db: Session = Depends(get_db)):
    return ExtractedDependentService.create_extracted_dependent(db_session=db, create_request=create_request)

@router.post("/extracted-dependents/multiple", response_model=ExtractedDependentResponse)
async def create_multiple_extracted_dependents(create_requests: List[ExtractedDependentCreateRequest], db: Session = Depends(get_db)):
    return ExtractedDependentService.create_multiple_extracted_dependents(db_session=db, create_requests=create_requests)

# @router.get("/extracted-dependents/{extracted_dependent_id}", response_model=ExtractedDependentResponse)
# async def get_extracted_dependent(extracted_dependent_id: int, db: Session = Depends(get_db)):
#     return ExtractedDependentService.get_extracted_dependent(extracted_dependent_id)
#
# @router.get("/extracted-dependents", response_model=ExtractedDependentResponse)
# async def get_all_extracted_dependents(db: Session = Depends(get_db)):
#     return ExtractedDependentService.get_all_extracted_dependents()

@router.put("/extracted-dependents/{extracted_dependent_id}", response_model=ExtractedDependentResponse)
async def update_extracted_dependent(extracted_dependent_id: int, update_request: ExtractedDependentUpdateRequest, db: Session = Depends(get_db)):
    return ExtractedDependentService.update_extracted_dependent(db_session=db, extracted_dependent_id=extracted_dependent_id, update_request=update_request)

@router.delete("/extracted-dependents/{extracted_dependent_id}", response_model=ExtractedDependentResponse)
async def delete_extracted_dependent(extracted_dependent_id: int, db: Session = Depends(get_db)):
    return ExtractedDependentService.delete_extracted_dependent(db_session=db, extracted_dependent_id=extracted_dependent_id)