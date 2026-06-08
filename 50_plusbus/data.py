from sqlalchemy.orm import declarative_base
from sqlalchemy import Column
from sqlalchemy import String, DateTime, Integer

Base = declarative_base()

class Kunder(Base):
	__tablename__ = "kunder"
	id = Column(Integer, primary_key=True)  # Ved godt denne her ikke stod i opgaven, men vidste ikke lige hvordan kundeid i bookinger skulle fungerer uden denne her, siden flere personer kan have det samme efternavn
	efternavn = Column(String)
	kontakt = Column(String)

	def __repr__(self):
		return f"Kunder({self.id=}    {self.efternavn=}    {self.kontakt=})"

	def convert_to_tuple(self):
		return self.id, self.efternavn, self.kontakt

	def valid(self):
		return self.efternavn == "$deleted"

class Rejser(Base):
	__tablename__ = "rejser"
	id = Column(Integer, primary_key=True)  # Ved godt denne her ikke stod i opgaven, men vidste ikke lige hvordan rejseid i bookinger skulle fungerer uden denne her, siden flere busser kan have den samme rute, dato osv (Tror jeg da... har ikke taget bus før).
	rute = Column(String)
	dato = Column(DateTime)
	pladskapacitet = Column(Integer)

	def __repr__(self):
		return f"Rejser({self.id=}    {self.rute=}    {self.dato=}    {self.pladskapacitet=})"

	def convert_to_tuple(self):
		return self.id, self.rute, self.dato, self.pladskapacitet

	def valid(self):
		return self.rute == "$deleted"

class Bookinger(Base):
	__tablename__ = "bookinger"
	id = Column(Integer, primary_key=True)
	rejseid = Column(Integer, primary_key=True)
	pladser = Column(Integer)

	def __repr__(self):
		return f"Bookinger({self.id=}    {self.rejseid=}    {self.pladser=})"

	def convert_to_tuple(self):
		return self.id, self.rejseid, self.pladser

	def valid(self):
		try:
			value = int(self.rejseid)
		except ValueError:
			return False
		return value >= 0
