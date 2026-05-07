import random

class Animal:

	def __init__(self, name, sound, height, weight, legs, female):
		self._name = name
		self._sound = sound
		self._height = height
		self._weight = weight
		self._legs = legs
		self._female = female

	def __repr__(self):
		return f"Animal is named {self._name}, makes the sound {self._sound}, is {self._height} cm high, weighs {self._weight} kg, has {self._legs} legs and is {'female' if self._female else 'male'}"

	def make_noise(self):
		print(self._sound)

	def is_female(self):
		return self._female


class Dog(Animal):

	def __init__(self, name, sound, height, weight, legs, female, tail_length, hunts_sheep):
		super().__init__(name, sound, height, weight, legs, female)
		self._tail_length = tail_length
		self._hunts_sheep = hunts_sheep

	def __add__(self, other):
		return mate(self, other)

	def wag_tail(self):
		print(f"{"Lille" if self._weight < 15 else "Store"} {self._name} vifter sin {self._tail_length} cm lange hale.")


def mate(mother: Dog, father: Dog):
	if not mother.is_female():
		return None
	if father.is_female():
		return None
	newdog = Dog("Unnamed", "whelp", random.uniform(2, 5), random.uniform(0.3, 1), 4, True if random.randint(0, 1) == 0 else False, random.uniform(0.1, 0.3), False)
	return newdog


animal = Animal("Ekans", "Tss", 30.5, 40.4, 4, False)
print(animal)
animal.make_noise()
dog = Dog("Dorthe", "Woof", 30.5, 14, 4, True, 5, False)
dog2 = Dog("Buster", "Woof", 30.5, 14, 4, False, 5, False)
print(dog)
dog.make_noise()
dog.wag_tail()
puppy = dog + dog2
print(puppy)
