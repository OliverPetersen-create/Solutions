from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

from data import Base

Database = "sqlite:///database.db"

def select_all(table):
	with Session(engine) as session:
		records = session.scalars(select(table))
		result = []
		for record in records:
			result.append(record)
	return result

def get_record(table, id_):
	with Session(engine) as session:
		record = session.scalars(select(table).where(table.id == id_)).first()
	return record

# def get_kunde(kunde: Kunder, id_):
# 	with Session(engine) as session:
# 		record = session.scalars(select(kunde).where(kunde.id == id_)).first()
# 	return record
#
# def get_rejse(rejse: Rejser, id_):
# 	with Session(engine) as session:
# 		record = session.scalars(select(rejse).where(rejse.id == id_)).first()
# 	return record
#
# def get_booking(booking: Bookinger, kunde_id):
# 	with Session(engine) as session:
# 		record = session.scalars(select(booking).where(booking.kundeid == kunde_id)).first()
# 	return record


if __name__ == "__main__":
	engine = create_engine(Database, echo=False, future=True)
	Base.metadata.create_all(engine)
else:
	engine = create_engine(Database, echo=False, future=True)
	Base.metadata.create_all(engine)