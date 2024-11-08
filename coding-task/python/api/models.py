import datetime

from sqlalchemy import Integer, Numeric, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    pass