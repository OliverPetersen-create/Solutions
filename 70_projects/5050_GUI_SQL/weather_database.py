from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, update

from weather_data import Base, Location, Weather

Database = "sqlite:///weather_database.db"

def get_record_id(id_):
	with Session(engine) as session:
		record = session.scalars(select(Location).where(Location.id == id_)).first()
	return record

def get_record(location):
	with Session(engine) as session:
		record = session.scalars(select(Location).where(Location.location == location)).first()
	return record

def get_all_records(table):
	with Session(engine) as session:
		records = session.scalars(select(table)).all()
	return records

def insert_data(data):
	with Session(engine) as session:
		session.add(data)
		session.flush()
		id_ = data.id
		session.commit()
	return id_


engine = create_engine(Database, echo=False, future=True)
Base.metadata.create_all(engine)
if __name__ == "__main__":
	if get_record("høje taastrup") is None:
		insert_data(Location(location="høje taastrup"))
	else:
		Weather("høje taastrup")
		print(get_record("høje taastrup"))
		print(Weather.get_weather("høje taastrup"))
else:
	if get_record_id(1) is None:
		insert_data(Location(location="høje taastrup"))