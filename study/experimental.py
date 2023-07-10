import calendar
import datetime
from datetime import timedelta


print(datetime.date(year=2023, month=1, day=1).strftime("%Y-%m-%d"))

print(datetime.date.today() - timedelta(weeks=12))
print((datetime.date(year=2023, month=1, day=15) - datetime.date(year=2023, month=1, day=10)) == timedelta(days=5))