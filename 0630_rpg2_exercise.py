"""opgave: Objektorienteret rollespil, afsnit 2 :

Som altid skal du læse hele øvelsesbeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Byg videre på din løsning af afsnit 1.

Del 1:
    Opfind to nye klasser, som arver fra klassen Character. For eksempel Hunter og Magician.
    Dine nye klasser skal have deres egne ekstra metoder og/eller attributter.
    Måske overskriver de også metoder eller attributter fra klassen Character.

Del 2:
    Lad i hovedprogrammet objekter af dine nye klasser (dvs. rollespilfigurer) kæmpe mod hinanden,
    indtil den ene figur er død. Udskriv, hvad der sker under kampen.

I hver omgang bruger en figur en af sine evner (metoder). Derefter er det den anden figurs tur.
Det er op til dig, hvordan dit program i hver tur beslutter, hvilken evne der skal bruges.
Beslutningen kan f.eks. være baseret på tilfældighed eller på en smart strategi

Del 3:
    Hver gang en figur bruger en af sine evner, skal du tilføje noget tilfældighed til den anvendte evne.

Del 4:
    Lad dine figurer kæmpe mod hinanden 100 gange.
    Hold styr på resultaterne.
    Prøv at afbalancere dine figurers evner på en sådan måde, at hver figur vinder ca. halvdelen af kampene.

Hvis du går i stå, kan du spørge google, de andre elever, en AI eller læreren.

Når dit program er færdigt, skal du skubbe det til dit github-repository.
"""


import random

class Character:

	def __init__(self, name):  # Alt andet end Name er hard-coded siden det her ville blive set som en "character creator", og derfor burde alle spillere så starte med de samme stats (baseret på ens play-style, fx: healer)
		self._name = name
		self._max_health = 100
		self._current_health = 100
		self._attackpower = 10
		self._dead = False

	def __repr__(self):
		return f"Character is named {self.get_name()}, has {self.get_max_health()} max health, currently has {self.get_health()} health and has {self.get_attackpower()} attack power"

	def hit(self, c: Character):
		print("\n", self.get_name(), "hits", c.get_name(), "for", self.get_attackpower(), "damage")
		c.get_hit(self.get_attackpower())

	def get_hit(self, number):  # Grunden til jeg valgte stadig at lave en get_hit method, selvom jeg allerede har en damage method, er fordi siden det her er en RPG, kunne ting som fall damage være en ting, og derfor ved vi at get_hit ville være skade fra en anden spiller af.
		self.damage(number)

	def get_healed(self, number):  # Samme grund til get_hit
		self.set_health(self.get_health() + number)

	def damage(self, number):
		self.set_health(self.get_health() - number)
		if self.get_health() < 0:
			self.set_health(0)

	def set_health(self, number):
		self._current_health = number
		if self.get_health() > self.get_max_health():
			self.set_health(self.get_max_health())
		elif self.get_health() < 0:
			self.set_health(0)
			self.has_died()

	def get_health(self):
		return self._current_health

	def set_max_health(self, number):
		self._max_health = number
		if self.get_health() > self.get_max_health():
			self.set_health(self.get_max_health())

	def get_max_health(self):
		return self._max_health

	def set_attackpower(self, number):
		self._attackpower = number

	def get_attackpower(self):
		return self._attackpower

	def get_name(self):
		return self._name

	def has_died(self):
		self._dead = True
		print("\n", self.get_name(), "died")

	def is_dead(self):
		return self._dead

class Healer(Character):

	def __init__(self, name):
		super().__init__(name)
		self._attackpower = 0
		self._max_health = 50
		self._current_health = 50
		self._healpower = 10

	def heal(self, c: Character):
		print("\n", self.get_name(), "heals", c.get_name(), "for", self.get_healpower(), "health")
		c.get_healed(self.get_healpower())

	def set_healpower(self, number):
		self._healpower = number

	def get_healpower(self):
		return self._healpower

class Hunter(Character):

	def __init__(self, name):
		super().__init__(name)
		self._attackpower = 15
		self._max_health = 80
		self._current_health = 80
		self._arrows = 10
		self._experience = 0
		self._accuracy = 50
		self._wastedturns = 0

	def shoot(self, c: Character):
		if random.random() + self.get_experience() / 100 > 0.95:
			self._accuracy += 5
			self._experience = 0
		if self.get_arrows() < 1 or self.get_wasted_turns() > 0:
			if self.get_wasted_turns() > 0:
				return
			else:
				self._wastedturns = 3
		print("\n", self.get_name(), "takes a shot at", c.get_name())
		self._arrows -= 1
		if random.random() < (self._accuracy / 100):
			c.get_hit(self.get_attackpower())
		else:
			print("\n", self.get_name(), "missed their shot")
			self._experience += 5

	def craft_arrows(self):
		if self.get_wasted_turns() > 0:
			self._arrows += 3
			self._wastedturns -= 1

	def get_arrows(self):
		return self._arrows

	def get_experience(self):
		return self._experience

	def get_wasted_turns(self):
		return self._wastedturns

# class