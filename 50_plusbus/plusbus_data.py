from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, DateTime, Integer

Base = declarative_base()

class Kunde(Base):
	__tablename__ = "kunder"
	id = Column(Integer, primary_key=True)
	efternavn = Column(String)
	kontakt = Column(String)
	auth = Column(Integer)

	def __repr__(self):
		return f"Kunde({self.id=}    {self.efternavn=}    {self.kontakt=}    {self.auth=})"

	def convert_to_tuple(self):
		return self.id, self.efternavn, self.kontakt, self.auth

	def valid(self):
		return self.efternavn == "$deleted"

class Rejse(Base):
	__tablename__ = "rejser"
	id = Column(Integer, primary_key=True)
	rute = Column(String)
	dato = Column(DateTime)
	pladskapacitet = Column(Integer)

	def __repr__(self):
		return f"Rejse({self.id=}    {self.rute=}    {self.dato=}    {self.pladskapacitet=})"

	def convert_to_tuple(self):
		return self.id, self.rute, self.dato, self.pladskapacitet

	def valid(self):
		return self.rute == "$deleted"

class Booking(Base):
	__tablename__ = "bookinger"
	id = Column(Integer, primary_key=True)
	kundeid = Column(Integer, ForeignKey("kunder.id"), nullable=False)
	rejseid = Column(Integer, ForeignKey("rejser.id"), nullable=False)
	pladser = Column(Integer)

	def __repr__(self):
		return f"Booking({self.id=}    {self.rejseid=}    {self.pladser=})"

	def convert_to_tuple(self):
		return self.id, self.rejseid, self.pladser

	def valid(self):
		try:
			value = int(self.rejseid)
		except ValueError:
			return False
		return value >= 0
