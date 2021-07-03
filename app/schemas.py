import datetime
from .db.database import Base
from typing import List, Optional
from pydantic import BaseModel, EmailStr, validator, ValidationError

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: str
    
    @validator('phone')
    def validate_phone(cls, v: str):
        if not v.isnumeric() or ' ' in v or len(v) != 9:
            raise ValidationError('Invalid phone number')
        return v
 
class UserIn(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    uuid: str
    
    class Config:
        orm_mode = True

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    token: str
    expires_at: datetime.datetime

class PersonalDataBase(BaseModel):
    pesel: int
    nationality: str
    country_of_birth: str
    mothers_maiden_name: str
    date_of_birth: datetime.date
    postcode: str
    city: str
    country: str
    street: str
    building_number: int
    marital_status: str
    marital_division: bool
    education: str
    financial_position: str
    household_occupants: int
    monthly_household_spendings: int
    other_burdens_spendings: int
    other_burdens_text: str
    has_business: bool
    has_closed_business: bool
    years_in_workforce: int
    is_eligible_for_early_retirement: bool

class PersonalDataIn(PersonalDataBase):
    pass

class PersonalData(PersonalDataBase):
    user_id: int

    class Config:
        orm_mode = True

class IncomeSourceBase(BaseModel):
    income_type: str
    subtype: str
    job_title: str
    employer_industry: str
    workplace_type: str
    is_paycheck_in_cash: bool
    paycheck_institution_name: str

class IncomeSourceIn(IncomeSourceBase):
    pass

class IncomeSource(IncomeSourceBase):
    user_id: int

    class Config:
        orm_mode = True

class ObligationBase(BaseModel):
    role_in_obligation: str
    obligation_type: str
    obligation_to_consolidation: bool
    obligation_bank: str
    date_of_grant: datetime.date
    to_be_paid: int
    currency: str
    amount_granted: int
    current_ammount_to_be_paid: int
    installment_rate: int
    is_secured_obligation: bool 
    is_shared_obligation: bool

class ObligationIn(ObligationBase):
    pass

class Obligation(ObligationBase):
    user_id: int

    class Config: 
        orm_mode = True

class IdentityCardBase(BaseModel):
    type: str

class IdentityCardIn(IdentityCardBase):
    pass

class IdentityCard(IdentityCardBase):
    scan_path1: str
    scan_path2: str