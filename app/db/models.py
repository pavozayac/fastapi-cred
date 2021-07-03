from pydantic.errors import ColorError
from sqlalchemy.sql.elements import collate
from sqlalchemy.sql.operators import ColumnOperators
from sqlalchemy.sql.traversals import COMPARE_FAILED
from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import backref, relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=True)
    uuid = Column(String, unique=True)

    #personal_data = relationship('PersonalData', back_populates='user')
    income_sources = relationship('IncomeSource', back_populates='user')
    obligations = relationship('Obligation', back_populates='user')
    identity_card = relationship('IdentityCard', back_populates='user')

class PersonalData(Base):
    __tablename__ = 'personals'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship('User', backref=backref('personal_data', uselist=False))

    pesel = Column(Integer)
    nationality = Column(String)
    country_of_birth = Column(String)
    mothers_maiden_name = Column(String)
    date_of_birth = Column(Date)

    postcode = Column(String)
    city = Column(String)
    country = Column(String)
    street = Column(String)
    building_number = Column(Integer)
    marital_status = Column(String)
    marital_division = Column(Boolean)
    education = Column(String)
    financial_position = Column(String)
    household_occupants = Column(Integer)
    monthly_household_spendings = Column(Integer)
    other_burdens_spendings = Column(Integer)
    other_burdens_text = Column(String)

    has_business = Column(Boolean)
    has_closed_business = Column(Boolean)

    years_in_workforce = Column(Integer)
    is_eligible_for_early_retirement = Column(Boolean)


class IncomeSource(Base):
    __tablename__ = 'income_sources'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship('User', back_populates='income_sources')

    income_type = Column(String)
    subtype = Column(String, nullable=True)
    job_title = Column(String)
    employer_industry = Column(String)
    workplace_type = Column(String)
    is_paycheck_in_cash = Column(Boolean)
    paycheck_institution_name = Column(String)
    
class Obligation(Base):
    __tablename__ = 'obligations'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship('User', back_populates='obligations')

    role_in_obligation = Column(String)
    obligation_type = Column(String)
    obligation_to_consolidation = Column(Boolean)
    obligation_bank = Column(String)
    date_of_grant = Column(Date)
    to_be_paid = Column(Integer)
    currency = Column(String)
    amount_granted = Column(Integer)
    current_ammount_to_be_paid = Column(Integer)
    installment_rate = Column(Integer)
    is_secured_obligation = Column(Boolean)
    is_shared_obligation = Column(Boolean)

class IdentityCard(Base):
    __tablename__ = 'cards'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship('User', back_populates='identity_card')

    type = Column(String)
    scan_path1 = Column(String)
    scan_path2 = Column(String)


    