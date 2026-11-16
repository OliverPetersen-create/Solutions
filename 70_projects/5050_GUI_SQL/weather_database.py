from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, update

from weather_data import Base, City

Database = "sqlite:///weather_database.db"

def get_record(table, id_):
	with Session(engine) as session:
		record = session.scalars(select(table).where(table.id == id_)).first()
	return record

def insert_data(data):
	with Session(engine) as session:
		session.add(data)
		session.flush()
		id_ = data.id
		session.commit()
	return id_

if __name__ == "__main__":
	pass
else:
	engine = create_engine(Database, echo=False, future=True)
	Base.metadata.create_all(engine)
	if get_record(City, "Høje Taastrup"):
		insert_data(City("Høje Taastrup"))