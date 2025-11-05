from pathlib import Path

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
import numpy as np
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from fastapi import File

from dotenv import load_dotenv
import os
import base64

from Model.DocumentModel import DocumentResponse
from Model.ResponseModel import BaseResponse
from Service import DocumentService
from sqlalchemy.orm import Session

from Utils.Enums import DocumentType

load_dotenv()


class ExtractedText(BaseModel):
    text: str
    confidence: float



class ExtractedTextResponse(BaseResponse):
    text: Optional[ExtractedText] = None
    texts: Optional[List[ExtractedText]] = None
    raw_text: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


endpoint = os.getenv("AZURE_ENDPOINT")
key = os.getenv("AZURE_KEY")


# def format_bounding_box(bounding_box):
#     if not bounding_box:
#         return "N/A"
#     reshaped_bounding_box = np.array(bounding_box).reshape(-1, 2)
#     return ", ".join(["[{}, {}]".format(x, y) for x, y in reshaped_bounding_box])


async def analyze_read(image_file: File, db_session: Session):
    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    # save image to local directory
    upload_response: DocumentResponse = await DocumentService.upload_document(
        db_session=db_session,
        file=image_file,
        user_id=1,
        document_type=DocumentType.SUPPORTING_DOCUMENT)

    if not upload_response.success:
        return ExtractedTextResponse(status_code=upload_response.status_code, success=False,
                                     message=upload_response.message)

    local_image_path = Path("backend") / upload_response.document.url
    with open(local_image_path, "rb") as f:
        image_data = f.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")

    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-read", body={"base64Source": base64_image}
    )
    result = poller.result()
    print(result.content)
    extracted_text = []
    for page in result.pages:
        for word in page.words:
            extracted_text.append(ExtractedText(text=word.content, confidence=word.confidence))

    return ExtractedTextResponse(
        success=True, status_code=200, message="Text extracted successfully",
        texts=extracted_text, raw_text=result.content)
