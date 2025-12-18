import random

alfabet = "abcdefghijklmnopqrstuvwxyz"
duzyalfabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
liczby = "0123456789"
znaki = ",./<>?;':@#$%^&*_+-=|`~"

#podaj liczbe znakow do wygenerowania hasla

def liczba_znakow():
    return random.randint(8, 16)

def generuj_haslo(uzywaj_male, uzywaj_duze, uzywaj_liczb, uzywaj_specjalne):

    zbior = ""
    wymagane_znaki = []

    if uzywaj_male:
        zbior += alfabet
        wymagane_znaki.append(random.choice(alfabet))
    if uzywaj_duze:
        zbior += duzyalfabet
        wymagane_znaki.append(random.choice(duzyalfabet))
    if uzywaj_liczb:
        zbior += liczby
        wymagane_znaki.append(random.choice(liczby))
    if uzywaj_specjalne:
        zbior += znaki
        wymagane_znaki.append(random.choice(znaki))

    if not zbior:
        return "Nie wybrałeś żadnych znaków."

    dlugosc = max(liczba_znakow(), len(wymagane_znaki))

    haslo = wymagane_znaki.copy()
    while len(haslo) < dlugosc:
        haslo.append(random.choice(zbior))

    random.shuffle(haslo)

    return ''.join(haslo)

if __name__ == "__main__":
    print("Opcje generowania hasła:")
    male = input("Czy używać małych liter? (t/n): ").lower() == "t"
    duze = input("Czy używać dużych liter? (t/n): ").lower() == "t"
    liczby_opcja = input("Czy używać liczb? (t/n): ").lower() == "t"
    znaki_opcja = input("Czy używać znaków specjalnych? (t/n): ").lower() == "t"

    print("Generowane hasła:")
    for i in range(5):
        print(f"{i + 1}: {generuj_haslo(male, duze, liczby_opcja, znaki_opcja)}")
