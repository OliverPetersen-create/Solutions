""" Opgave "Number guessing"

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

--------

Opret et program, der spiller et gættespil med brugeren. Programmet fungerer på følgende måde:
    Forklar reglerne for brugeren.
    Generer tilfældigt et 4-cifret heltal.
    Bed brugeren om at gætte et 4-cifret tal.
    Hvert ciffer, som brugeren gætter korrekt i den rigtige position, tæller som en sort mønt.
    Hvert ciffer, som brugeren gætter korrekt, men i den forkerte position, tæller som en hvid mønt.
    Når brugeren har gættet, udskrives det, hvor mange sorte og hvide mønter gættet er værd.
    Lad brugeren gætte, indtil gættet er korrekt.
    Hold styr på antallet af gæt, som brugeren gætter i løbet af spillet, og print det ud til sidst.

--------

Hvis du går i stå, så spørg google, de andre elever, en AI eller læreren.

Når dit program er færdigt, skal du skubbe det til dit github-repository.
"""
import random


print("Programmet vil genere et 4-cifret tal, tag et gæt på hvad det kan være.")
print("Hvis du gætter et tal korrekt i dens rigtige position, får du 1 sort mønt.")
print("Hvis du gætter et tal korrekt i dens forkerte position, får du 1 hvid mønt.")
print("Du får af vide hvor mange af hver mønt du har hvert gæt.")
print("Gæt tallet i så få gæt så muligt, held og lykke.")
print()
guesses = 0
correct_number = ""
for i in range(4):  # Lavede tallet sådan her i stedet for random.randint(1000, 9999) fordi ellers kunne det første tal aldrig være 0
	correct_number += f"{random.randint(0, 9)}"
while True:
	black_coins = 0
	white_coins = 0
	try:
		guess = input("Hvad tror du tallet er? ")
		if guess == "/cheat":
			print(f"Tallet er {correct_number}, snydepels.")
			continue
		if len(guess) < 4 or len(guess) > 4:
			print("Du skal gætte på et 4-cifret tal!")
			print()
			continue
		for index in range(4):
			int(guess[index])
			if guess[index] == correct_number[index]:
				black_coins += 1
			elif guess[index] in correct_number:
				white_coins += 1
		print(f"Du fandt {black_coins} sorte mønter og {white_coins} hvide mønter.")
		guesses += 1
		if guess == correct_number:
			print(f"Du fandt tallet! Det var {correct_number}")
			print(f"Det tog dig {guesses} gæt.")
			break
	except ValueError:
		print("Vær sød at gætte på et ordenligt tal!")
		print()
