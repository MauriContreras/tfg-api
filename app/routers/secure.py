from fastapi import APIRouter, Depends
from app.security.auth import get_user
from app.database import crud
from app.models.responses.error_responses import ErrorResponses
from app.database.database import get_db

from sqlalchemy.orm import Session
from app.models import schemas



router = APIRouter()
error_responses = ErrorResponses()


@router.get("/person/{person_id}", response_model=schemas.Person)
def get_person(person_id: int, db: Session = Depends(get_db)):
    person = crud.get_person(db, person_id=person_id)
    if person is None:
        error_responses.NotFound(raise_error=True)
    return person


@router.get("/procedure/{p_concept_id}", response_model=schemas.Treatment)
def get_procedure(p_concept_id: int, db: Session = Depends(get_db)):
    procedure = crud.get_procedure(db, p_concept_id=p_concept_id)
    if procedure is None:
        return error_responses.NotFound(raise_error=True)
    response_dict = {
        "concept_id": procedure.concept_id,
        "concept_name": procedure.concept_name,
        "vocabulary_id": procedure.vocabulary_id,
        "concept_code": procedure.concept_code
    }
    return response_dict


@router.get("/condition/{c_concept_id}", response_model=schemas.Treatment)
def get_condition(c_concept_id: int, db: Session = Depends(get_db)):
    condition = crud.get_condition(db, c_concept_id=c_concept_id)
    if condition is None:
        return error_responses.NotFound(raise_error=True)
    response_dict = {
        "concept_id": condition.concept_id,
        "concept_name": condition.concept_name,
        "vocabulary_id": condition.vocabulary_id,
        "concept_code": condition.concept_code
    }
    return response_dict


@router.get("/procedures/")
def get_procedures(db: Session = Depends(get_db)):
    procedures = crud.get_procedures(db)
    if not procedures:
        return error_responses.NotFound(raise_error=True)
    return procedures


@router.get("/conditions/")
def get_conditions(db: Session = Depends(get_db)):
    conditions = crud.get_conditions(db)
    if not conditions:
        return error_responses.NotFound(raise_error=True)
    return conditions


@router.get("/conditions&procedures")
def get_conditions_and_procedures(db: Session = Depends(get_db)):
    # Retrieve conditions and procedures
    conditions_list = crud.get_conditions(db)
    procedures_list = crud.get_procedures(db)

    # Prefix keys with "condition_" and "procedure_" to avoid collisions
    conditions_prefixed = {f"condition_{i}": condition for i, condition in enumerate(conditions_list)}
    procedures_prefixed = {f"procedure_{i}": procedure for i, procedure in enumerate(procedures_list)}

    # Merge the prefixed dictionaries
    combined_dict = {**conditions_prefixed, **procedures_prefixed}

    # Sort the combined dictionary by the concept_id
    sorted_combined_dict = sorted(combined_dict.items(), key=lambda item: item[1]['concept_id'])

    # Convert the sorted_combined_dict into the desired list format
    sorted_combined_list = [{key: value} for key, value in sorted_combined_dict]

    return sorted_combined_list


@router.get("/conditons-and-procedures-ids")
def get_diagnoses_and_treatments_ids(db: Session = Depends(get_db)):
    all_diagnoses_treatments = crud.get_concept_ids(db)
    return all_diagnoses_treatments


@router.get("/patient_data/{person_id}/{start_date}/{last_date}")
def get_patient_data(person_id, start_date, last_date, db: Session = Depends(get_db)):
    return crud.get_patient_data(db, person_id=person_id, start_date=start_date, last_date=last_date)


@router.get("/people_id/")
def get_people_ids(db: Session = Depends(get_db)):
    return crud.get_people_id(db)


@router.get("/get_latest_condOrtreat_date/{person_id}/{start_date}/{end_date}")
def get_latest_condOrtreat_date(person_id, start_date, end_date, db: Session = Depends(get_db)):
    return crud.get_latest_condOrtreat_date(db, person_id=person_id, start_date=start_date, end_date=end_date)


@router.get("/images_interval/{person_id}/{years}/{interval_code}")
def images_interval(person_id, years, interval_code, db: Session = Depends(get_db)):
    return crud.image_interval(db, person_id=person_id, years=years, interval_code=interval_code)