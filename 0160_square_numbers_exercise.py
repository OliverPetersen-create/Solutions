"""
Opgave "square numbers":

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

-------

Skriv kode i funktionen, som printer alle kwadrattal (1, 4, 9, ...), som er mindre end limit.

-------

Hvis du går i stå, så spørg google, de andre elever, en AI eller læreren.

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Fortsæt derefter med den næste fil.
"""


def print_squarenumbers(limit):
    current = 1
    while current ** 2 < limit:
        print(current ** 2)
        current += 1


print_squarenumbers(700)
