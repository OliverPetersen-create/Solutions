"""
Kør dette program.
Tilføj oop-relaterede kommentarer til denne kode.
    Eksempler:
        class definition / klasse definition
        constructor / konstruktor
        inheritance / nedarvning
        object definition / objekt definition
        attribute / attribut
        method / metode
        polymorphism / polymorfisme
        encapsulation: protected attribute / indkapsling: beskyttet attribut
        encapsulation: protected method / indkapsling: beskyttet metode
"""


class Building: # Starten af Building klassen
    def __init__(self, area, floors, value): # Building klasse konstruktor, sætter attributes til argumenterne når du laver en ny instance af Building
        self.area = area
        self.floors = floors
        self._value = value # Dette er en privat/protected attribute, kun brug denne indenfor klassen

    def renovate(self): # En normal method, som kalder en privat/protected method.
        print("Installing an extra bathroom...")
        self._adjust_value(10)  # <- er god

    def _adjust_value(self, percentage): # En privat/protected method, kun kald denne method indenfor klassen
        self._value *= 1 + (percentage / 100) # Ændrer en privat/protected attribute
        print(f'Value has been adjusted by {percentage}% to {self._value:.2f}\n')


class Skyscraper(Building): # Arver methods (og attributes, men kun hvis de er globale indenfor klassen.) fra Building klassen

    def renovate(self): # Overrider renovate() methoden fra Building klassen
        print("Installing a faster elevator.")
        self._adjust_value(6) # Ændrer privat/protected attribute arvet fra Building klassen af


small_house = Building(160, 2, 200000) # Skaber en ny instance af Building klassen og kalder __init__ (konstruktoren)
skyscraper = Skyscraper(5000, 25, 10000000) # Skaber en ny instance af Skyscraper klassen og kalder __init__ (konstruktoren) fra Building klassen

for building in [small_house, skyscraper]: # For loop som gennemgår begge instances
    print(f'This building has {building.floors} floors and an area of {building.area} square meters.') # Kalder attributes fra 2 forskellige klasser, men er de samme attributes pågrund af arv.
    building.renovate() # Polymorphism
