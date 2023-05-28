from labs.lab10.bikes_database.select_from_db import SQLSelector
import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import os
from labs.lab10.bikes_database.load_data import load_from_file, add_rental_data_to_db
from labs.lab10.bikes_database.rents_metadata import Rental, Station, Base, Bike

db_rows = [
    {'rental_id': 1, 'bike_number': 1,
     'start_time': '2021-01-01 13:00:00', 'end_time': '2021-01-01 14:00:00',
     'rental_station': 'Galeria Dominikanska', 'return_station': 'Mickiewicza',
     'durance': 60},
    {'rental_id': 2, 'bike_number': 2,
     'start_time': '2021-02-01 12:00:00', 'end_time': '2021-02-01 14:00:00',
     'rental_station': 'Galeria Dominikanska', 'return_station': 'Swidnicka',
     'durance': 120},
    {'rental_id': 3, 'bike_number': 2,
     'start_time': '2021-03-01 12:00:00', 'end_time': '2021-03-01 12:30:00',
     'rental_station': 'Swidnicka', 'return_station': 'Mickiewicza',
     'durance': 30},
    {'rental_id': 4, 'bike_number': 2,
     'start_time': '2021-01-01 13:00:00', 'end_time': '2021-01-01 14:00:00',
     'rental_station': 'Mickiewicza', 'return_station': 'Galeria Dominikanska',
     'durance': 60},

]


@pytest.fixture()
def db_name(tmp_path):
    db_name = tmp_path / "bike_rentals.db"
    engine = create_engine(f"sqlite:///{db_name}", echo=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        for row in db_rows:
            add_rental_data_to_db(row, session)

    return db_name

@pytest.fixture()
def instance(db_name):
    return SQLSelector(db_name)


class TestSqlSelector:

    def test_avg_rental_time_starting_at_station(self, instance):
        _sum = instance.compute_average_rental_time_starting_at_station("Galeria Dominikanska")
        assert _sum == 90.0

    def test_avg_rental_time_ending_at_station(self, instance):
        _sum = instance.compute_average_rental_time_ending_at_station("Mickiewicza")
        assert _sum == 45.0

    def test_compute_n_of_bikes_parked(self, instance):
        n_bikes = instance.compute_number_of_bikes_parked("Galeria Dominikanska")
        print(n_bikes)
        # for row in n_bikes:
          #   print(row)