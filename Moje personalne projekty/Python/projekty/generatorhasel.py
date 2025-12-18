import random

alfabet = "abcdefghijklmnopqrstuvwxyz"
duzyalfabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
liczby = "0123456789"
znaki = ",./<>?;':@#$%^&*_+-=|`~"

def liczba_znakow():
    return random.randint(8, 16)

def generuj_haslo():
    """Generuje losowe hasło."""
    dlugosc = liczba_znakow()
    haslo = ''.join(random.choices(alfabet + duzyalfabet + liczby + znaki, k=dlugosc))
    return haslo

if __name__ == "__main__":
    print("Generowane hasła:")
    for iloschasel in range(5):
        print(f"{iloschasel+1}: {generuj_haslo()}")

