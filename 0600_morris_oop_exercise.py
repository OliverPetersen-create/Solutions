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
		self._stats = {"turn": 0, "sleepiness": 0, "thirst": 0, "hunger": 0, "whisky": 0, "gold": 0}

	def _run_attributes(self, attributes):
		self._stats["turn"] += 1
		for attribute, value in attributes.items():
			self._stats[attribute] += value
			if self._stats[attribute] < 0:
				self._stats[attribute] = 0

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
		if self.get_whisky() > 9:
			return
		attributes = {"sleepiness": 5, "thirst": 1, "hunger": 1, "whisky": 1, "gold": -1}
		self._run_attributes(attributes)

	def drink(self):
		if self.get_whisky() < 1:
			return
		attributes = {"sleepiness": 5, "thirst": -15, "hunger": -1, "whisky": -1}
		self._run_attributes(attributes)

	def dead(self):
		return self.get_sleepiness() > 100 or self.get_thirst() > 100 or self.get_hunger() > 100

	def get_gold(self):
		return self._stats["gold"]

	def get_turn(self):
		return self._stats["turn"]

	def get_sleepiness(self):
		return self._stats["sleepiness"]

	def get_hunger(self):
		return self._stats["hunger"]

	def get_thirst(self):
		return self._stats["thirst"]

	def get_whisky(self):
		return self._stats["whisky"]


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
