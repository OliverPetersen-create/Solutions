"""Opgave: Objektorienteret rollespil, afsnit 1 :

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Del 1:
    Definer en klasse "Character" med attributterne "name", "max_health", "_current_health", "attackpower".
    _current_health skal være en protected attribut, det er ikke meningen at den skal kunne ændres udefra i klassen.

Del 2:
    Tilføj en konstruktor (__init__), der accepterer klassens attributter som parametre.

Del 3:
    Tilføj en metode til udskrivning af klasseobjekter (__repr__).

Del 4:
    Tilføj en metode "hit", som reducerer _current_health af en anden karakter med attackpower.
    Eksempel: _current_health=80 og attackpower=10: et hit reducerer _current_health til 70.
    Metoden hit må ikke ændre den private attribut _current_health i en (potentielt) fremmed klasse.
    Definer derfor en anden metode get_hit, som reducerer _current_health for det objekt, som den tilhører, med attackpower.

Del 5:
    Tilføj en klasse "Healer", som arver fra klassen Character.
    En healer har attackpower=0 men den har en ekstra attribut "healpower".

Del 6:
    Tilføj en metode "heal" til "Healer", som fungerer som "hit" men forbedrer sundheden med healpower.
    For at undgå at "heal" forandrer den protected attribut "_current_health" direkte,
    tilføj en metode get_healed til klassen Character, som fungerer lige som get_hit.

Hvis du er gået i stå, kan du spørge google, de andre elever, en AI eller læreren.
Hvis du ikke aner, hvordan du skal begynde, kan du åbne 0622_rpg1_help.py og starte derfra.

Når dit program er færdigt, skal du skubbe det til dit github-repository
og sammenlign det med lærerens løsning i 0624_rpg1_solution.py
"""


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

	def set_health(self, number):
		self._current_health = number
		if self.get_health() > self.get_max_health():
			self.set_health(self.get_max_health())
		elif self.get_health() < 1:
			self._current_health = 0
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
		self._healpower = 10

	def heal(self, c: Character):
		print("\n", self.get_name(), "heals", c.get_name(), "for", self.get_healpower(), "health")
		c.get_healed(self.get_healpower())

	def set_healpower(self, number):
		self._healpower = number

	def get_healpower(self):
		return self._healpower


hero1 = Character("Bozeto")
hero2 = Character("Andananda")
hero3 = Healer("DoctorX")
print(hero1)
print(hero2)
print(hero3)
hero1.hit(hero2)
print(hero2)
hero3.heal(hero2)
print(hero2)
