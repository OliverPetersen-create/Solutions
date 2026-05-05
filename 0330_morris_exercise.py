"""
Opgave "Morris the Miner":

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

-------

Udgangssituation:
Morris har egenskaberne sleepiness, thirst, hunger, whisky, gold.
Alle attributter har startværdien 0.

Regler:
Hvis sleepiness, thirst eller hunger kommer over 100, dør Morris.
Morris kan ikke opbevare mere end 10 flasker whisky.
Ingen attribut kan gå under 0.

Ved hver omgang kan Morris udføre præcis én af disse aktiviteter:
sleep:      sleepiness-=10, thirst+=1,  hunger+=1,  whisky+=0, gold+=0
mine:       sleepiness+=5,  thirst+=5,  hunger+=5,  whisky+=0, gold+=5
eat:        sleepiness+=5,  thirst-=5,  hunger-=20, whisky+=0, gold-=2
buy_whisky: sleepiness+=5,  thirst+=1,  hunger+=1,  whisky+=1, gold-=1
drink:      sleepiness+=5,  thirst-=15, hunger-=1,  whisky-=1, gold+=0

Din opgave:
Skriv et program, der giver Morris så meget guld som muligt på 1000 omgange.

Hvis du ikke har nogen idé om hvordan du skal begynde, så åbn 0332_morris_help.py og start derfra.

-------

Hvis du går i stå, så spørg google, de andre elever, en AI eller læreren.

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Fortsæt derefter med den næste fil.
"""

morris = {"turn": 0, "sleepiness": 0, "thirst": 0, "hunger": 0, "whisky": 0, "gold": 0}

def run_attributes(attributes):
	morris["turn"] += 1
	for attribute, value in attributes.items():
		morris[attribute] += value
		if morris[attribute] < 0:
			morris[attribute] = 0

def sleep():
	attributes = {"sleepiness": -10, "thirst": 1, "hunger": 1}
	run_attributes(attributes)

def mine():
	attributes = {"sleepiness": 5, "thirst": 5, "hunger": 5, "gold": 5}
	run_attributes(attributes)

def eat():
	attributes = {"sleepiness": 5, "thirst": -5, "hunger": -20, "gold": -2}
	run_attributes(attributes)

def buy_whisky():
	if morris["whisky"] > 9:
		return
	attributes = {"sleepiness": 5, "thirst": 1, "hunger": 1, "whisky": 1, "gold": -1}
	run_attributes(attributes)

def drink():
	if morris["whisky"] < 1:
		return
	attributes = {"sleepiness": 5, "thirst": -15, "hunger": -1, "whisky": -1}
	run_attributes(attributes)

def morris_dead():
	return morris["sleepiness"] > 100 or morris["thirst"] > 100 or morris["hunger"] > 100


while not morris_dead() and morris["turn"] < 1000:
	mine()
	if morris["sleepiness"] > 90:
		sleep()
	if morris["hunger"] > 95:
		eat()
	if morris["thirst"] > 95:
		buy_whisky()
		drink()
	print(f"{morris=}")


if not morris_dead():
	print(f"Morris is happy now, since he ended with {morris['gold']} gold.")
else:
	print("You killed Morris.")
