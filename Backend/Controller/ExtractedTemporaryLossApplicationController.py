from typing import List

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from Config.database import get_db
from Service import ExtractedTemporaryLossApplicationService

# router = APIRouter()
router = APIRouter(
    prefix="/extracted_temporary_loss_application",
)

@router.get("/extracted-temporary-loss-applications/")
async def get_extracted_temporary_loss_applications(db_session: Session = Depends(get_db)):
    return ExtractedTemporaryLossApplicationService.get_all_extracted_temporary_loss_applications(db_session)

@router.get("/extracted-temporary-loss-applications/{id}")
async def get_extracted_temporary_loss_application(id: int, db_session: Session = Depends(get_db)):
    return ExtractedTemporaryLossApplicationService.get_extracted_temporary_loss_application(db_session, id)

@router.post("/extract-temporary-loss-application/{user_id}")
async def extract_temporary_loss_application(files: List[UploadFile] = File(...), user_id: int = None, db_session: Session = Depends(get_db)):
    return await ExtractedTemporaryLossApplicationService.extract_temporary_loss_application(db_session=db_session, files=files, user_id=user_id)

# @router.put("/extracted-temporary-loss-applications/{id}")
# async def update_extracted_temporary_loss_application(id: int, update_request: ExtractedTemporaryLossApplicationUpdateRequest, db_session: Session = Depends(get_db)):
#     return ExtractedTemporaryLossApplicationService.update_extracted_temporary_loss_application(db_session, id, update_request)
#
# @router.delete("/extracted-temporary-loss-applications/{id}")
# async def delete_extracted_temporary_loss_application(id: int, db_session: Session = Depends(get_db)):
#     return ExtractedTemporaryLossApplicationService.delete_extracted_temporary_loss_application(db_session, id)