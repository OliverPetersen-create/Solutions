from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, delete

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

def delete_record(location):
	with Session(engine) as session:
		session.execute(delete(Location).where(Location.location == location))
		session.commit()

def get_all_records():
	with Session(engine) as session:
		records = session.scalars(select(Location)).all()
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
	if len(get_all_records()) < 1:
		insert_data(Location(location="høje taastrup"))