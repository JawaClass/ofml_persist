from typing import Any
from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from models import generate_session
from models.ocd import OcdPropertyDB, OcdPropertyValueDB
from api_models.ocd.property import (
    OcdPropertyCreate,
    OcdPropertyFilter,
    OcdPropertyItemFilter,
    OcdPropertyItemOut,
    OcdPropertyOut,
    OcdPropertyUpdate,
    OcdPropertyWithTextOut,
)
from fastapi_filter import FilterDepends, with_prefix
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from routes import util
from sqlalchemy.orm import joinedload, selectinload


stmt_select_propertyvalue_with_text = select(OcdPropertyValueDB).options(
    selectinload(OcdPropertyValueDB.ref_text),
)
