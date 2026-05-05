"""
Opgave "Morris The Miner" (denne gang objekt orienteret)

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Genbrug din oprindelige Morris-kode og omskriv den til en objektorienteret version.

Definer en klasse Miner med attributter som sleepiness, thirst osv.
og metoder som sleep, drink osv.
Opret Morris og initialiser hans attributter ved at kalde konstruktoren for Miner:
morris = Miner()

Hvis du går i stå, så spørg google, de andre elever, en AI eller læreren.

Når dit program er færdigt, skal du skubbe det til dit github-repository.
."""


class Miner:

	def __init__(self):  # Jeg laver attributesne private, da det er hvad man normalt ville have gjort i Java, og så bare lave getters til dem, så gør det bare her.
		self._turn = 0
		self._sleepiness = 0
		self._thirst = 0
		self._hunger = 0
		self._whisky = 0
		self._gold = 0

	def _run_attributes(self, attributes):
		self._turn += 1
		# Siden det er attributes nu, så ved jeg ikke lige om jeg bare kan loope igennem dem, så tager den længere metode.
		for attribute, value in attributes.items():
			if attribute == "sleepiness":
				self._sleepiness += value
				if self._sleepiness < 0:
					self._sleepiness = 0
			elif attribute == "thirst":
				self._thirst += value
				if self._thirst < 0:
					self._thirst = 0
			elif attribute == "hunger":
				self._hunger += value
				if self._hunger < 0:
					self._hunger = 0
			elif attribute == "whisky":
				self._whisky += value
				if self._whisky < 0:
					self._whisky = 0
			elif attribute == "gold":
				self._gold += value
				if self._gold < 0:
					self._gold = 0

	def sleep(self):
		attributes = {"sleepiness": -10, "thirst": 1, "hunger": 1}
		self._run_attributes(attributes)

	def mine(self):
		attributes = {"sleepiness": 5, "thirst": 5, "hunger": 5, "gold": 5}
		self._run_attributes(attributes)

	def eat(self):
		attributes = {"sleepiness": 5, "thirst": -5, "hunger": -20, "gold": -2}
		self._run_attributes(attributes)

	def buy_whisky(self):
		if self._whisky > 9:
			return
		attributes = {"sleepiness": 5, "thirst": 1, "hunger": 1, "whisky": 1, "gold": -1}
		self._run_attributes(attributes)

	def drink(self):
		if self._whisky < 1:
			return
		attributes = {"sleepiness": 5, "thirst": -15, "hunger": -1, "whisky": -1}
		self._run_attributes(attributes)

	def dead(self):
		return self._sleepiness > 100 or self._thirst > 100 or self._hunger > 100

	def get_gold(self):
		return self._gold

	def get_turn(self):
		return self._turn

	def get_sleepiness(self):
		return self._sleepiness

	def get_hunger(self):
		return self._hunger

	def get_thirst(self):
		return self._thirst


morris = Miner()

while not morris.dead() and morris.get_turn() < 1000:
	morris.mine()
	if morris.get_sleepiness() > 90:
		morris.sleep()
	if morris.get_hunger() > 95:
		morris.eat()
	if morris.get_thirst() > 95:
		morris.buy_whisky()
		morris.drink()

if not morris.dead():
	print(f"Morris is happy now, since he ended with {morris.get_gold()} gold.")
else:
	print("You killed Morris.")
