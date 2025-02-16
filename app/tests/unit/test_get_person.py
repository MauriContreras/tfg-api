# -*- coding: utf-8 -*-
"""
    LUCIA

    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @author: Mauricio Contreras Garay - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""

# test_get_person.py
from sqlalchemy.orm import Session

import app.database.crud
from app.database import crud
from app.models import schemas, models
import unittest.mock as mock


@mock.patch('app.database.crud.get_person')
def test_get_person_with_existing_person(mock_get_person):
    expected_person = schemas.Person(person_id=1253672769, year_of_birth=1965, gender_concept_id=8507,
                                     race_concept_id=0, ethnicity_concept_id=0)
    mock_get_person.return_value = expected_person
    user = app.database.crud.get_person(1253672769)
    assert user == expected_person


@mock.patch('app.database.crud.get_person')
def test_get_person_with_existing_person(mock_get_person):
    expected_person = schemas.Person(person_id=1253672769, year_of_birth=1965, gender_concept_id=8507,
                                     race_concept_id=0, ethnicity_concept_id=0)
    mock_get_person.return_value = expected_person
    user = app.database.crud.get_person(12536727698)
    assert user == expected_person
