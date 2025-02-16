# -*- coding: utf-8 -*-
"""
    LUCIA

    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @author: Mauricio Contreras Garay - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""

from fastapi import Depends, APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter

from app.database import crud
from app.models import schemas
from app.database.database import get_db
from app.models.responses.error_responses import ErrorResponses

from typing import Annotated




router = APIRouter()
error_responses = ErrorResponses()

# @ before all (o algo así)
# leer desde un csv tokens
# recuperas el token por parámetro
# si el token no está ahí,  devuelves 403, sino sigues
