# -*- coding: utf-8 -*-
"""
    LUCIA

    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @author: Mauricio Contreras Garay - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""

# crud.py

from sqlalchemy.orm import Session, aliased
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.exc import DataError
import os
import pandas as pd

from app.models.responses.error_responses import ErrorResponses
from app.models import models
from app.models.responses import error_responses

error_responses = ErrorResponses()


def get_person(db: Session, person_id: int):
    return db.query(models.Person).filter(models.Person.person_id == person_id).first()


def get_procedure(db: Session, p_concept_id: int):
    return db.query(models.Concept).filter(models.Concept.concept_id == p_concept_id).first()


def get_condition(db: Session, c_concept_id: int):
    return db.query(models.Concept).filter(models.Concept.concept_id == c_concept_id).first()


def get_procedures(db: Session):
    try:
        po = aliased(models.ProcedureOccurrence)
        concepts_with_counts = db.query(
            models.Concept.concept_id,
            models.Concept.concept_name,
            models.Concept.vocabulary_id,
            models.Concept.concept_code,
            func.count().label('occurrences')  # Count occurrences
        ).join(
            po, models.Concept.concept_id == po.procedure_concept_id
        ).group_by(
            models.Concept.concept_id,
            models.Concept.concept_name,
            models.Concept.vocabulary_id,
            models.Concept.concept_code
        ).all()
        concepts_list = create_concept_dictionary(concepts_with_counts)
        return concepts_list
    except Exception as e:
        print(f"Error in get_procedures: {e}")
        raise ValueError("Error occurred while fetching treatments")


def get_conditions(db: Session):
    try:
        po = aliased(models.ConditionOccurrence)
        concepts_with_counts = db.query(
            models.Concept.concept_id,
            models.Concept.concept_name,
            models.Concept.vocabulary_id,
            models.Concept.concept_code,
            func.count().label('occurrences')  # Count occurrences
        ).join(
            po, models.Concept.concept_id == po.condition_concept_id
        ).group_by(
            models.Concept.concept_id,
            models.Concept.concept_name,
            models.Concept.vocabulary_id,
            models.Concept.concept_code
        ).all()

        concepts_list = create_concept_dictionary(concepts_with_counts)
        return concepts_list
    except Exception as e:
        print(f"Error in get_treatments: {e}")
        raise ValueError("Error occurred while fetching treatments")


def create_concept_dictionary(concepts):
    concept_list = []
    for idx, concept in enumerate(concepts):
        concept_list.append({
            "concept_id": concept.concept_id,
            "concept_name": concept.concept_name,
            "vocabulary_id": concept.vocabulary_id,
            "concept_code": concept.concept_code,
            "occurrences": concept.occurrences
        })
    return concept_list


def get_patient_data(db: Session, person_id: int, start_date, last_date):
    try:
        patient_data = []

        print(type(person_id), type(start_date), type(last_date))
        print(person_id, start_date, last_date)
        if start_date and last_date:
            procedures = db.query(models.ProcedureOccurrence).filter(
                models.ProcedureOccurrence.person_id == person_id,
                models.ProcedureOccurrence.procedure_date >= start_date,
                models.ProcedureOccurrence.procedure_end_date <= last_date
            ).all()
            conditions = db.query(models.ConditionOccurrence).filter(
                models.ConditionOccurrence.person_id == person_id,
                models.ConditionOccurrence.condition_start_date >= start_date,
                models.ConditionOccurrence.condition_end_date <= last_date
            ).all()
        else:
            procedures = db.query(models.ProcedureOccurrence).filter(
                models.ProcedureOccurrence.person_id == person_id).all()
            conditions = db.query(models.ConditionOccurrence).filter(
                models.ConditionOccurrence.person_id == person_id).all()

        for proc in procedures:
            # Check if the entry already exists in patient_data
            if not any(entry['concept_id'] == proc.procedure_concept_id and
                       entry['start_date'] == proc.procedure_date and
                       entry['end_date'] == proc.procedure_end_date for entry in patient_data):
                # If not, append the entry to patient_data
                patient_data.append({
                    'concept_id': proc.procedure_concept_id,
                    'start_date': proc.procedure_date,
                    'end_date': proc.procedure_end_date,
                    'type': 'treatment'  # Assuming 7 represents a procedure
                })

        for cond in conditions:
            patient_data.append({
                'concept_id': cond.condition_concept_id,
                'start_date': cond.condition_start_date,
                'end_date': cond.condition_end_date,
                'type': 'diagnosis'  # Assuming 8 represents a condition
            })

        return patient_data
    except DataError as e:
        error_msg = "Invalid date format or value"
        return error_responses.ValueError(raise_error=True,
                                          description="Doesnt fulfill specified format")


"""
def get_diagnoses_and_treatments_ids(db):
    try:
        # Retrieve distinct concept IDs from condition_occurrence
        condition_concept_ids = db.query(models.ConditionOccurrence.condition_concept_id) \
            .distinct() \
            .order_by(models.ConditionOccurrence.condition_concept_id) \
            .all()
        # Retrieve distinct concept IDs from procedure_occurrence
        procedure_concept_ids = db.query(models.ProcedureOccurrence.procedure_concept_id) \
            .distinct() \
            .order_by(models.ProcedureOccurrence.procedure_concept_id) \
            .all()

        # Merge condition and procedure concept IDs into a single structure
        concept_ids = [item[0] for item in condition_concept_ids]
        concept_ids.extend(item[0] for item in procedure_concept_ids)

        return concept_ids

    except Exception as e:
        print(f"Error in get_condition_and_procedure_concept_ids: {e}")
        raise ValueError("Error occurred while fetching concept IDs")
"""


def get_people_id(db):
    return [person.person_id for person in db.query(models.Person).all()]


def get_latest_condOrtreat_date(db, person_id, start_date, end_date):
    # If the start_date and end_date are provided, the data retrieved is limited to a date range
    if start_date and end_date:
        patient_data = get_patient_data(db, person_id, start_date, end_date)
    else:
        patient_data = get_patient_data(db, person_id, None, None)

    latest_date = None
    earliest_date = None
    final_date = None
    for patient in patient_data:
        start_date = patient['start_date']
        # Might create conflict
        end_date = patient['end_date']
        if latest_date is None or start_date > latest_date:
            latest_date = start_date
        if earliest_date is None or start_date < earliest_date:
            earliest_date = start_date
        if final_date is None or end_date > final_date:
            final_date = end_date

    dates = {
        'earliest_start_date': earliest_date,
        'latest_start_date': latest_date,
        'latest_end_date': final_date
    }
    return dates


def get_additional_info(db, person_id):
    result = db.query(models.Person.year_of_birth).filter(models.Person.person_id == person_id).first()
    return result[0]


def load_all_descendants_ints():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'app/all_descendants.txt')
    with open(file_path, 'r') as f:
        all_descendants_ints = [int(x) for x in f.read().strip('[]').split(',')]
    return all_descendants_ints


def check_has_cancer(patient_data):
    all_descendants_ints = load_all_descendants_ints()

    has_cancer = 0
    for index, patient in patient_data.iterrows():
        concept_id = patient['concept_id']
        # print(concept_id)
        if concept_id in all_descendants_ints:
            has_cancer = 1
    return has_cancer


def substract_years(date, years, interval_code):
    date = datetime.combine(date, datetime.min.time())
    end_year = date.year - years
    end_date = date.replace(year=end_year)
    match interval_code:
        case 'd':
            interval = (date - end_date).days
        case 'w':
            interval = (date - end_date).days // 7
        case 'm':
            interval = (date - end_date).days // 30
        case '3m':
            interval = (date - end_date).days // 90
        case '6m':
            interval = (date - end_date).days // 180
    return interval


def get_concept_ids(db: Session):
    try:
        # Retrieve the version_control_data column from version_control table
        concept_ids = (
            db.query(models.VersionControl.version_control_data)
            .filter(models.VersionControl.version_control_name == 'default')
            .scalar()  # Use scalar() to get a single value directly
        )

        # Check if concept_ids is not None
        if concept_ids is not None:
            return concept_ids
        else:
            print("Error: No data found in version_control table with name 'default'")
            return None
    except Exception as e:
        print("Error retrieving concept_ids:", e)
        return None


def fill_matrix_with_interval(matrix, concept_ids, patient_data, start_date_aux, interval_days):
    # Convert start_date_aux to datetime if it's not already
    start_date_aux = pd.to_datetime(start_date_aux)

    # Initialize an empty dictionary to store counts for each concept and interval
    concept_interval_counts = {}

    # Initialize an empty set to keep track of processed dates
    processed_dates = set()

    # Iterate over each row in patient_data
    for _, row in patient_data.iterrows():
        # Convert start and end dates to datetime
        start_date = pd.to_datetime(row['start_date'])
        end_date = pd.to_datetime(row['end_date'])

        # Calculate the number of days between start_date_aux and start_date
        days_offset = (start_date - start_date_aux).days

        # Calculate the number of days between start_date and end_date
        days_duration = (end_date - start_date).days

        # Generate interval indices for each day between start_date and end_date
        for day_offset in range(days_duration + 1):
            current_date = start_date + timedelta(days=day_offset)
            interval_index = (days_offset + day_offset) // interval_days

            # Get the concept ID
            concept_id = row['concept_id']

            # Check if the current date has already been processed for the same interval index
            if (concept_id, interval_index, current_date) not in processed_dates:
                # Update the concept_interval_counts dictionary
                if (concept_id, interval_index) in concept_interval_counts:
                    concept_interval_counts[(concept_id, interval_index)] += 1
                else:
                    concept_interval_counts[(concept_id, interval_index)] = 1

                # Add the current date to the processed dates set
                processed_dates.add((concept_id, interval_index, current_date))

    # Update the matrix with counts for each relevant concept ID and interval
    for (concept_id, interval_index), count in concept_interval_counts.items():
        matrix.loc[concept_id, interval_index] = count

    return matrix


def get_interval_int(interval_code):
    match interval_code:
        case 'd':
            return_value = 1
        case 'w':
            return_value = 7
        case 'm':
            return_value = 30
        case '3m':
            return_value = 90
        case '6m':
            return_value = 180
        case _:
            error_responses.BadRequest("Invalid interval code")
    return return_value


def fill_matrix_all(matrix, concept_ids, patient_data, start_date_aux, interval_code):
    if interval_code in ['d', 'w', 'm', '3m', '6m']:
        interval_int = get_interval_int(interval_code)
        return fill_matrix_with_interval(matrix, concept_ids, patient_data, start_date_aux, interval_int)
    else:
        raise ValueError("Invalid granularity. Supported values are 'd', 'w', 'm', '3m', and '6m'.")


def image_interval(db, person_id, years, interval_code):
    # get the indexes of the rows
    # previous version: concept_ids = get_diagnoses_and_treatments_ids(db)
    concept_ids = get_concept_ids(db)

    # we want to know which treatment/diagnosis was the last a patient received
    dates = get_latest_condOrtreat_date(db, person_id, None, None)

    end_date = dates['latest_start_date']
    start_date = dates['earliest_start_date']
    last_date = dates['latest_end_date']
    print(dates['earliest_start_date'], dates['latest_start_date'], dates['latest_end_date'])

    # required_interval determine the row indexes of a person's image
    # This new method will now behave with a modular approach:
    # required_interval represents the amount of units necessary for the columns respective of the years
    # if interval_code = 'd', and years=4, then required_interval is 1462
    # if interval_code = 'w', and years=4, then required_interval is 209
    # and so on
    required_interval = substract_years(dates['latest_end_date'], int(years), interval_code) + 1
    print(f"required interval in {interval_code}: {required_interval}")

    # required_days is used to get the new starting day
    required_days = substract_years(dates['latest_end_date'], int(years), 'd') + 1
    print(f"required interval in days: {required_days}")
    # creates the 2d image of a person taking into account the unique concept_ids as row indexes and the days as
    # column indexes.
    matrix = pd.DataFrame(0, index=concept_ids, columns=range(required_interval))
    ##------------------------------------------------------------------------------------------------------
    # get the new start date based on the time interval defined by the user
    # this date represents the index 0 of the columns but in a matrix
    # constricted by the years passed by the user
    # new_start_date = - timedelta(days=(required_weeks * 7 - 1))
    # print(new_start_date)
    new_start_date = dates['latest_end_date'] - timedelta(days=(required_days - 1))
    print(new_start_date)

    # dates_2 represents the same as above, but this time restricted to a time interval
    # of x years, where x is a int, defined by the user
    # get_latest_condOrtreat_date_2 differs from get_latest_condOrtreat_date in
    # the fact that, the latter gets all data from a patient without restrictions, while
    # the former does with a set start and end date.
    dates_2 = get_latest_condOrtreat_date(db, person_id, new_start_date, dates['latest_end_date'])
    print(f"new dates: {dates_2['earliest_start_date']}, {dates_2['latest_start_date']}, {dates_2['latest_end_date']}")

    # patient_data is now patient date restricted to a time interval of:
    # the start_date of the last diagnosis/treatment of a patient and x years backwards,
    # where x is an int representing the years within a period where the user wants
    # to retrieve data from
    # dates_2[0] is chosen as start date because the previous method will return the dates for the oldest
    # diagnosis/treatment in the defined time interval, it could also be used new_start_date, but as we now that
    # there is no data of interest before that dates_2, makes no sense to retrieve it
    # using dates[1][1] or dates_2[1][1] shouldn't make any difference at all, as the ending date or the latest
    # condition or treatment will always be the same
    patient_data = get_patient_data(db, person_id, dates_2['earliest_start_date'], dates['latest_end_date'])
    patient_data_df = pd.DataFrame(patient_data)

    # filled_matrix is the 2d image of a patient in a fixed time interval
    # filled_matrix = fill_matrix_week(matrix, concept_ids, patient_data_df, new_start_date)
    filled_matrix = fill_matrix_all(matrix, concept_ids, patient_data_df, new_start_date, interval_code)

    # get the birth_date, and bmi, if they exist
    extra_data = get_additional_info(db, person_id)

    # check if the pacient has suffered cancer in a time interval
    cancer_result = check_has_cancer(patient_data_df)

    # structure of the data has to be returned
    # In the first batch of data nothing about weight or height is mentioned so it is
    # set to None
    full_image = {
        'indexes': concept_ids,
        'data': filled_matrix.values.tolist(),
        'birth_date': extra_data,
        'last_diagnosis_date': dates['latest_start_date'],
        'bmi': None,
        'lung_cancer': cancer_result
    }

    return full_image
