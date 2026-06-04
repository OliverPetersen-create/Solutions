"""
Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

--------

Anvend det, du har lært i dette kapitel om databaser, på en denne opgave.

Trin 1:
Opret en ny SQLite database "2311_my_second_sql_database.db" i din solutions mappe.
Denne database skal indeholde 2 tabeller.
Den første tabel skal hedde "customers" og repræsenteres i Python-koden af en klasse kaldet "Customer".
Tabellen bruger sin første attribut "id" som primærnøgle.
De andre attributter i tabellen hedder "name", "address" og "age".
Definer selv fornuftige datatyper for attributterne.

Trin 2:
Den anden tabel skal hedde "products" og repræsenteres i Python-koden af en klasse kaldet "Product".
Denne tabel bruger også sin første attribut "id" som primærnøgle.
De andre attributter i tabellen hedder "product_number", "price" og "brand".

Trin 3:
Skriv en funktion create_test_data(), der opretter testdata for begge tabeller.

Trin 4:
Skriv en metode __repr__() for begge dataklasser, så du kan vise poster til testformål med print().

Til læsning fra databasen kan du genbruge de to funktioner select_all() og get_record() fra 2240_db_class_methods.py.

Trin 5:
Skriv hovedprogrammet: Det skriver testdata til databasen, læser dataene fra databasen med select_all() og/eller get_record() og udskriver posterne til konsollen med print().

--------

Når dit program er færdigt, skal du skubbe det til dit github-repository.
"""

from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine, select

Database = "sqlite:////2311_my_second_sql_database.db"
Base = declarative_base()

class Customer(Base):
	__tablename__ = "customers"
	id = Column(Integer, primary_key=True)
	name = Column(String)
	address = Column(String)
	age = Column(Integer)

	def __repr(self):
		return f"Customer({self.id=}   {self.name=}   {self.address=}   {self.age=})"

class Product(Base):
	__tablename__ = "products"
	id = Column(Integer, primary_key=True)
	product_number = Column(Integer)
	price = Column(Integer)
	brand = Column(String)

	def __repr(self):
		return f"Product({self.id=}   {self.product_number=}   {self.price=}   {self.brand=})"

def create_test_data():
	with Session(engine) as session:
		test_data = []
		test_data.append(Customer(name="Jens", age=44))
		test_data.append(Customer(name="Marius", address="København", age=22))
		test_data.append(Customer(name="SomeOtherNameICantComeUpWith", address="Ulano", age=87))
		test_data.append(Product(product_number=0, price=255, brand="Yesno"))
		test_data.append(Product(product_number=1, price=257))
		test_data.append(Product(brand="Hah"))
		session.add_all(test_data)
		session.commit()

def select_all(table):
	with Session(engine) as session:
		records = session.scalars(select(table))
		result = []
		for record in records:
			result.append(record)
	return result

def get_record(table, record_id):
	with Session(engine) as session:
		record = session.scalars(select(table).where(table.id == record_id)).first()
	return record


engine = create_engine(Database, echo=False, future=True)
Base.metadata.create_all(engine)

create_test_data()
print(f"Product #1: {get_record(Product, 1)}")
print(f"Customer #1: {get_record(Customer, 1)}")
for products in select(Product):
	print(f"Products: {products}")
for customers in select(Customer):
	print(f"Products: {customers}")
