import sys
from pathlib import Path
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine
from labs.lab10.bikes_database.rents_metadata import Bike, Rental, Station, Base
import csv
from sqlalchemy import select
from functools import partial
from datetime import datetime

# 2021-01-31 23:49:56
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_object_and_create_if_not_exist(object_row, object_type, key_column, session):
    obj = session.scalars(select(object_type).
                              where(getattr(object_type, key_column) == object_row[key_column])).first()
    if not obj:
        obj = object_type(**object_row)
        session.add(obj)
        session.commit()

    return obj


def get_or_add_bike(object_row, session):
    return get_object_and_create_if_not_exist(object_row=object_row, object_type=Bike, key_column='bike_id',
                                              session=session)


def get_or_add_station(object_row, session):
    return get_object_and_create_if_not_exist(object_row=object_row, object_type=Station, key_column='station_name',
                                              session=session)


def add_rental_data_to_db(row, session):
    bike = get_or_add_bike({'bike_id': row['bike_number']}, session)
    rental_station = get_or_add_station({'station_name': row['rental_station']}, session)
    return_station = get_or_add_station({'station_name': row['return_station']}, session)

    rental = Rental(rental_id=row['rental_id'], rent_bike=bike,
                    start_time=datetime.strptime(row['start_time'], DATE_FORMAT),
                    end_time=datetime.strptime(row['end_time'], DATE_FORMAT),
                    rental_station=rental_station, return_station=return_station,
                    durance=row['durance'])

    session.add(rental)
    session.commit()


if __name__ == "__main__":

    sys.argv.append(r'C:\Users\julia\PycharmProjects\ScriptLanguages\labs\lab10\data\historia_przejazdow_2021-01.csv')
    sys.argv.append('bike_rentals.db')

    if len(sys.argv) >= 3:
        filepath = Path(sys.argv[1])
        db_name = sys.argv[2]
    else:
        raise ValueError("Provide both file name and database name")

    if not filepath.exists():
        raise FileNotFoundError("File couldn't be found")

    with open(filepath) as f:
        engine = create_engine(f"sqlite:///{db_name}", echo=True)

        fieldnames = ['rental_id', 'bike_number', 'start_time', 'end_time', 'rental_station',
                      'return_station', 'durance']
        dict_reader = csv.DictReader(f, fieldnames=fieldnames)
        next(dict_reader)       # skip header row
        for row in dict_reader:
            pass





