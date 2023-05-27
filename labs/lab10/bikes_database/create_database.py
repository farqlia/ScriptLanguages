from labs.lab10.bikes_database.rents_metadata import Base
from sqlalchemy import create_engine
import sys

if __name__ == "__main__":

    db_name = sys.argv[1] if len(sys.argv) > 1 else "my_db.db"
    engine = create_engine(f"sqlite:///{db_name}", echo=True)
    Base.metadata.create_all(engine)
