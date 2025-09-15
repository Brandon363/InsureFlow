from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

from Config.middleware_and_cors import MyMiddleware

load_dotenv()

from starlette.middleware.cors import CORSMiddleware

app = FastAPI()


# Define Pydantic models
class AgentDetails(BaseModel):
    full_name_and_surname: str
    agent_number: str


class NextOfKinDetails(BaseModel):
    full_name_and_surname: str
    contact_number: str


class InsuredDetails(BaseModel):
    full_name_and_surname: str
    title: str
    id_number: str
    contact_number: str
    residential_address: str
    gender: str
    date_of_birth: str
    email_address: str | None
    next_of_kin_details: NextOfKinDetails


class BankDetails(BaseModel):
    bank_name: str
    account_number: str
    branch_code: str
    date_of_birth: str


class InsuranceDocument(BaseModel):
    agent_details: AgentDetails
    insured_details: InsuredDetails
    bank_details: BankDetails


# Initialize Gemini API client
client = genai.Client()


@app.post("/upload")
async def extract_insurance_info(image: UploadFile = File(...)):
    # Read image bytes
    image_bytes = await image.read()

    # Extract information using Gemini API
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type='image/jpeg',
            ),
            'Extract that information?'
        ]
    )

    # Parse extracted data
    insurance_info = response.text

    # Return extracted data
    print(insurance_info)
    return insurance_info


app.add_middleware(MyMiddleware)
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"],
                   allow_credentials=True)
