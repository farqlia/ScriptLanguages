# model relacyjny to tabele
# Data Definition Language:
# CREATE, ALTER, DROP TABLE
# Data Manipulation Language:
# SELECT, INSERT, UPDATE, DELETE (CRUD)
# więzy integralności

'''
ORM - Object Relational Mapping - odwzorowywanie kodu tworzonego
w paradygmacie obiektowym do relacyjnych baz danych
'''
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Float
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import create_engine


class Base(DeclarativeBase):
    pass


class Pig(Base):
    __tablename__ = "pigs"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    weight: Mapped[float] = mapped_column(Float(30))
    food_id: Mapped[Optional[int]] = mapped_column(ForeignKey("food.id"))
    food: Mapped["Food"] = relationship(back_populates="pigs")

    def __repr__(self) -> str:
        return f"Pig(id={self.id!r}, name={self.name!r}, weight={self.weight!r})"


class Food(Base):
    __tablename__ = "food"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    pigs: Mapped[List["Pig"]] = relationship(back_populates="food")

    def __repr__(self) -> str:
        return f"Food(id={self.id!r}, name={self.name!r})"


if __name__ == "__main__":

    db_name = "pigs.db"
    # This operation returns Engine object, which will lazily try
    # to connect to database with the first time it is asked to do
    # something against the db
    # echo will print to the console
    engine = create_engine(f"sqlite:///{db_name}", echo=True)
    print(Base.metadata.create_all(engine))

    with Session(engine) as session:
        potato = Food(name="potato")
        chrumcia = Pig(name="Chrumcia", weight=80.0, food=potato)
        snowbull = Pig(name="Snowbull", weight=9001.0, food=None)

        print("Print ids")
        print(chrumcia.food_id)
        print(snowbull.food_id)
        print(potato.pigs)

        session.add_all([chrumcia, snowbull])
        session.commit()
    # Engine object provides Connection object
    # text() can be used to write SQL statements

    # Connection is the best used with context manager
    # Result object is the result returned by making some db operations
    # however, it shouldn't be passed around outside the scope of the
    # context manager
    # If you perform some operations, you should explicitly commit them

