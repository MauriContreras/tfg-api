from pydantic import BaseModel
from typing import Annotated
from fastapi import Query
from datetime import date, datetime


class PersonBase(BaseModel):
    year_of_birth: int
    gender_concept_id: int
    race_concept_id: int
    ethnicity_concept_id: int


class PersonCreate(PersonBase):
    pass


class Person(PersonBase):
    person_id: int

    def __eq__(self, other):
        return (
                isinstance(other, Person)
                and self.person_id == other.person_id
                and self.year_of_birth == other.year_of_birth
                and self.gender_concept_id == other.gender_concept_id
                and self.race_concept_id == other.race_concept_id
                and self.ethnicity_concept_id == other.ethnicity_concept_id
        )

    class Config:
        orm_mode = True


class VisitOccurrenceBase(BaseModel):
    pass


class VisitOccurrenceCreate(VisitOccurrenceBase):
    pass


class VisitOccurrence(VisitOccurrenceBase):
    pass


class ConditionOccurrenceBase(BaseModel):
    person_id: int
    condition_concept_id: int
    condition_start_date: date
    condition_start_datetime: datetime | None = None
    condition_end_date: date | None = None
    condition_end_datetime: datetime | None = None
    condition_type_concept_id: int
    condition_status_concept_id: int | None = None
    stop_reason: str | None = None
    provider_id: int | None = None
    visit_occurrence_id: int | None = None
    visit_detail_id: int | None = None
    condition_source_value: str | None = None
    condition_source_concept_id: int | None = None
    condition_status_source_value: str | None = None


class ConditionOccurrenceCreate(ConditionOccurrenceBase):
    pass


class ConditionOccurrence(ConditionOccurrenceBase):
    condition_occurrence_id: int

    class Config:
        orm_mode = True


class ProcedureOccurrenceBase(BaseModel):
    person_id: int
    procedure_concept_id: int
    procedure_date: date
    procedure_datetime: datetime | None = None
    procedure_end_date: date | None = None
    procedure_end_datetime: datetime | None = None
    procedure_type_concept_id: int
    modifier_concept_id: int | None = None
    quantity: int | None = None
    provider_id: int | None = None
    visit_occurrence_id: int | None = None
    visit_detail_id: int | None = None
    procedure_source_value: str | None = None
    procedure_source_concept_id: int | None = None
    modifier_source_value: str | None = None


class ProcedureOccurrenceCreate(ProcedureOccurrenceBase):
    pass


class ProcedureOccurrence(ProcedureOccurrenceBase):
    procedure_occurrence_id: int

    class Config:
        orm_mode = True


class ProviderBase(BaseModel):
    provider_name: str | None = None


class ProviderCreate(ProviderBase):
    pass


class Provider(ProviderBase):
    provider_id: int

    class Config:
        orm_mode = True


class DrugEraBase(BaseModel):
    person_id: int
    drug_concept_id: int
    drug_era_start_date: date
    drug_era_end_date: date
    drug_exposure_count: int | None = None
    gap_days: int | None = None


class DrugEraCreate(DrugEraBase):
    pass


class DrugEra(DrugEraBase):
    drug_era_id: int

    class Config:
        orm_mode = True


class ConditionEraBase(BaseModel):
    person_id: int
    condition_concept_id: int
    condition_era_start_date: date
    condition_era_end_date: date
    condition_occurrence_count: int | None = None


class ConditionEraCreate(ConditionEraBase):
    pass


class ConditionEra(ConditionEraBase):
    condition_era_id: int

    class Config:
        orm_mode = True


class ConceptBase(BaseModel):
    concept_id: int
    concept_name: str
    domain_id: str
    vocabulary_id: str
    concept_class_id: str
    standard_concept: str | None = None
    concept_code: str
    valid_start_date: date
    valid_end_date: date
    invalid_reason: str | None = None


class ConceptCreate(ConceptBase):
    pass


class Concept(ConceptBase):
    class Config:
        orm_mode = True


class Treatment(BaseModel):
    concept_id: int
    concept_name: str
    vocabulary_id: str
    concept_code: str


class Diagnosis(BaseModel):
    concept_id: int
    concept_name: str
    vocabulary_id: str
    concept_code: str

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str  # ✅ Includes hashed password storage
