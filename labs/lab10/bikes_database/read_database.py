from labs.lab10.bikes_database.rents_metadata import Rental, Station, Base, Bike
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime

if __name__ == "__main__":

    db_name = "bike_rentals.db"
    engine = create_engine(f"sqlite:///{db_name}", echo=True)

    with Session(engine) as session:
        print(session.get(Rental, 1))
        print(session.get(Rental, 3))

        if session.get(Rental, 3) is None:
            rental = Rental(rental_id=1, rent_bike=session.get(Bike, 1),
                            start_time=datetime(year=2023, month=6, day=29, hour=23, minute=0, second=0),
                            end_time=datetime(year=2023, month=6, day=30, hour=1, minute=0, second=0),
                            rental_station=session.get(Station, 1), return_station=session.get(Station, 3))

        session.add(rental)
        # session.commit()

        print(session.get(Rental, 3))

