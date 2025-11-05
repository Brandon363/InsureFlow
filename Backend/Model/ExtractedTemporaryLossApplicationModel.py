from pydantic import BaseModel, ConfigDict
from datetime import date, datetime

from Model.ApplicationTrackingModel import ApplicationTrackingDTO
from Model.ExtractedDependentModel import ExtractedDependentDTO
from Model.ResponseModel import BaseResponse
from Utils.Enums import ApplicationStatus, EntityStatus
from typing import Optional, List


class ExtractedTemporaryLossApplicationDTO(BaseModel):
    id: Optional[int] = None
    application_id: Optional[int] = None
    full_name: Optional[str] = None
    full_name_confidence: Optional[float] = None
    id_number: Optional[str] = None
    id_number_confidence: Optional[float] = None
    date_of_birth: Optional[date] = None
    date_of_birth_confidence: Optional[float] = None
    contact_number: Optional[str] = None
    contact_number_confidence: Optional[float] = None
    email: Optional[str] = None
    email_confidence: Optional[float] = None
    address: Optional[str] = None
    address_confidence: Optional[float] = None
    nok_full_name: Optional[str] = None
    nok_full_name_confidence: Optional[float] = None
    nok_contact_number: Optional[str] = None
    nok_contact_number_confidence: Optional[float] = None
    bank_name: Optional[str] = None
    bank_name_confidence: Optional[float] = None
    account_number: Optional[str] = None
    account_number_confidence: Optional[float] = None
    branch_code: Optional[str] = None
    branch_code_confidence: Optional[float] = None
    existing_insurance_with_other_company: Optional[str] = None
    existing_insurance_with_other_company_confidence: Optional[float] = None
    existing_chronic_condition: Optional[str] = None
    existing_chronic_condition_confidence: Optional[float] = None
    agent_full_name: Optional[str] = None
    agent_full_name_confidence: Optional[float] = None
    agent_number: Optional[str] = None
    agent_number_confidence: Optional[float] = None
    title: Optional[str] = None
    title_confidence: Optional[float] = None
    gender: Optional[str] = None
    gender_confidence: Optional[float] = None
    b_date_of_birth: Optional[date] = None
    b_date_of_birth_confidence: Optional[float] = None
    claim_ailment: Optional[str] = None
    claim_ailment_confidence: Optional[float] = None
    claim_amount: Optional[str] = None
    claim_amount_confidence: Optional[float] = None
    declined_coverage: Optional[bool] = None
    declined_coverage_confidence: Optional[float] = None
    declined_cover_reason: Optional[str] = None
    declined_cover_reason_confidence: Optional[float] = None
    overall_accuracy: Optional[float] = None
    status: Optional[ApplicationStatus] = None
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None
    entity_status: Optional[EntityStatus] = None

    extracted_dependents: Optional[List[ExtractedDependentDTO]] = None
    application_tracking_stages: Optional[List[ApplicationTrackingDTO]] = None

    model_config = ConfigDict(from_attributes=True)


class ExtractedTemporaryLossApplicationCreateRequest(BaseModel):
    application_id: Optional[int] = None
    full_name: Optional[str] = None
    full_name_confidence: Optional[float] = None
    id_number: Optional[str] = None
    id_number_confidence: Optional[float] = None
    date_of_birth: Optional[date] = None
    date_of_birth_confidence: Optional[float] = None
    contact_number: Optional[str] = None
    contact_number_confidence: Optional[float] = None
    email: Optional[str] = None
    email_confidence: Optional[float] = None
    address: Optional[str] = None
    address_confidence: Optional[float] = None
    nok_full_name: Optional[str] = None
    nok_full_name_confidence: Optional[float] = None
    nok_contact_number: Optional[str] = None
    nok_contact_number_confidence: Optional[float] = None
    bank_name: Optional[str] = None
    bank_name_confidence: Optional[float] = None
    account_number: Optional[str] = None
    account_number_confidence: Optional[float] = None
    branch_code: Optional[str] = None
    branch_code_confidence: Optional[float] = None
    existing_insurance_with_other_company: Optional[str] = None
    existing_insurance_with_other_company_confidence: Optional[float] = None
    existing_chronic_condition: Optional[str] = None
    existing_chronic_condition_confidence: Optional[float] = None
    agent_full_name: Optional[str] = None
    agent_full_name_confidence: Optional[float] = None
    agent_number: Optional[str] = None
    agent_number_confidence: Optional[float] = None
    title: Optional[str] = None
    title_confidence: Optional[float] = None
    gender: Optional[str] = None
    gender_confidence: Optional[float] = None
    b_date_of_birth: Optional[date] = None
    b_date_of_birth_confidence: Optional[float] = None
    claim_ailment: Optional[str] = None
    claim_ailment_confidence: Optional[float] = None
    claim_amount: Optional[str] = None
    claim_amount_confidence: Optional[float] = None
    declined_coverage: Optional[bool] = None
    declined_coverage_confidence: Optional[float] = None
    declined_cover_reason: Optional[str] = None
    declined_cover_reason_confidence: Optional[float] = None
    overall_accuracy: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class ExtractedTemporaryLossApplicationUpdateRequest(BaseModel):
    application_id: Optional[int] = None
    full_name: Optional[str] = None
    full_name_confidence: Optional[float] = None
    id_number: Optional[str] = None
    id_number_confidence: Optional[float] = None
    date_of_birth: Optional[date] = None
    date_of_birth_confidence: Optional[float] = None
    contact_number: Optional[str] = None
    contact_number_confidence: Optional[float] = None
    email: Optional[str] = None
    email_confidence: Optional[float] = None
    address: Optional[str] = None
    address_confidence: Optional[float] = None
    nok_full_name: Optional[str] = None
    nok_full_name_confidence: Optional[float] = None
    nok_contact_number: Optional[str] = None
    nok_contact_number_confidence: Optional[float] = None
    bank_name: Optional[str] = None
    bank_name_confidence: Optional[float] = None
    account_number: Optional[str] = None
    account_number_confidence: Optional[float] = None
    branch_code: Optional[str] = None
    branch_code_confidence: Optional[float] = None
    existing_insurance_with_other_company: Optional[str] = None
    existing_insurance_with_other_company_confidence: Optional[float] = None
    existing_chronic_condition: Optional[str] = None
    existing_chronic_condition_confidence: Optional[float] = None
    agent_full_name: Optional[str] = None
    agent_full_name_confidence: Optional[float] = None
    agent_number: Optional[str] = None
    agent_number_confidence: Optional[float] = None
    title: Optional[str] = None
    title_confidence: Optional[float] = None
    gender: Optional[str] = None
    gender_confidence: Optional[float] = None
    b_date_of_birth: Optional[date] = None
    b_date_of_birth_confidence: Optional[float] = None
    claim_ailment: Optional[str] = None
    claim_ailment_confidence: Optional[float] = None
    claim_amount: Optional[str] = None
    claim_amount_confidence: Optional[float] = None
    declined_coverage: Optional[bool] = None
    declined_coverage_confidence: Optional[float] = None
    declined_cover_reason: Optional[str] = None
    declined_cover_reason_confidence: Optional[float] = None
    overall_accuracy: Optional[float] = None
    status: Optional[ApplicationStatus] = None

    model_config = ConfigDict(from_attributes=True)


class ExtractedTemporaryLossApplicationResponse(BaseResponse):
    extracted_temporary_loss_application: Optional[ExtractedTemporaryLossApplicationDTO] = None
    extracted_temporary_loss_applications: Optional[List[ExtractedTemporaryLossApplicationDTO]] = None

    model_config = ConfigDict(from_attributes=True)