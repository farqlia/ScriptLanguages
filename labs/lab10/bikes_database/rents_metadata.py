from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped, Session
from sqlalchemy import Integer, DateTime, String, ForeignKey
from datetime import datetime
from typing import Optional
from typing import List

# What are relationship():
#   https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#persisting-and-loading-relationships
# This is the central configuration object
# Other classes will subclass this one
# This form is called 'Declarative Table Configuration'
# Rental N - 1 Rental Station
# Rental N - 1 Return Station

# This class contains a metadata object which stores all Tables


class Base(DeclarativeBase):
    pass


class Rental(Base):
    # Each class has its associated Table created
    __tablename__ = 'rentals'

    rental_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    bike_number: Mapped[int] = mapped_column(ForeignKey('bikes.bike_id'))
    start_time: Mapped[datetime] = mapped_column(DateTime())
    end_time: Mapped[datetime] = mapped_column(DateTime())
    durance: Mapped[int] = mapped_column(Integer())

    rental_station_id: Mapped[int] = mapped_column(ForeignKey('stations.station_id'))
    return_station_id: Mapped[int] = mapped_column(ForeignKey('stations.station_id'))

    rental_station: Mapped['Station'] = relationship(foreign_keys=[rental_station_id],
                                                     back_populates='start_of_rentals')
    return_station: Mapped['Station'] = relationship(foreign_keys=[return_station_id],
                                                     back_populates='end_of_rentals')

    rent_bike: Mapped['Bike'] = relationship(back_populates='bike_rentals')

    def __repr__(self):
        return f"Rental(rental_id={self.rental_id!r}, bike_number={self.bike_number!r}, " \
               f"start_time={self.start_time!r}, end_time={self.end_time!r}, " \
               f"rental_station={self.rental_station!r}, return_station={self.return_station!r})"


class Bike(Base):

    __tablename__ = 'bikes'

    bike_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)

    bike_rentals: Mapped[List['Rental']] = relationship(back_populates='rent_bike')

    def __repr__(self):
        return f"Bike(bike_id={self.bike_id!r})"


class Station(Base):
    __tablename__ = 'stations'

    station_id: Mapped[int] = mapped_column(primary_key=True)
    station_name: Mapped[str] = mapped_column(String(30), unique=True)

    start_of_rentals: Mapped[List['Rental']] = relationship(back_populates='rental_station',
                                                           foreign_keys="[Rental.rental_station_id]")
    end_of_rentals: Mapped[List['Rental']] = relationship(back_populates='return_station',
                                                           foreign_keys="[Rental.return_station_id]")

    def __repr__(self):
        return f"Station(station_id={self.station_id!r}, station_name={self.station_name!r})"