from labs.lab10.bikes_database.select_from_db import SQLSelector
import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy import func
import os
from labs.lab10.bikes_database.load_data import load_from_file, add_rental_data_to_db
from labs.lab10.bikes_database.rents_metadata import Rental, Station, Base, Bike

db_rows = [
    {'rental_id': 1, 'bike_number': 1,
     'start_time': '2021-01-01 13:00:00', 'end_time': '2021-01-01 14:00:00',
     'rental_station': 'Galeria Dominikanska', 'return_station': 'Mickiewicza',
     'durance': 60},
    {'rental_id': 2, 'bike_number': 2,
     'start_time': '2021-01-01 14:01:00', 'end_time': '2021-01-01 16:01:00',
     'rental_station': 'Galeria Dominikanska', 'return_station': 'Swidnicka',
     'durance': 120},
    {'rental_id': 3, 'bike_number': 2,
     'start_time': '2021-01-01 15:00:00', 'end_time': '2021-01-01 15:30:00',
     'rental_station': 'Swidnicka', 'return_station': 'Mickiewicza',
     'durance': 30},
    {'rental_id': 4, 'bike_number': 2,
     'start_time': '2021-01-03 18:00:00', 'end_time': '2021-01-03 19:00:00',
     'rental_station': 'Mickiewicza', 'return_station': 'Galeria Dominikanska',
     'durance': 60},
    {'rental_id': 5, 'bike_number': 3,
     'start_time': '2021-01-02 17:01:00', 'end_time': '2021-01-02 17:16:00',
     'rental_station': 'Swidnicka', 'return_station': 'Galeria Dominikanska',
     'durance': 15},
    {'rental_id': 6, 'bike_number': 3,
     'start_time': '2021-01-03 18:00:00', 'end_time': '2021-02-05 18:20:00',
     'rental_station': 'Mickiewicza', 'return_station': 'Swidnicka',
     'durance': 20},

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
def engine(tmp_path, db_name):
    db_name = tmp_path / "bike_rentals.db"
    engine = create_engine(f"sqlite:///{db_name}", echo=True)
    return engine


@pytest.fixture()
def instance(db_name):
    return SQLSelector(db_name)


class TestSqlSelector:

    @pytest.mark.parametrize("station,time",
                             [("Galeria Dominikanska", 90.0),
                              ('Swidnicka', 22.5),
                              ('Mickiewicza', 40.0)])
    def test_avg_rental_time_starting_at_station(self, station, time, instance):
        assert time == instance.compute_average_rental_time_starting_at_station(station)

    @pytest.mark.parametrize("station,time",
                             [("Galeria Dominikanska", 37.5),
                              ('Swidnicka', 70),
                              ('Mickiewicza', 45.0)])
    def test_avg_rental_time_ending_at_station(self, station, time, instance):
        assert time == instance.compute_average_rental_time_ending_at_station(station)

    @pytest.mark.parametrize("station,n_bikes_parked",
                             [("Galeria Dominikanska", 3),
                              ('Swidnicka', 2),
                              ('Mickiewicza', 2)])
    def test_compute_n_of_bikes_parked(self, station, n_bikes_parked, instance):
        assert n_bikes_parked == instance.compute_number_of_bikes_parked(station)

    @pytest.mark.parametrize("station,avg_rentals",
                             [("Galeria Dominikanska", 2),
                              ('Swidnicka', 1),
                              ('Mickiewicza', 2)])
    def test_compute_average_daily_rentals_from_station(self, station, avg_rentals, instance):
        assert avg_rentals == instance.compute_average_daily_rentals_from_station(station)


    def test_how_lag_works(self, engine):
        with Session(engine) as session:
            elements = session.execute(select(Rental,
                                   func.lag(Rental.start_time).over(
                                       order_by=Rental.start_time,
                                       partition_by=Rental.rental_station
                                   ).label('prev time')))

            for elem in elements:
                print(elem)
