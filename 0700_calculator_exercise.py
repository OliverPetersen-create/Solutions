""" Øvelse: "Calculator"

Som altid, læs hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning i kopien.

-------

Opret et program, der fungerer som en simpel lommeregner. Programmet skal fungere som følger:
    1. Forklar brugeren hvordan man betjener programmet.
    2. Præsenter en menu med følgende muligheder:
        - Addition
        - Subtraktion
        - Multiplikation
        - Division
        - Afslut
    3. Bed brugeren om at vælge en mulighed fra menuen.
    4. Hvis brugeren vælger en aritmetisk operation, bed om to tal.
    5. Udfør den valgte operation og vis resultatet.
    6. Gentag processen, indtil brugeren vælger at afslutte.

-------

Hvis du går i stå, spørg Google, andre elever, en AI eller læreren.

Når dit program er færdigt, skub det til dit GitHub-repository.
"""


while True:
	print("- Skriv en af de følgende tal for at bruge operationen -")
	print()
	print("1. Addition")
	print("2. Subtraktion")
	print("3. Multiplikation")
	print("4. Division")
	print("5. Afslut")
	print()
	try:
		user_input = int(input())
		print()
		match user_input:
			case 1:
				print("Du valgte option 1. Addition")
			case 2:
				print("Du valgte option 2. Subtraktion")
			case 3:
				print("Du valgte option 3. Multiplikation")
			case 4:
				print("Du valgte option 4. Division")
			case 5:
				print("Du valgte option 5. Afslut")
				print("Afslutter nu.")
				break
			case _:
				print("Vælg en option mellem 1-5.")
				print()
				continue
		num1 = float(input("Hvad er dit første tal du vil bruge med operatoren? "))
		num2 = float(input("Hvad er dit andet tal du vil bruge med operatoren? "))
		match user_input:
			case 1:
				result = num1 + num2
			case 2:
				result = num1 - num2
			case 3:
				result = num1 * num2
			case 4:
				result = num1 / num2
		print(f"\nDit resultat er {result}")
		print()
	except ValueError:
		print("Vær sød at undgå at skrive nogen bogstaver eller symboler.")
		print()
