from datetime import datetime, date
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

from Model.ApplicationTrackingModel import ApplicationTrackingDTO
from Model.DependentModel import DependentDTO, DependentUpdateRequest
from Model.ExtractedTemporaryLossApplicationModel import ExtractedTemporaryLossApplicationDTO
from Model.ResponseModel import BaseResponse
from Utils.Enums import ApplicationStatus


class TemporaryLossApplicationDTO(BaseModel):
    id: int
    # extracted_application_id: Optional[int] =None
    # application_number: Optional[str]
    full_name: Optional[str]
    id_number: Optional[str]
    date_of_birth: Optional[date]
    contact_number: Optional[str]
    email: Optional[str]
    address: Optional[str]
    nok_full_name: Optional[str]
    nok_contact_number: Optional[str]
    bank_name: Optional[str]
    account_number: Optional[str]
    branch_code: Optional[str]
    existing_insurance_with_other_company: Optional[str]
    existing_chronic_condition: Optional[str]
    status: Optional[ApplicationStatus]
    agent_full_name: Optional[str]
    agent_number: Optional[str]
    title: Optional[str]
    gender: Optional[str]
    b_date_of_birth: Optional[date]
    claim_ailment: Optional[str]
    claim_amount: Optional[str]
    declined_coverage: Optional[bool] = None
    declined_cover_reason: Optional[str]

    date_created: Optional[datetime]
    date_updated: Optional[datetime]

    # extracted_applications: Optional[List[ExtractedTemporaryLossApplicationDTO]] = None
    extracted_applications: Optional[List[ExtractedTemporaryLossApplicationDTO]] = []
    dependents: Optional[List[DependentDTO]]= None
    application_tracking_stages: Optional[List[ApplicationTrackingDTO]] = None


    model_config = ConfigDict(from_attributes=True)


class TemporaryLossApplicationCreateRequest(BaseModel):
    # extracted_application_id: Optional[int] =None
    full_name: Optional[str]
    id_number: Optional[str]
    date_of_birth: Optional[date]
    contact_number: Optional[str]
    email: Optional[str]
    address: Optional[str]
    nok_full_name: Optional[str]
    nok_contact_number: Optional[str]
    bank_name: Optional[str]
    account_number: Optional[str]
    branch_code: Optional[str]
    existing_insurance_with_other_company: Optional[str]
    existing_chronic_condition: Optional[str]
    agent_full_name: Optional[str]
    agent_number: Optional[str]
    title: Optional[str]
    gender: Optional[str]
    b_date_of_birth: Optional[date]
    claim_ailment: Optional[str]
    claim_amount: Optional[str]
    declined_coverage: Optional[bool] = None
    declined_cover_reason: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class TemporaryLossApplicationUpdateRequest(BaseModel):
    # extracted_application_id: Optional[int] =None
    id: Optional[int]
    full_name: Optional[str]
    id_number: Optional[str]
    date_of_birth: Optional[date]
    contact_number: Optional[str]
    email: Optional[str]
    address: Optional[str]
    nok_full_name: Optional[str]
    nok_contact_number: Optional[str]
    bank_name: Optional[str]
    account_number: Optional[str]
    branch_code: Optional[str]
    existing_insurance_with_other_company: Optional[str]
    existing_chronic_condition: Optional[str]
    status: Optional[ApplicationStatus]
    agent_full_name: Optional[str]
    agent_number: Optional[str]
    title: Optional[str]
    gender: Optional[str]
    b_date_of_birth: Optional[date]
    claim_ailment: Optional[str]
    claim_amount: Optional[str]
    declined_coverage: Optional[bool] = None
    declined_cover_reason: Optional[str]
    dependents: Optional[List[DependentUpdateRequest]] = None

    model_config = ConfigDict(from_attributes=True)


class TemporaryLossApplicationResponse(BaseResponse):
    temporary_loss_application: Optional[TemporaryLossApplicationDTO] = None
    temporary_loss_applications: Optional[List[TemporaryLossApplicationDTO]] = None