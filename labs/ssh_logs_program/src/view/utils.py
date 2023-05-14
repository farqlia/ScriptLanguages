from PySide6.QtCore import QDateTime
import datetime as dt


def to_datetime(qdatetime: QDateTime):
    return dt.datetime(year=qdatetime.date().year(),
                       month=qdatetime.date().month(),
                          day=qdatetime.date().day(),
                       hour=qdatetime.time().hour(),
                          minute=qdatetime.time().minute(),
                       second=qdatetime.time().second())


def to_q_datetime(string):
    date_format = "%d-%m-%y %H:%M:%S"
    return QDateTime.fromString(string, date_format)