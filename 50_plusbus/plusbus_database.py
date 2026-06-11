from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

from plusbus_data import Base, Kunde

Database = 'sqlite:///plusbus_database.db'

def select_all(table):
	with Session(engine) as session:
		records = session.scalars(select(table))
		result = []
		for record in records:
			result.append(record)
	return result

def create_test_data():
	with Session(engine) as session:
		test_data = []
		test_data.append(Kunde(efternavn="Petersen(Mig selv ja)", kontakt="Tlf. 27813897"))
		test_data.append(Kunde(efternavn="Hej", kontakt="test@gmail.com"))
		session.add_all(test_data)
		session.commit()

def insert_data(data):
	with Session(engine) as session:
		session.add(data)
		session.commit()

def get_record(table, id_):
	with Session(engine) as session:
		record = session.scalars(select(table).where(table.id == id_)).first()
	return record


if __name__ == "__main__":
	engine = create_engine(Database, echo=False, future=True)
	Base.metadata.create_all(engine)
	# create_test_data()
	# insert_data(Kunde(efternavn="Lol", kontakt="Ingen"))
	if get_record(Kunde, 1) is None:
		print("Kunden findes ikke")
	else:
		print(f"#1: {get_record(Kunde, 1)}")
		print(select_all(Kunde))
else:
	engine = create_engine(Database, echo=False, future=True)
	Base.metadata.create_all(engine)
