from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, update

from weather_data import Base, City, Weather

Database = "sqlite:///weather_database.db"

def get_record_id(table, id_):
	with Session(engine) as session:
		record = session.scalars(select(table).where(table.id == id_)).first()
	return record

def get_record(table, city):
	with Session(engine) as session:
		record = session.scalars(select(table).where(table.city == city)).first()
	return record

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
	if get_record(City, "høje taastrup") is None:
		insert_data(City(city="høje taastrup"))
	else:
		Weather("høje taastrup")
		print(get_record(City, "høje taastrup"))
		print(Weather.get_weather("høje taastrup"))
else:
	if get_record_id(City, 1) is None:
		insert_data(City(city="høje taastrup"))