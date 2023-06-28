from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import DatabaseError
from labs.lab10.bikes_database.rents_metadata import Rental, Bike, Station, Base
from sqlalchemy import func
from sqlalchemy import over


class SQLSelector:

    def __init__(self, db_name):
        print(db_name)
        self.engine = create_engine(f"sqlite:///{db_name}?charset=utf8mb4", echo=True)

    def select_all_stations(self):
        with Session(self.engine) as session:
            stations = session.scalars(select(Station))
            return list(stations)

    def _compute_average_durance_time(self, station_name, rental_join_key):
        with Session(self.engine) as session:
            average = session.execute(select(func.avg(Rental.durance).label('average')).
                                   join(rental_join_key).
                                   where(Station.station_name == station_name))

            return round(average.first()[0], 2)

    def compute_average_rental_time_starting_at_station(self, station_name):
        return self._compute_average_durance_time(station_name, Rental.rental_station)

    def compute_average_rental_time_ending_at_station(self, station_name):
        return self._compute_average_durance_time(station_name, Rental.return_station)

    def compute_number_of_bikes_parked(self, station_name):
        with Session(self.engine) as session:
            union = session.query(select(Station.station_name, Rental.bike_number)
                                  .where(Station.station_name == station_name)
                                  .join(Rental.return_station).
                                union(select(Station.station_name, Rental.bike_number)
                                      .where(Station.station_name == station_name)
                                      .join(Rental.rental_station))
                                  .subquery())
            n_of_bikes = union.distinct().count()

            return n_of_bikes

    def compute_average_daily_rentals_from_station(self, station_name):
        with Session(self.engine) as session:
            query = session.query(select(func.date(Rental.start_time).label("rdate"),
                                         func.count(Rental.rental_id).label('count'))
                                            .where(Station.station_name == station_name)
                                            .join(Rental.rental_station)
                                            .group_by(text("rdate")).subquery("sub"))

            result = session.scalars(select(func.avg(text("sub_count")))
                                     .select_from(query)).first()

        return round(result, 2)


