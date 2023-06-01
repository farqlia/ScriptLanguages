from sqlalchemy import create_engine, select, func, text
from sqlalchemy.orm import Session
from labs.lab10.bikes_database.rents_metadata import Rental, Bike, Station
from labs.lab10.bikes_database.select_from_db import SQLSelector

if __name__ == "__main__":

    db_name = 'bike_rentals_demo.db'
    engine = create_engine(f"sqlite:///{db_name}?charset=utf8mb4")

    sql_selector = SQLSelector(db_name)

    print(sql_selector.select_all_stations())

    with Session(engine) as session:

        results = session.scalars(
             select(func.date(Rental.start_time), Rental.start_time, Station.station_name).join(Rental.rental_station)
             .where(Station.station_name == 'Rondo Reagana'))

        for result in results:
            print(result)

        subquery = session.query(
             select(func.date(Rental.start_time).label("rdate"), func.count(Rental.rental_id).label('count'))
             .join(Rental.rental_station)
             .where(Station.station_name == 'Rondo Reagana').group_by(text('rdate')).subquery("sub"))

        result3 = session.scalars(select(func.avg(text("sub_count"))).select_from(subquery)).first()

        result2 = list(session.execute(subquery))

        for result in result2:
            print(result)

        print(result3)
        print(sql_selector.compute_average_daily_rentals_from_station('Plac Legionów'))
        sql_selector.compute_number_of_bikes_parked('Plac Legionów')


        '''
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
    '''
