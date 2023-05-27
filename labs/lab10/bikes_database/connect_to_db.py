from labs.lab10.bikes_database.rents_metadata import Rental, Station, Base, Bike
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime

if __name__ == "__main__":

    db_name = "bike_rentals.db"
    engine = create_engine(f"sqlite:///{db_name}", echo=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        s1 = Station(station_name='Wyspa Slodowa')
        s2 = Station(station_name='Mickiewicza')
        b1 = Bike()
        r1 = Rental(rent_bike=b1,
                    start_time=datetime(year=2023, month=6, day=29, hour=23, minute=0, second=0),
                    end_time=datetime(year=2023, month=6, day=30, hour=1, minute=0, second=0),
                    rental_station=s1, return_station=s2, durance=30)

        print(r1.rental_station)
        print(r1.return_station)

        print(s1.start_of_rentals)
        print(s2.end_of_rentals)

        session.add_all([s1, s2, b1, r1])
        session.commit()



