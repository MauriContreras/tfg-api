from sqlalchemy import Column, Integer, ForeignKey, Date, String, Float, DateTime, ARRAY, Boolean
# from sqlalchemy.orm import relationship

from app.database.database import Base


class Person(Base):
    __tablename__ = "person"

    person_id = Column(Integer, primary_key=True, index=True)
    year_of_birth = Column(Integer)
    gender_concept_id = Column(Integer)
    race_concept_id = Column(Integer)
    ethnicity_concept_id = Column(Integer)
    # Inexistent attributes in the data received
    '''
    month_of_birth = Column(Integer)
    day_of_birth = Column(Integer)
    birth_datetime = Column(DateTime)
    location_id = Column(Integer)
    provider_id = Column(Integer)
    care_site_id = Column(Integer)
    person_source_value = Column(String)
    gender_source_value = Column(String)
    gender_source_concept_id = Column(Integer)
    race_source_value = Column(String)
    race_source_concept_id = Column(Integer)
    ethnicity_source_value = Column(String)
    ethnicity_source_concept_id = Column(Integer)
    deceased = Column(Boolean)
    deceased_datetime = Column(Date)
    is_primary_care_provider = Column(Boolean)
    primary_care_provider_id = Column(Integer)
    visit_occurrence_id = Column(Integer)
    visit_start_date = Column(Date)
    visit_end_date = Column(Date)
    '''
    # to create the relationships...
    # visit_ocurrences = relationship("Visit_Ocurrence", back_populates="owner")
    # owner = relationship("Person", back_populates="visit_ocurrences")


# Newly generated
"""
class VisitOccurrence(Base):
    __tablename__ = "visit_occurrence"

    # Commented out attributes not used with the given data
    
    visit_occurrence_id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey('person.person_id'))
    visit_start_date = Column(Date)
    visit_end_date = Column(Date)
    visit_concept_id = Column(Integer)
    visit_type_concept_id = Column(Integer)
    visit_source_value = Column(String)
    admitting_source_concept_id = Column(Integer)
    admitting_source_value = Column(String)
    discharge_to_concept_id = Column(Integer)
    discharge_to_source_value = Column(String)
    preceding_visit_occurrence_id = Column(Integer)
"""


class ConditionOccurrence(Base):
    __tablename__ = "condition_occurrence"

    condition_occurrence_id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey('person.person_id'))
    condition_concept_id = Column(Integer)
    condition_start_date = Column(Date)
    condition_start_datetime = Column(DateTime)
    condition_end_date = Column(Date)
    condition_end_datetime = Column(DateTime)
    condition_type_concept_id = Column(Integer)
    condition_status_concept_id = Column(Integer)
    stop_reason = Column(String(length=20))
    provider_id = Column(Integer)
    visit_occurrence_id = Column(Integer)
    visit_detail_id = Column(Integer)
    condition_source_value = Column(String(length=50))
    condition_source_concept_id = Column(Integer)
    condition_status_source_value = Column(String(length=50))


class ProcedureOccurrence(Base):
    __tablename__ = "procedure_occurrence"

    procedure_occurrence_id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey('person.person_id'))
    procedure_concept_id = Column(Integer)
    procedure_date = Column(Date)
    procedure_datetime = Column(DateTime)
    procedure_end_date = Column(Date)
    procedure_end_datetime = Column(DateTime)
    procedure_type_concept_id = Column(Integer)
    modifier_concept_id = Column(Integer)
    quantity = Column(Integer)
    provider_id = Column(Integer, ForeignKey('provider.provider_id'))
    visit_occurrence_id = Column(Integer)
    visit_detail_id = Column(Integer)
    procedure_source_value = Column(String)
    procedure_source_concept_id = Column(Integer)
    modifier_source_value = Column(String)

    # concept = relationship("Concept", foreign_keys=[procedure_concept_id])


class DrugExposure(Base):
    __tablename__ = "drug_exposure"

    drug_exposure_id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey('person.person_id'))
    drug_concept_id = Column(Integer)
    drug_exposure_start_date = Column(Date)
    drug_exposure_start_datetime = Column(DateTime)
    drug_exposure_end_date = Column(Date)
    drug_exposure_end_datetime = Column(DateTime)
    verbatim_end_date = Column(Date)
    drug_type_concept_id = Column(Integer)
    stop_reason = Column(String(length=20))
    refills = Column(Integer)
    quantity = Column(Float)
    days_supply = Column(Integer)
    sig = Column(String)
    route_concept_id = Column(Integer)
    lot_number = Column(String(length=50))
    provider_id = Column(Integer, ForeignKey('provider.provider_id'))
    visit_occurrence_id = Column(Integer)
    visit_detail_id = Column(Integer)
    drug_source_value = Column(String(length=50))
    drug_source_concept_id = Column(Integer)
    route_source_value = Column(String(length=50))
    dose_unit_source_value = Column(String)


class Provider(Base):
    __tablename__ = "provider"

    provider_id = Column(Integer, primary_key=True, index=True)
    provider_name = Column(String(length=255))

    ''' Not currently in use
    npi = Column(String)
    dea = Column(String)
    specialty_concept_id = Column(Integer)
    care_site_id = Column(Integer)
    year_of_birth = Column(Integer)
    gender_concept_id = Column(Integer)
    provider_source_value = Column(String)
    specialty_source_value = Column(String)
    specialty_source_concept_id = Column(Integer)
    gender_source_value = Column(String)
    gender_source_concept_id = Column(Integer)
    '''


class DrugEra(Base):
    __tablename__ = "drug_era"

    drug_era_id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey('person.person_id'))
    drug_concept_id = Column(Integer)
    drug_era_start_date = Column(Date)
    drug_era_end_date = Column(Date)
    drug_exposure_count = Column(Integer)
    gap_days = Column(Integer)


class ConditionEra(Base):
    __tablename__ = "condition_era"

    condition_era_id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey('person.person_id'))
    condition_concept_id = Column(Integer)
    condition_era_start_date = Column(Date)
    condition_era_end_date = Column(Date)
    condition_occurrence_count = Column(Integer)


class Concept(Base):
    __tablename__ = 'concept'

    concept_id = Column(Integer, primary_key=True)
    concept_name = Column(String(length=255))
    domain_id = Column(String(length=20))
    vocabulary_id = Column(String(length=20))
    concept_class_id = Column(String(length=20))
    standard_concept = Column(String(length=1))
    concept_code = Column(String(length=50))
    valid_start_date = Column(Date)
    valid_end_date = Column(Date)
    invalid_reason = Column(String(length=1))


class VersionControl(Base):
    __tablename__ = 'version_control'

    version_control_id = Column(Integer, primary_key=True)
    version_control_name = Column(String, nullable=False)
    version_control_data = Column(ARRAY(Integer), nullable=False)
    version_control_description = Column(String, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100))
    hashed_password = Column(String(255), nullable=False)
    disabled = Column(Boolean, default=False)