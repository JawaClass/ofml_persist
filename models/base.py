from sqlalchemy.orm import DeclarativeBase
from models.deepcopy_row import BaseDeepCopyMixin


class SqlAlchemyBase(DeclarativeBase, BaseDeepCopyMixin):

    def __str__(self) -> str:
        package = self.__class__.__module__
        class_ = self.__class__.__name__
        attrs = ((k, getattr(self, k)) for k in self.__mapper__.columns.keys())
        sattrs = ", ".join(f"{key}={value!r}" for key, value in attrs)
        return f"{package}.{class_}({sattrs})"

    def __repr__(self) -> str:
        return str(self)

    def to_dict222(self):
        import json
        items = self.__dict__.items()
        d =  {k: v for k, v in items if not k.startswith("_")}
        print("to_dict...", d)
        return d

def get_orm_class(table_name: str):
    """Finds the ORM class dynamically by table name."""
    for cls in SqlAlchemyBase.registry.mappers:
        if cls.class_.__table__.name == table_name:
            return cls.class_
    return None  # Return None if no ORM class found