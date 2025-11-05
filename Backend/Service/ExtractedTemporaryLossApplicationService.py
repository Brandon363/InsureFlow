import base64
import os
from dateutil.parser import ParserError
from pathlib import Path
from typing import List
from fastapi import UploadFile
from PIL import Image
from io import BytesIO
import base64
from pypdf import PdfReader
from tempfile import NamedTemporaryFile

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from dateutil import parser
from dotenv import load_dotenv
from fastapi import File
from sqlalchemy.orm import Session

from Entity.ExtractedTemporaryLossApplicationEntity import ExtractedTemporaryLossApplicationEntity
from Model.ApplicationTrackingModel import ApplicationTrackingCreateRequest
from Model.DependentModel import DependentCreateRequest
from Model.DocumentModel import DocumentUpdate
from Model.ExtractedDependentModel import ExtractedDependentCreateRequest
from Model.ExtractedTemporaryLossApplicationModel import ExtractedTemporaryLossApplicationResponse, \
    ExtractedTemporaryLossApplicationCreateRequest
from Model.NotificationModel import NotificationCreate
from Model.TemporaryLossApplicationModel import TemporaryLossApplicationCreateRequest
from Repository import ExtractedTemporaryLossApplicationRepository
from Service import (DocumentService, NotificationService, ApplicationTrackingService, ExtractedDependentService,
                     DependentService, TemporaryLossApplicationService)
from Utils.Enums import DocumentType, NotificationType, ApplicationStage, ApplicationStatus

load_dotenv()

endpoint = os.getenv("AZURE_ENDPOINT")
key = os.getenv("AZURE_KEY")

document_intelligence_client = DocumentIntelligenceClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)


def get_extracted_temporary_loss_application(db_session: Session, id: int) -> ExtractedTemporaryLossApplicationResponse:
    extracted_application = ExtractedTemporaryLossApplicationRepository.find_extracted_temporary_loss_application_by_id(
        db_session, id)
    if extracted_application is None:
        return ExtractedTemporaryLossApplicationResponse(status_code=404, success=False,
                                                         message="Application not found")

    return ExtractedTemporaryLossApplicationResponse(status_code=200, success=True, message="Application found",
                                                     extracted_temporary_loss_application=extracted_application)


def get_all_extracted_temporary_loss_applications(db_session: Session) -> ExtractedTemporaryLossApplicationResponse:
    extracted_applications = ExtractedTemporaryLossApplicationRepository.find_all_extracted_temporary_loss_applications(
        db_session)
    if extracted_applications is None:
        return ExtractedTemporaryLossApplicationResponse(status_code=404, success=False,
                                                         message="Applications not found")

    return ExtractedTemporaryLossApplicationResponse(status_code=200, success=True, message="Applications found",
                                                     extracted_temporary_loss_applications=extracted_applications)


def create_extracted_temporary_loss_application(db_session: Session,
                                                create_request: ExtractedTemporaryLossApplicationCreateRequest) \
        -> ExtractedTemporaryLossApplicationResponse:
    # Create user entity
    user_entity = ExtractedTemporaryLossApplicationEntity(**create_request.dict())
    db_session.add(user_entity)
    db_session.commit()
    db_session.refresh(user_entity)

    return ExtractedTemporaryLossApplicationResponse(
        status_code=201, success=True, message="Application created successfully",
        extracted_temporary_loss_application=user_entity)


# async def extract_temporary_loss_application(db_session: Session, files: List[UploadFile],
#                                              user_id: int) -> ExtractedTemporaryLossApplicationResponse:
#     images = []
#     pdfs = []
#     for file in files:
#         file_content = await file.read()
#         try:
#             image = Image.open(BytesIO(file_content))
#             images.append(image)
#         except Exception as e:
#             try:
#                 # Check if it's a PDF
#                 pdf_reader = PdfReader(BytesIO(file_content))
#                 pdfs.append(file_content)
#             except Exception as e:
#                 print(f"Error opening file {file.filename}: Not a valid image or PDF")
#
#     if images:
#         # Save images as PDF
#         combined_image_path = "combined.pdf"
#         images[0].save(combined_image_path, "PDF", save_all=True, append_images=images[1:])
#         with open(combined_image_path, "rb") as f:
#             file_content = f.read()
#     elif pdfs:
#         # If all files are PDFs, you might want to merge them here
#         # For simplicity, let's just use the first PDF
#         file_content = pdfs[0]
#     else:
#         return ExtractedTemporaryLossApplicationResponse(
#             status_code=400,
#             success=False,
#             message="No valid images or PDFs found in the uploaded files",
#         )
#
#     # Create a temporary file
#     temp_file = NamedTemporaryFile(suffix=".pdf", delete=False)
#     temp_file.write(file_content)
#     temp_file.seek(0)  # Reset the file pointer to the beginning
#
#     # Create an UploadFile object
#     pdf_file = UploadFile(filename="combined.pdf", file=temp_file)
#
#     # Save file and get upload response
#     upload_response = await DocumentService.upload_document(db_session=db_session, file=pdf_file, user_id=user_id,
#                                                             document_type=DocumentType.CLAIM_DOCUMENT)
#
#     if not upload_response.success:
#         return ExtractedTemporaryLossApplicationResponse(status_code=upload_response.status_code, success=False,
#                                                          message=upload_response.message)
#     temp_file.close()
#     os.remove(temp_file.name)
#
#     # Extract data using Azure Document Intelligence
#     local_file_path = Path("backend") / upload_response.document.url
#     with open(local_file_path, "rb") as f:
#         image_data = f.read()
#         base64_image = base64.b64encode(image_data).decode("utf-8")
#
#     poller = document_intelligence_client.begin_analyze_document(
#         "Temporary_Loss_Of_Income_Protection_Proposal_Form_Extractor_v1",
#         body={"base64Source": base64_image}
#     )
#
#     extracted_data = poller.result()
#     for idx, id_document in enumerate(extracted_data.documents):
#         print("--------Recognizing ID document #{}--------".format(idx + 1))
#
#         # Extract fields
#         agent_full_name = id_document.fields.get("AgentFullName")
#         agent_number = id_document.fields.get("AgentNumber")
#         full_name = id_document.fields.get("FullName")
#         title = id_document.fields.get("Title")
#         gender = id_document.fields.get("Gender")
#         id_number = id_document.fields.get("IdNumber")
#         date_of_birth = id_document.fields.get("DateOfBirth")
#         contact_number = id_document.fields.get("ContactNumber")
#         email = id_document.fields.get("Email")
#         address = id_document.fields.get("Address")
#         nok_full_name = id_document.fields.get("NOK_FullName")
#         nok_contact_number = id_document.fields.get("NOK_ContactNumber")
#         bank_name = id_document.fields.get("BankName")
#         b_date_of_birth = id_document.fields.get("B_DateOfBirth")
#         account_number = id_document.fields.get("AccountNumber")
#         branch_code = id_document.fields.get("BranchCode")
#         existing_insurance_with_other_company = id_document.fields.get("ExistingInsuranceWithOtherCompany")
#         existing_chronic_condition = id_document.fields.get("ExistingChronicCondition")
#         claim_ailment = id_document.fields.get("ClaimAilment")
#         claim_amount = id_document.fields.get("ClaimAmount")
#         declined_coverage = id_document.fields.get("DeclinedCoverage")
#         declined_cover_reason = id_document.fields.get("DeclinedCoverReason")
#         dependents = id_document.fields.get("Dependents")
#
#         # Create extracted application entity
#         extracted_application = ExtractedTemporaryLossApplicationCreateRequest()
#
#         # Map extracted fields
#         extracted_application.full_name = full_name.value_string if full_name else None
#         extracted_application.full_name_confidence = full_name.confidence if full_name else None
#
#         extracted_application.id_number = id_number.value_string if id_number else None
#         extracted_application.id_number_confidence = id_number.confidence if id_number else None
#
#         extracted_application.date_of_birth = parser.parse(date_of_birth.value_string,
#                                                            dayfirst=True).date() if date_of_birth else None
#         extracted_application.date_of_birth_confidence = date_of_birth.confidence if date_of_birth else None
#
#         extracted_application.contact_number = contact_number.value_string if contact_number else None
#         extracted_application.contact_number_confidence = contact_number.confidence if contact_number else None
#
#         extracted_application.email = email.value_string if email else None
#         extracted_application.email_confidence = email.confidence if email else None
#
#         extracted_application.address = address.value_string if address else None
#         extracted_application.address_confidence = address.confidence if address else None
#
#         extracted_application.nok_full_name = nok_full_name.value_string if nok_full_name else None
#         extracted_application.nok_full_name_confidence = nok_full_name.confidence if nok_full_name else None
#
#         extracted_application.nok_contact_number = nok_contact_number.value_string if nok_contact_number else None
#         extracted_application.nok_contact_number_confidence = nok_contact_number.confidence if nok_contact_number else None
#
#         extracted_application.bank_name = bank_name.value_string if bank_name else None
#         extracted_application.bank_name_confidence = bank_name.confidence if bank_name else None
#
#         extracted_application.account_number = account_number.value_string if account_number else None
#         extracted_application.account_number_confidence = account_number.confidence if account_number else None
#
#         extracted_application.branch_code = branch_code.value_string if branch_code else None
#         extracted_application.branch_code_confidence = branch_code.confidence if branch_code else None
#
#         extracted_application.existing_insurance_with_other_company = existing_insurance_with_other_company.value_string if existing_insurance_with_other_company else None
#         extracted_application.existing_insurance_with_other_company_confidence = existing_insurance_with_other_company.confidence if existing_insurance_with_other_company else None
#
#         extracted_application.existing_chronic_condition = existing_chronic_condition.value_string if existing_chronic_condition else None
#         extracted_application.existing_chronic_condition_confidence = existing_chronic_condition.confidence if existing_chronic_condition else None
#
#         extracted_application.agent_full_name = agent_full_name.value_string if agent_full_name else None
#         extracted_application.agent_full_name_confidence = agent_full_name.confidence if agent_full_name else None
#
#         extracted_application.agent_number = agent_number.value_string if agent_number else None
#         extracted_application.agent_number_confidence = agent_number.confidence if agent_number else None
#
#         extracted_application.title = title.value_string if title else None
#         extracted_application.title_confidence = title.confidence if title else None
#
#         extracted_application.gender = gender.value_string if gender else None
#         extracted_application.gender_confidence = gender.confidence if gender else None
#
#         extracted_application.b_date_of_birth = parser.parse(
#             b_date_of_birth.value_string).date() if b_date_of_birth else None
#
#         extracted_application.b_date_of_birth_confidence = b_date_of_birth.confidence if b_date_of_birth else None
#
#         extracted_application.claim_ailment = claim_ailment.value_string if claim_ailment else None
#         extracted_application.claim_ailment_confidence = claim_ailment.confidence if claim_ailment else None
#
#         extracted_application.claim_amount = claim_amount.value_string if claim_amount else None
#         extracted_application.claim_amount_confidence = claim_amount.confidence if claim_amount else None
#
#         # extracted_application.declined_coverage = declined_coverage.value_string if declined_coverage else None
#         extracted_application.declined_coverage = declined_coverage.value_selection_mark == 'selected' if declined_coverage else None
#         # print(declined_coverage)
#         extracted_application.declined_coverage_confidence = declined_coverage.confidence if declined_coverage else None
#
#         extracted_application.declined_cover_reason = declined_cover_reason.value_string if declined_cover_reason else None
#         extracted_application.declined_cover_reason_confidence = declined_cover_reason.confidence if declined_cover_reason else None
#
#         # Calculate overall accuracy
#         total_confidence = 0
#         count = 0
#
#         fields = [
#             ("full_name", extracted_application.full_name_confidence),
#             ("id_number", extracted_application.id_number_confidence),
#             ("date_of_birth", extracted_application.date_of_birth_confidence),
#             ("contact_number", extracted_application.contact_number_confidence),
#             ("email", extracted_application.email_confidence),
#             ("address", extracted_application.address_confidence),
#             ("nok_full_name", extracted_application.nok_full_name_confidence),
#             ("nok_contact_number", extracted_application.nok_contact_number_confidence),
#             ("bank_name", extracted_application.bank_name_confidence),
#             ("account_number", extracted_application.account_number_confidence),
#             ("branch_code", extracted_application.branch_code_confidence),
#             ("existing_insurance_with_other_company",
#              extracted_application.existing_insurance_with_other_company_confidence),
#             ("existing_chronic_condition", extracted_application.existing_chronic_condition_confidence),
#             ("agent_full_name", extracted_application.agent_full_name_confidence),
#             ("agent_number", extracted_application.agent_number_confidence),
#             ("title", extracted_application.title_confidence),
#             ("gender", extracted_application.gender_confidence),
#             ("b_date_of_birth", extracted_application.b_date_of_birth_confidence),
#             ("claim_ailment", extracted_application.claim_ailment_confidence),
#             ("claim_amount", extracted_application.claim_amount_confidence),
#             ("declined_coverage", extracted_application.declined_coverage_confidence),
#             ("declined_cover_reason", extracted_application.declined_cover_reason_confidence),
#         ]
#
#         for field, confidence in fields:
#             if confidence is not None:
#                 total_confidence += confidence
#                 count += 1
#
#         if count > 0:
#             overall_accuracy = total_confidence / count
#         else:
#             overall_accuracy = 0
#
#         extracted_application.overall_accuracy = overall_accuracy
#
#
#         # save the copy in the system
#         saved_application_response = TemporaryLossApplicationService.create_temporary_loss_application(
#             db_session=db_session,
#             create_request=TemporaryLossApplicationCreateRequest(
#                 **extracted_application.dict()))
#         if not saved_application_response.success:
#             return ExtractedTemporaryLossApplicationResponse(**saved_application_response.dict())
#
#         extracted_application.application_id = saved_application_response.temporary_loss_application.id
#
#         # Save extracted application
#         saved_extracted_application_response = create_extracted_temporary_loss_application(
#             db_session=db_session,
#             create_request=extracted_application)
#         if not saved_extracted_application_response.success:
#             return saved_extracted_application_response
#
#         # save the extracted dependents
#         extracted_dependent_create_requests = []
#         if dependents and dependents.value_array:
#             print("Dependents: ", len(dependents.value_array))
#             for dependent in dependents.value_array:
#                 if dependent.value_object:
#                     dependent_full_name = dependent.value_object.get("FullName")
#                     dependent_id_number = dependent.value_object.get("IdNumber")
#                     dependent_date_of_birth = dependent.value_object.get("DateOfBirth")
#                     dependent_age = dependent.value_object.get("Age")
#                     dependent_gender = dependent.value_object.get("Gender")
#                     dependent_relationship = dependent.value_object.get("Relationship")
#
#                     create_request = ExtractedDependentCreateRequest(
#                         extracted_application_id=saved_extracted_application_response.extracted_temporary_loss_application.id,
#                         full_name=dependent_full_name.value_string if dependent_full_name else None,
#                         full_name_confidence=dependent_full_name.confidence if dependent_full_name else None,
#                         id_number=dependent_id_number.value_string if dependent_id_number else None,
#                         id_number_confidence=dependent_id_number.confidence if dependent_id_number else None,
#                         date_of_birth=parser.parse(
#                             dependent_date_of_birth.value_string).date() if dependent_date_of_birth else None,
#                         date_of_birth_confidence=dependent_date_of_birth.confidence if dependent_date_of_birth else None,
#                         age=int(dependent_age.value_string) if dependent_age else None,
#                         age_confidence=dependent_age.confidence if dependent_age else None,
#                         gender=dependent_gender.value_string if dependent_gender else None,
#                         gender_confidence=dependent_gender.confidence if dependent_gender else None,
#                         client_relationship=dependent_relationship.value_string if dependent_relationship else None,
#                         client_relationship_confidence=dependent_relationship.confidence if dependent_relationship else None,
#                     )
#                     extracted_dependent_create_requests.append(create_request)
#
#         if len(extracted_dependent_create_requests) > 0:
#             # create the extracted
#             create_extracted_dependents_response = ExtractedDependentService.create_multiple_extracted_dependents(
#                 create_requests=extracted_dependent_create_requests, db_session=db_session
#             )
#             if not create_extracted_dependents_response.success:
#                 return ExtractedTemporaryLossApplicationResponse(**create_extracted_dependents_response.dict())
#
#             # create the actual
#             create_dependents_response = DependentService.create_multiple_dependents(
#                 create_requests=[DependentCreateRequest(
#                     **request.dict(), application_id=saved_application_response.temporary_loss_application.id
#                 ) for request in extracted_dependent_create_requests],
#                 db_session=db_session
#             )
#             if not create_dependents_response.success:
#                 return ExtractedTemporaryLossApplicationResponse(**create_dependents_response.dict())
#
#         create_track_response = ApplicationTrackingService.create_application_tracking(
#             create_request=ApplicationTrackingCreateRequest(
#                 application_id=saved_application_response.temporary_loss_application.id,
#                 stage=ApplicationStage.SUBMITTED,
#                 status=ApplicationStatus.PENDING,
#                 # user_id=user_id,
#                 notes=None,
#                 action_performed_by_id=user_id,
#             ), db_session=db_session)
#
#         if not create_track_response.success:
#             return ExtractedTemporaryLossApplicationResponse(
#                 status_code=create_track_response.status_code, success=False, message=create_track_response.message)
#
#         # Create notification
#         # notification_request = NotificationCreate(
#         #     user_id=user_id,
#         #     notification_type=NotificationType.APPLICATION_UPDATE,
#         #     title="Application Submitted", message="Your temporary loss application has been submitted",
#         #     path_id=str(saved_application_response.temporary_loss_application.id)
#         # )
#         #
#         # notification_response = NotificationService.create_notification(create_request=notification_request,
#         #                                                                 db_session=db_session)
#         # if not notification_response.success:
#         #     print(notification_response.message)
#
#         refreshed_application_response = get_extracted_temporary_loss_application(
#             db_session=db_session,
#             id=saved_extracted_application_response.extracted_temporary_loss_application.id)
#         if not refreshed_application_response.success:
#             return refreshed_application_response
#
#         return ExtractedTemporaryLossApplicationResponse(
#             status_code=201, success=True,
#             message="Application extracted successfully",
#             extracted_temporary_loss_application=refreshed_application_response.extracted_temporary_loss_application,
#             # notification=notification_response.notification if notification_response.notification else None
#         )
async def extract_temporary_loss_application(db_session: Session, files: List[UploadFile],
                                             user_id: int) -> ExtractedTemporaryLossApplicationResponse:
    images = []
    pdfs = []
    for file in files:
        file_content = await file.read()
        try:
            image = Image.open(BytesIO(file_content))
            images.append(image)
        except Exception as e:
            try:
                # Check if it's a PDF
                pdf_reader = PdfReader(BytesIO(file_content))
                pdfs.append(file_content)
            except Exception as e:
                print(f"Error opening file {file.filename}: Not a valid image or PDF")

    if images:
        # Save images as PDF
        combined_image_path = "combined.pdf"
        images[0].save(combined_image_path, "PDF", save_all=True, append_images=images[1:])
        with open(combined_image_path, "rb") as f:
            file_content = f.read()
    elif pdfs:
        # If all files are PDFs, you might want to merge them here
        # For simplicity, let's just use the first PDF
        file_content = pdfs[0]
    else:
        return ExtractedTemporaryLossApplicationResponse(
            status_code=400,
            success=False,
            message="No valid images or PDFs found in the uploaded files",
        )

    # Create a temporary file
    temp_file = NamedTemporaryFile(suffix=".pdf", delete=False)
    temp_file.write(file_content)
    temp_file.seek(0)  # Reset the file pointer to the beginning

    # Create an UploadFile object
    pdf_file = UploadFile(filename="combined.pdf", file=temp_file)

    # Save file and get upload response
    upload_response = await DocumentService.upload_document(db_session=db_session, file=pdf_file, user_id=user_id,
                                                            document_type=DocumentType.CLAIM_DOCUMENT)

    if not upload_response.success:
        return ExtractedTemporaryLossApplicationResponse(status_code=upload_response.status_code, success=False,
                                                         message=upload_response.message)
    temp_file.close()
    os.remove(temp_file.name)

    # Extract data using Azure Document Intelligence
    local_file_path = Path("backend") / upload_response.document.url
    with open(local_file_path, "rb") as f:
        image_data = f.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")

    poller = document_intelligence_client.begin_analyze_document(
        "Temporary_Loss_Of_Income_Protection_Proposal_Form_Extractor_v1",
        body={"base64Source": base64_image}
    )

    extracted_data = poller.result()

    for idx, id_document in enumerate(extracted_data.documents):
        print("--------Recognizing ID document #{}--------".format(idx + 1))

        # check if its worth saving
        if id_document.confidence < 0.3:
            return ExtractedTemporaryLossApplicationResponse(
                status_code=400, success=False,
                message=f"Accuracy of {id_document.confidence * 100}% is too low, either no form detected or poor picture quality")

        print(id_document.confidence)

        # Extract fields
        agent_full_name = id_document.fields.get("AgentFullName")
        agent_number = id_document.fields.get("AgentNumber")
        full_name = id_document.fields.get("FullName")
        title = id_document.fields.get("Title")
        gender = id_document.fields.get("Gender")
        id_number = id_document.fields.get("IdNumber")
        date_of_birth = id_document.fields.get("DateOfBirth")
        contact_number = id_document.fields.get("ContactNumber")
        email = id_document.fields.get("Email")
        address = id_document.fields.get("Address")
        nok_full_name = id_document.fields.get("NOK_FullName")
        nok_contact_number = id_document.fields.get("NOK_ContactNumber")
        bank_name = id_document.fields.get("BankName")
        b_date_of_birth = id_document.fields.get("B_DateOfBirth")
        account_number = id_document.fields.get("AccountNumber")
        branch_code = id_document.fields.get("BranchCode")
        existing_insurance_with_other_company = id_document.fields.get("ExistingInsuranceWithOtherCompany")
        existing_chronic_condition = id_document.fields.get("ExistingChronicCondition")
        claim_ailment = id_document.fields.get("ClaimAilment")
        claim_amount = id_document.fields.get("ClaimAmount")
        declined_coverage = id_document.fields.get("DeclinedCoverage")
        declined_cover_reason = id_document.fields.get("DeclinedCoverReason")
        dependents = id_document.fields.get("Dependents")

        # Create extracted application entity
        extracted_application = ExtractedTemporaryLossApplicationCreateRequest()

        # Map extracted fields
        extracted_application.full_name = full_name.value_string if full_name else None
        extracted_application.full_name_confidence = full_name.confidence if full_name else None

        extracted_application.id_number = id_number.value_string if id_number else None
        extracted_application.id_number_confidence = id_number.confidence if id_number else None

        try:
            extracted_application.date_of_birth = parse_date(date_of_birth)
        except Exception as e:
            extracted_application.date_of_birth = None
            print("Error parsing date of birth")

        extracted_application.date_of_birth_confidence = date_of_birth.confidence if date_of_birth else None

        extracted_application.contact_number = contact_number.value_string if contact_number else None
        extracted_application.contact_number_confidence = contact_number.confidence if contact_number else None

        extracted_application.email = email.value_string if email else None
        extracted_application.email_confidence = email.confidence if email else None

        extracted_application.address = address.value_string if address else None
        extracted_application.address_confidence = address.confidence if address else None

        extracted_application.nok_full_name = nok_full_name.value_string if nok_full_name else None
        extracted_application.nok_full_name_confidence = nok_full_name.confidence if nok_full_name else None

        extracted_application.nok_contact_number = nok_contact_number.value_string if nok_contact_number else None
        extracted_application.nok_contact_number_confidence = nok_contact_number.confidence if nok_contact_number else None

        extracted_application.bank_name = bank_name.value_string if bank_name else None
        extracted_application.bank_name_confidence = bank_name.confidence if bank_name else None

        extracted_application.account_number = account_number.value_string if account_number else None
        extracted_application.account_number_confidence = account_number.confidence if account_number else None

        extracted_application.branch_code = branch_code.value_string if branch_code else None
        extracted_application.branch_code_confidence = branch_code.confidence if branch_code else None

        extracted_application.existing_insurance_with_other_company = existing_insurance_with_other_company.value_string if existing_insurance_with_other_company else None
        extracted_application.existing_insurance_with_other_company_confidence = existing_insurance_with_other_company.confidence if existing_insurance_with_other_company else None

        extracted_application.existing_chronic_condition = existing_chronic_condition.value_string if existing_chronic_condition else None
        extracted_application.existing_chronic_condition_confidence = existing_chronic_condition.confidence if existing_chronic_condition else None

        extracted_application.agent_full_name = agent_full_name.value_string if agent_full_name else None
        extracted_application.agent_full_name_confidence = agent_full_name.confidence if agent_full_name else None

        extracted_application.agent_number = agent_number.value_string if agent_number else None
        extracted_application.agent_number_confidence = agent_number.confidence if agent_number else None

        extracted_application.title = title.value_string if title else None
        extracted_application.title_confidence = title.confidence if title else None

        extracted_application.gender = gender.value_string if gender else None
        extracted_application.gender_confidence = gender.confidence if gender else None

        try:
            extracted_application.b_date_of_birth = parse_date(b_date_of_birth)
        except Exception as e:
            extracted_application.b_date_of_birth = None
            print("Error parsing B date of birth")

        extracted_application.b_date_of_birth_confidence = b_date_of_birth.confidence if b_date_of_birth else None

        extracted_application.claim_ailment = claim_ailment.value_string if claim_ailment else None
        extracted_application.claim_ailment_confidence = claim_ailment.confidence if claim_ailment else None

        extracted_application.claim_amount = claim_amount.value_string if claim_amount else None
        extracted_application.claim_amount_confidence = claim_amount.confidence if claim_amount else None

        extracted_application.declined_coverage = declined_coverage.value_selection_mark == 'selected' if declined_coverage else None
        extracted_application.declined_coverage_confidence = declined_coverage.confidence if declined_coverage else None

        extracted_application.declined_cover_reason = declined_cover_reason.value_string if declined_cover_reason else None
        extracted_application.declined_cover_reason_confidence = declined_cover_reason.confidence if declined_cover_reason else None

        # Calculate overall accuracy
        total_confidence = 0
        count = 0

        fields = [
            ("full_name", extracted_application.full_name_confidence),
            ("id_number", extracted_application.id_number_confidence),
            ("date_of_birth", extracted_application.date_of_birth_confidence),
            ("contact_number", extracted_application.contact_number_confidence),
            ("email", extracted_application.email_confidence),
            ("address", extracted_application.address_confidence),
            ("nok_full_name", extracted_application.nok_full_name_confidence),
            ("nok_contact_number", extracted_application.nok_contact_number_confidence),
            ("bank_name", extracted_application.bank_name_confidence),
            ("account_number", extracted_application.account_number_confidence),
            ("branch_code", extracted_application.branch_code_confidence),
            ("existing_insurance_with_other_company",
             extracted_application.existing_insurance_with_other_company_confidence),
            ("existing_chronic_condition", extracted_application.existing_chronic_condition_confidence),
            ("agent_full_name", extracted_application.agent_full_name_confidence),
            ("agent_number", extracted_application.agent_number_confidence),
            ("title", extracted_application.title_confidence),
            ("gender", extracted_application.gender_confidence),
            ("b_date_of_birth", extracted_application.b_date_of_birth_confidence),
            ("claim_ailment", extracted_application.claim_ailment_confidence),
            ("claim_amount", extracted_application.claim_amount_confidence),
            ("declined_coverage", extracted_application.declined_coverage_confidence),
            ("declined_cover_reason", extracted_application.declined_cover_reason_confidence),
        ]

        for field, confidence in fields:
            if confidence is not None:
                total_confidence += confidence
                count += 1

        if count > 0:
            overall_accuracy = total_confidence / count
        else:
            overall_accuracy = 0

        extracted_application.overall_accuracy = overall_accuracy

        # save the copy in the system
        saved_application_response = TemporaryLossApplicationService.create_temporary_loss_application(
            db_session=db_session,
            create_request=TemporaryLossApplicationCreateRequest(
                **extracted_application.dict()))
        if not saved_application_response.success:
            return ExtractedTemporaryLossApplicationResponse(**saved_application_response.dict())

        extracted_application.application_id = saved_application_response.temporary_loss_application.id

        # Save extracted application
        saved_extracted_application_response = create_extracted_temporary_loss_application(
            db_session=db_session,
            create_request=extracted_application)
        if not saved_extracted_application_response.success:
            return saved_extracted_application_response

        # save the extracted dependents
        extracted_dependent_create_requests = []
        if dependents and dependents.value_array:
            print("Dependents: ", len(dependents.value_array))
            for dependent in dependents.value_array:
                if dependent.value_object:
                    dependent_full_name = dependent.value_object.get("FullName")
                    dependent_id_number = dependent.value_object.get("IdNumber")
                    dependent_date_of_birth = dependent.value_object.get("DateOfBirth")
                    dependent_age = dependent.value_object.get("Age")
                    dependent_gender = dependent.value_object.get("Gender")
                    dependent_relationship = dependent.value_object.get("Relationship")

                    try:
                        parsed_date_of_birth = parse_date(dependent_date_of_birth)
                    except Exception as e:
                        parsed_date_of_birth = None
                        print("Error parsing dependent date of birth")

                    create_request = ExtractedDependentCreateRequest(
                        extracted_application_id=saved_extracted_application_response.extracted_temporary_loss_application.id,
                        full_name=dependent_full_name.value_string if dependent_full_name else None,
                        full_name_confidence=dependent_full_name.confidence if dependent_full_name else None,
                        id_number=dependent_id_number.value_string if dependent_id_number else None,
                        id_number_confidence=dependent_id_number.confidence if dependent_id_number else None,
                        date_of_birth=parsed_date_of_birth,
                        date_of_birth_confidence=dependent_date_of_birth.confidence if dependent_date_of_birth else None,
                        age=int(dependent_age.value_string) if dependent_age else None,
                        age_confidence=dependent_age.confidence if dependent_age else None,
                        gender=dependent_gender.value_string if dependent_gender else None,
                        gender_confidence=dependent_gender.confidence if dependent_gender else None,
                        client_relationship=dependent_relationship.value_string if dependent_relationship else None,
                        client_relationship_confidence=dependent_relationship.confidence if dependent_relationship else None,
                    )
                    extracted_dependent_create_requests.append(create_request)

        if len(extracted_dependent_create_requests) > 0:
            for request in extracted_dependent_create_requests:

                # create the actual
                create_dependents_response = DependentService.create_dependent(
                    create_request=DependentCreateRequest(
                        **request.dict(),
                        application_id=saved_application_response.temporary_loss_application.id
                    ),
                    db_session=db_session
                )

                if not create_dependents_response.success:
                    return ExtractedTemporaryLossApplicationResponse(**create_dependents_response.dict())

                request.dependant_id = create_dependents_response.dependent.id

                # create the extracted
                create_extracted_dependents_response = ExtractedDependentService.create_extracted_dependent(
                    create_request=request,
                    db_session=db_session
                )
                if not create_extracted_dependents_response.success:
                    return ExtractedTemporaryLossApplicationResponse(**create_extracted_dependents_response.dict())

        create_track_response = ApplicationTrackingService.create_application_tracking(
            create_request=ApplicationTrackingCreateRequest(
                application_id=saved_application_response.temporary_loss_application.id,
                stage=ApplicationStage.SUBMITTED,
                status=ApplicationStatus.PENDING,
                # user_id=user_id,
                notes=None,
                action_performed_by_id=user_id,
            ), db_session=db_session)

        if not create_track_response.success:
            return ExtractedTemporaryLossApplicationResponse(
                status_code=create_track_response.status_code, success=False, message=create_track_response.message)

        refreshed_application_response = get_extracted_temporary_loss_application(
            db_session=db_session,
            id=saved_extracted_application_response.extracted_temporary_loss_application.id)
        if not refreshed_application_response.success:
            return refreshed_application_response

        edit_document_response = DocumentService.update_document(
            db_session=db_session,
            document_id=upload_response.document.id,
            update_request=DocumentUpdate(
                temporary_loss_application_id=saved_application_response.temporary_loss_application.id
            )
        )

        if not edit_document_response.success:
            return ExtractedTemporaryLossApplicationResponse(
                success=False, status_code=edit_document_response.status_code, message=edit_document_response.message)

        return ExtractedTemporaryLossApplicationResponse(
            status_code=201, success=True,
            message="Application extracted successfully",
            extracted_temporary_loss_application=refreshed_application_response.extracted_temporary_loss_application,
            # notification=notification_response.notification if notification_response.notification else None
        )


def parse_date(date_field):
    if date_field and date_field.value_string:
        try:
            return parser.parse(date_field.value_string, dayfirst=True).date()
        except ParserError:
            print("Invalid date format")
    return None
