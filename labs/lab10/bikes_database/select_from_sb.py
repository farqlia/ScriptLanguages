from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from labs.lab10.bikes_database.rents_metadata import Rental, Bike, Station
from labs.lab10.bikes_database.select_from_db import SQLSelector

if __name__ == "__main__":

    db_name = 'bike_rentals.db'
    engine = create_engine(f"sqlite:///{db_name}?charset=utf8mb4")

    sql_selector = SQLSelector(db_name)

    print(sql_selector.select_all_stations())

    with Session(engine) as session:

        # results = session.scalars(
          #   select(Rental))

        #for result in results:

         #    print(result)

        stations = session.scalars(
            select(Station)
        )

        for station in stations:
            print(station)

        bikes = session.scalars(
            select(Bike).order_by(Bike.bike_id)
        )

        for bike in bikes:
            print(bike)

