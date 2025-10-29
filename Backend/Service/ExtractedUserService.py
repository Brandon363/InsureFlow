from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session
from fastapi import UploadFile, File

from Entity.ExtractedUserEntity import ExtractedUserEntity
from Model.DocumentModel import DocumentResponse
from Model.ExtractedUserModel import ExtractedUserResponse, ExtractedUserCreateRequest, ExtractedUserDTO
from Model.NotificationModel import NotificationCreate
from Model.VerificationTrackingModel import VerificationTrackingCreateRequest
from Repository import ExtractedUserRepository
from Utils.Enums import EntityStatus, DocumentType, NotificationType, VerificationStatus, VerificationTrackingStage, \
    TrackingStatus
from Service import DocumentService, UserService, NotificationService, VerificationTrackingService

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentAnalysisFeature

from dotenv import load_dotenv
import os
import base64

load_dotenv()

endpoint = os.getenv("AZURE_ENDPOINT")
key = os.getenv("AZURE_KEY")

document_intelligence_client = DocumentIntelligenceClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)


def get_active_extracted_user_by_id(db_session: Session, extracted_user_id: int) -> ExtractedUserResponse:
    if extracted_user_id is None:
        return ExtractedUserResponse(status_code=400, success=False, message="Extracted user ID cannot be null")
    db_user = ExtractedUserRepository.find_active_extracted_user_by_id(db_session=db_session,
                                                                       extracted_user_id=extracted_user_id)
    if db_user is None:
        return ExtractedUserResponse(status_code=404, success=False,
                                     message=f"User with id {extracted_user_id} not found")

    return ExtractedUserResponse(status_code=200, success=True, message="User successfully found",
                                 extracted_user=db_user)


def get_active_extracted_user_by_user_id(db_session: Session, user_id: int) -> ExtractedUserResponse:
    if user_id is None:
        return ExtractedUserResponse(status_code=400, success=False, message="ID number cannot be null")

    db_user = ExtractedUserRepository.find_active_extracted_user_by_user_id(db_session=db_session, user_id=user_id)
    if db_user is None:
        return ExtractedUserResponse(status_code=404, success=False, message=f"ID {user_id} not found")

    return ExtractedUserResponse(status_code=200, success=True, message="User successfully found",
                                 extracted_user=db_user)


def get_all_active_extracted_users(db_session: Session) -> ExtractedUserResponse:
    db_users = ExtractedUserRepository.find_all_active_extracted_users(db_session=db_session)

    if db_users is None:
        return ExtractedUserResponse(status_code=404, success=False, message=f"Users not found")

    return ExtractedUserResponse(status_code=200, success=True, message="Users successfully found",
                                 extracted_users=db_users)


def create_extracted_user(db_session: Session, create_request: ExtractedUserCreateRequest) -> ExtractedUserResponse:
    # Check if ID number already exists
    existing_user_by_id = ExtractedUserRepository.find_active_extracted_user_by_user_id(db_session=db_session,
                                                                                        user_id=create_request.user_id)

    # if existing_user_by_id:
    #     return ExtractedUserResponse(status_code=400, success=False, message="User already applied")

    # Create user entity
    user_entity = ExtractedUserEntity(**create_request.dict())
    db_session.add(user_entity)
    db_session.commit()
    db_session.refresh(user_entity)

    return ExtractedUserResponse(status_code=201, success=True, message="User created successfully",
                                 extracted_user=user_entity)


def delete_extracted_user(db_session: Session, user_id: int) -> ExtractedUserResponse:
    existing_user = ExtractedUserRepository.find_active_extracted_user_by_id(db_session=db_session,
                                                                             extracted_user_id=user_id)

    if existing_user is None:
        return ExtractedUserResponse(status_code=404, success=False, message="Extracted user does not exist")

    user_to_return = ExtractedUserDTO.from_orm(existing_user)
    db_session.delete(existing_user)
    db_session.commit()

    return ExtractedUserResponse(status_code=201, success=True, message="User successfully deleted",
                                 extracted_user=user_to_return)


def parse_date(date_string):
    try:
        return datetime.strptime(date_string, "%d/%m/%Y").date()
    except ValueError:
        return None


def safe_capitalize(value: str | None) -> str | None:
    return value.capitalize() if isinstance(value, str) and value else None


async def extract_user(db_session: Session, image_file: File, user_id: int) -> ExtractedUserResponse:
    # check if user exists
    user_response = UserService.get_active_user_by_id(db_session=db_session, user_id=user_id)
    if not user_response.success:
        return ExtractedUserResponse(success=False, status_code=user_response.status_code,
                                     message=user_response.message)

    # save image to local directory
    upload_response: DocumentResponse = await DocumentService.upload_document(
        db_session=db_session,
        file=image_file,
        user_id=user_id,
        document_type=DocumentType.NATIONAL_ID)

    if not upload_response.success:
        return ExtractedUserResponse(status_code=upload_response.status_code, success=False,
                                     message=upload_response.message)

    local_image_path = Path("backend") / upload_response.document.url
    with open(local_image_path, "rb") as f:
        image_data = f.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")

    # poller = document_intelligence_client.begin_analyze_document(
    #     "prebuilt-idDocument",
    #     body={"base64Source": base64_image},
    #     features=[DocumentAnalysisFeature.QUERY_FIELDS],  # Specify which add-on capabilities to enable.
    #     query_fields=["PlaceOfBirth", "VillageOfOrigin"]
    # )

    poller = document_intelligence_client.begin_analyze_document(
        "Zimbabwe_National_ID_Extractor_v1",
        body={"base64Source": base64_image}
    )

    id_documents = poller.result()

    # user_extracted_data = ExtractedUserEntity()
    user_extracted_data = ExtractedUserCreateRequest(
        user_id=user_id
    )

    for idx, id_document in enumerate(id_documents.documents):
        print("--------Recognizing ID document #{}--------".format(idx + 1))

        first_name = id_document.fields.get("FirstName")
        if first_name:
            full_name = first_name.value_string.split()
            first_name_value = full_name[0] if len(full_name) > 0 else None
            other_names = ' '.join(full_name[1:]) if len(full_name) > 1 else None

            user_extracted_data.first_name = safe_capitalize(first_name_value)
            user_extracted_data.other_names = safe_capitalize(other_names)
            user_extracted_data.first_name_confidence = first_name.confidence
            user_extracted_data.other_names_confidence = first_name.confidence

        last_name = id_document.fields.get("LastName")
        if last_name:
            user_extracted_data.last_name = safe_capitalize(last_name.value_string)
            user_extracted_data.last_name_confidence = last_name.confidence

        document_number = id_document.fields.get("IdNumber")
        if document_number:
            user_extracted_data.id_number = document_number.value_string.replace(" ", "")
            user_extracted_data.id_number_confidence = document_number.confidence

        date_of_birth = id_document.fields.get("DateOfBirth")
        if date_of_birth:
            date_object = parse_date(date_of_birth.value_string)
            if date_object:
                user_extracted_data.date_of_birth = date_object
                user_extracted_data.date_of_birth_confidence = date_of_birth.confidence

        place_of_birth = id_document.fields.get("PlaceOfBirth")
        if place_of_birth:
            user_extracted_data.place_of_birth = safe_capitalize(place_of_birth.content)
            user_extracted_data.place_of_birth_confidence = place_of_birth.confidence

        village_of_origin = id_document.fields.get("VillageOfOrigin")
        if village_of_origin:
            user_extracted_data.village_of_origin = safe_capitalize(village_of_origin.value_string)
            user_extracted_data.village_of_origin_confidence = village_of_origin.confidence

        total_confidence = 0
        count = 0

        # Extracted fields and their confidence scores
        fields = [
            ("first_name", user_extracted_data.first_name_confidence),
            ("last_name", user_extracted_data.last_name_confidence),
            ("id_number", user_extracted_data.id_number_confidence),
            ("date_of_birth", user_extracted_data.date_of_birth_confidence),
            ("place_of_birth", user_extracted_data.place_of_birth_confidence),
            ("village_of_origin", user_extracted_data.village_of_origin_confidence),
        ]

        for field, confidence in fields:
            if confidence is not None:
                total_confidence += confidence
                count += 1

        if count > 0:
            overall_accuracy = total_confidence / count
        else:
            overall_accuracy = 0

        print(f"Overall Accuracy: {overall_accuracy:.2f}")
        user_extracted_data.overall_accuracy = overall_accuracy

        create_response = create_extracted_user(db_session=db_session, create_request=user_extracted_data)
        if not create_response.success:
            DocumentService.delete_file(upload_response.document.url)
            return ExtractedUserResponse(status_code=create_response.status_code, success=False,
                                         message=create_response.message)

        # change user verification status
        change_verification_status_response = UserService.make_user_verification_status_pending(db_session=db_session,
                                                                                                user_id=user_id)
        if not change_verification_status_response.success:
            print(change_verification_status_response.message)

        create_tracker_response = VerificationTrackingService.create_verification_tracking(
            db_session=db_session,
            create_request=VerificationTrackingCreateRequest(
                user_id=user_id,
                status=TrackingStatus.PENDING,
                stage=VerificationTrackingStage.SUBMITTED,
                notes="Your profile has been submitted for verification"
            )
        )

        if not create_tracker_response.success:
            print(create_tracker_response.message)

        create_notification_response = NotificationService.create_notification(
            create_request=NotificationCreate(
                user_id=user_id,
                notification_type=NotificationType.USER_UPDATE,
                title='Verification Submitted',
                message='Your profile has been submitted for verification'
            ),
            db_session=db_session)

        if not create_notification_response.success:
            print(create_notification_response.message)

        return ExtractedUserResponse(
            status_code=201,
            success=True, message="User successfully extracted",
            extracted_user=create_response.extracted_user,
            notification=create_notification_response.notification if create_notification_response.success else None)
