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

first_number = False
current_number = 0
while True:
	print("- Skriv en af de følgende tal for at bruge operationen -")
	print()
	print("1. Addition")
	print("2. Subtraktion")
	print("3. Multiplikation")
	print("4. Division")
	print("5. Afslut")
	print()
	if first_number:
		print(f"Nuværende kalkulation: {current_number}")
		print()
	try:
		user_input = int(input())
		num1 = 0
		num2 = 0
		print()
		print(f"Du valgte {'option 1. Addition' if user_input == 1 else '' if '' else ''}")
		print()
		user_input = float(input("Hvad er det før"))

	except ValueError:
		print("Vær sød at undgå at skrive nogen bogstaver.")
		print()
