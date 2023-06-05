import sys
from pathlib import Path
from sqlalchemy.exc import OperationalError, IntegrityError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from labs.lab10.bikes_database.rents_metadata import Bike, Rental, Station, Base
import csv
from sqlalchemy import select
from functools import partial
from datetime import datetime
from labs.ssh_logs_program.src.model.logging_configure import configure_logging
import logging

# 2021-01-31 23:49:56
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def is_non_negative_integer(num):
    return str(num).isdigit()


def is_formatted_date(str_date):
    try:
        datetime.strptime(str_date, DATE_FORMAT)
        return True
    except ValueError:
        return False


CONSTRAINTS = {'rental_id': is_non_negative_integer,
               'bike_number': is_non_negative_integer,
               'start_time': is_formatted_date,
               'end_time': is_formatted_date,
               'rental_station': lambda x: True,
               'return_station': lambda x: True,
               'durance': is_non_negative_integer}


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
    rental_station = get_or_add_station({'station_name': row['rental_station'].strip()}, session)
    return_station = get_or_add_station({'station_name': row['return_station'].strip()}, session)

    rental = Rental(rental_id=row['rental_id'], rent_bike=bike,
                    start_time=datetime.strptime(row['start_time'], DATE_FORMAT),
                    end_time=datetime.strptime(row['end_time'], DATE_FORMAT),
                    rental_station=rental_station, return_station=return_station,
                    durance=row['durance'])

    session.add(rental)
    session.commit()


def validate(data_row):
    for key in CONSTRAINTS.keys():
        if not data_row[key] or not CONSTRAINTS[key](data_row[key]):
            return False
    return True


def load_from_file(engine, filepath):
    with Session(engine) as session:
        with open(filepath, encoding='utf-8') as f:
            fieldnames = ['rental_id', 'bike_number', 'start_time', 'end_time', 'rental_station',
                          'return_station', 'durance']
            dict_reader = csv.DictReader(f, fieldnames=fieldnames)
            next(dict_reader)       # skip header
            for row in dict_reader:
                if not validate(row):
                    logging.error(f"Row '{row}' is invalid")
                else:
                    try:
                        add_rental_data_to_db(row, session)
                    except IntegrityError as err:
                        session.rollback()
                        logging.error(f"Adding {row} caused an error: {err}")


if __name__ == "__main__":

    # sys.argv.append(r'C:\Users\julia\PycharmProjects\ScriptLanguages\labs\lab10\data\test_data.csv')
    # sys.argv.append('bike_rentals.db')

    configure_logging()

    if len(sys.argv) >= 3:
        filepath = Path(sys.argv[1])
        db_name = sys.argv[2]
    else:
        raise ValueError("Provide both file name and database name")

    if not filepath.exists():
        raise FileNotFoundError("File couldn't be found")

    engine = create_engine(f"sqlite:///{db_name}?charset=utf8mb4")
    Base.metadata.create_all(engine)

    load_from_file(engine, filepath)

