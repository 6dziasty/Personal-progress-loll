import random

alfabet_male = "abcdefghijklmnopqrstuvwxyz"
alfabet_duze = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
liczby = "0123456789"
znaki_specjalne = ",./<>?;':@#$%^&*_+-=|`~"

def pobierz_opcje():
    """Pobiera od użytkownika, czy chce dane grupy znaków."""
    uzywaj_male = input("Czy używać małych liter? (y/n): ").lower() == 'y'
    uzywaj_duze = input("Czy używać dużych liter? (y/n): ").lower() == 'y'
    uzywaj_liczb = input("Czy używać liczb? (y/n): ").lower() == 'y'
    uzywaj_specjalnych = input("Czy używać znaków specjalnych? (y/n): ").lower() == 'y'
    return uzywaj_male, uzywaj_duze, uzywaj_liczb, uzywaj_specjalnych

def pobierz_dlugosc():
    """Pobiera od użytkownika żądaną długość hasła."""
    while True:
        try:
            dlugosc = int(input("Podaj długość hasła (min. 8): "))
            if dlugosc >= 8:
                return dlugosc
            else:
                print("Długość musi być co najmniej 8 znaków.")
        except ValueError:
            print("Podaj liczbę!")

def generuj_haslo_z_opcjami(dlugosc, uzywaj_male, uzywaj_duze, uzywaj_liczb, uzywaj_specjalnych):
    """Generuje hasło na podstawie wybranych opcji."""
    znak_zbior = ""
    if uzywaj_male:
        znak_zbior += alfabet_male
    if uzywaj_duze:
        znak_zbior += alfabet_duze
    if uzywaj_liczb:
        znak_zbior += liczby
    if uzywaj_specjalnych:
        znak_zbior += znaki_specjalne

    if not znak_zbior:
        print("Nie wybrałeś żadnej grupy znaków!")
        return ""

    # Tutaj będzie logika generowania z gwarancją, że każde wymagane znaki się pojawią:
    # Na przykład przez ręczne dołożenie jednego znaku z każdej grupy,
    # a resztę dopełnić losowaniem z całości.

    return "tu_będzie_hasło"
    print("Twoje hasło:", haslo)

if __name__ == "__main__":
    opcje = pobierz_opcje()
    dlugosc = pobierz_dlugosc()
    haslo = generuj_haslo_z_opcjami(dlugosc, *opcje)
    print("Twoje hasło:", haslo)
