from datetime import date
from google import genai
from google.genai import types

from pydantic import BaseModel, Field

from dotenv import load_dotenv
load_dotenv()

client = genai.Client()


class ZimbabweNationalRegistrationCard(BaseModel):
    id_number: str
    surname: str
    first_name: str
    date_of_birth: date
    village_of_origin: str | None
    place_of_birth: str
    date_of_issue: date

    class Config:
        json_encoders = {
            date: lambda v: v.strftime('%d/%m/%Y')
        }


from pydantic import BaseModel
from datetime import date
from typing import Optional

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
    date_of_birth: date
    email_address: Optional[str]
    next_of_kin_details: NextOfKinDetails

class BankDetails(BaseModel):
    bank_name: str
    account_number: str
    branch_code: str
    date_of_birth: date  # seems unusual here, but as per image

class InsuranceDocument(BaseModel):
    agent_details: AgentDetails
    insured_details: InsuredDetails
    bank_details: BankDetails

    class Config:
        json_encoders = {
            date: lambda v: v.strftime('%d-%m-%Y')
        }

with open('images/form1.jpg', 'rb') as f:
    image_bytes = f.read()

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        types.Part.from_bytes(
            data=image_bytes,
            mime_type='image/jpeg',
        ),
        'Extract that information?'
    ],
    config={
        "response_mime_type": "application/json",
        "response_schema": InsuranceDocument,
    },
)

# print(response.text)
card_info = response.parsed
print(card_info.model_dump_json(indent=4))
