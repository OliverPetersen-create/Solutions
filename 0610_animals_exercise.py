class Animal:

	def __init__(self, name, sound, height, weight, legs, female):
		self._name = name
		self._sound = sound
		self._height = height
		self._weight = weight
		self._legs = legs
		self._female = female

	def __repr__(self):
		if self._female:
			gender = "female"
		else:
			gender = "male"
		return f"Animal is named {self._name}, makes the sound {self._sound}, is {self._height} cm high, weighs {self._weight}, has {self._legs} legs and is {gender}"
