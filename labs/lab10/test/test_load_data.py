import csv

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import os
from labs.lab10.bikes_database.rents_metadata import Rental, Station, Base, Bike
from datetime import datetime
from labs.lab10.bikes_database.load_data import get_object_and_create_if_not_exist, \
    add_rental_data_to_db, validate, load_from_file

# Session.begin() can only handle one transaction


@pytest.fixture()
def engine(tmp_path):
    db_name = tmp_path / "bike_rentals.db"
    engine = create_engine(f"sqlite:///{db_name}", echo=True)
    Base.metadata.create_all(engine)

    with Session(engine) as s:
        s1 = Station(station_name='Wyspa Slodowa')
        s2 = Station(station_name='Mickiewicza')
        b1 = Bike(bike_id=3)
        r1 = Rental(rental_id=1, rent_bike=b1,
                    start_time=datetime(year=2023, month=6, day=29, hour=23, minute=0, second=0),
                    end_time=datetime(year=2023, month=6, day=30, hour=1, minute=0, second=0),
                    rental_station=s1, return_station=s2, durance=20)
        s.add_all([s1, s2, b1, r1])
        s1 = Station(station_name='Galeria Dominikanska')
        s2 = Station(station_name='Swidnicka')
        b1 = Bike(bike_id=1)
        r1 = Rental(rental_id=99, rent_bike=b1,
                    start_time=datetime(year=2023, month=7, day=29, hour=13, minute=0, second=0),
                    end_time=datetime(year=2023, month=7, day=29, hour=14, minute=0, second=0),
                    rental_station=s1, return_station=s2, durance=10)
        s.add_all([s1, s2, b1, r1])
        s.commit()

    return engine

    # os.remove(db_name)

@pytest.fixture()
def row():
    return {'rental_id': 111744877, 'bike_number': 1,
     'start_time': '2021-01-31 23:49:56', 'end_time': '2021-02-01 00:11:06',
     'rental_station': 'Galeria Dominikanska', 'return_station': 'Mickiewicza',
     'durance': 22}


class TestGetObjectAndCreateIfNotExist:

    def test_should_create_new_station(self, engine):
        station_row = {"station_name": "Wroclavia"}
        with Session(engine) as session:
            station = get_object_and_create_if_not_exist(station_row, Station, "station_name", session)
            assert station.station_name == "Wroclavia"
            assert station.station_id == 5
            # assert session.get(Station, 5) == station

    def test_should_create_new_bike(self, engine):
        bike_row = {"bike_id": 4}
        with Session(engine) as session:
            bike = get_object_and_create_if_not_exist(bike_row, Bike, "bike_id", session)
            assert bike.bike_id == 4

    def test_should_return_station(self, engine):
        station_row = {"station_name": "Galeria Dominikanska"}
        with Session(engine) as session:
            station = get_object_and_create_if_not_exist(station_row, Station, "station_name", session)
            assert station.station_name == "Galeria Dominikanska"
            assert station.station_id == 3


# add_rental_data_to_db
class TestRentalDataToDb:

    def test_should_add_rental_to_db(self, engine, row):
        with Session(engine) as session:
            add_rental_data_to_db(row, session)
            rental = session.scalars(select(Rental).
                            where(Rental.rental_id == 111744877)).first()
            bike = session.scalars(select(Bike).
                            where(Bike.bike_id == 1)).first()
            rental_station = session.scalars(select(Station).
                                   where(Station.station_id == 3)).first()
            assert rental.rent_bike == bike
            assert rental.rental_id == 111744877
            assert rental.rental_station == rental_station


class TestValidate:

    def test_for_valid_row(self, row):
        assert validate(row)

    def test_for_invalid_row_missing_data(self):
        instance = {'rental_id': '111744877', 'bike_number': '1',
            'start_time': '2021-01-31 23:49:56', 'end_time': '2021-02-01 00:11:06',
            'rental_station': None, 'return_station': 'Mickiewicza',
            'durance': '22'}
        assert not validate(instance)

    @pytest.mark.parametrize("instance", [
        {'rental_id': '-1', 'bike_number': '1',
         'start_time': '2021-01-31 23:49:56', 'end_time': '2021-02-01 00:11:06',
         'rental_station': 'Galeria Dominikanska', 'return_station': 'Mickiewicza',
         'durance': '22'},
        {'rental_id': '111744877', 'bike_number': '1',
         'start_time': '2021/01/31 23:49:56', 'end_time': '2021-02-01 00:11:06',
         'rental_station': 'Galeria Dominikanska', 'return_station': 'Mickiewicza',
         'durance': '22'},
        {'rental_id': '111744877', 'bike_number': '1.1243',
         'start_time': '2021-01-31 23:49:56', 'end_time': '2021-02-01 00:11:06',
         'rental_station': 'Galeria Dominikanska', 'return_station': 'Mickiewicza',
         'durance': '22'}
    ])
    def test_for_invalid_datatype(self, instance):
        assert not validate(instance)


def test_encoding():
    filepath = r"C:\Users\julia\PycharmProjects\ScriptLanguages\labs\lab10\data\test_data.csv"
    with open(filepath, encoding='utf-8') as f:
        fieldnames = ['rental_id', 'bike_number', 'start_time', 'end_time', 'rental_station',
                      'return_station', 'durance']
        dict_reader = csv.DictReader(f, fieldnames=fieldnames)
        next(dict_reader)  # skip header
        for row in dict_reader:
            print(row['rental_station'], row['return_station'])