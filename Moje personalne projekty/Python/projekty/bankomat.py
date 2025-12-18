import random
saldo = float(input("Podaj ile masz mamony "))  # początkowa kwota na koncie

def menu():
    print("---- BANKOMAT ----")
    print("1. Sprawdź saldo")
    print("2. Wpłać pieniądze")
    print("3. Wypłać pieniądze")
    print("4. Fortuna")
    print("5. Ranking")
    print("6. Wyjście")

while True:
    menu()
    wybor = input("Wybierz opcję (1-6) ")

    if wybor == "1":
        print(f"Twoje saldo wynosi: {saldo} zł")

    elif wybor == "2":
        kwota = float(input("Ile chcesz wpłacić? "))
        if kwota > 0:
            saldo += kwota
            print(f"Wpłacono {kwota} zł. Nowe saldo: {saldo} zł")
        else:
            print("Nieprawidłowa kwota.")

    elif wybor == "3":
        kwota = float(input("Ile chcesz wypłacić? "))
        if kwota > 0 and kwota <= saldo:
            saldo -= kwota
            print(f"Wypłacono {kwota} zł. Nowe saldo: {saldo} zł")
        else:
            print("Nieprawidłowa kwota lub brak środków.")

    elif wybor == "4":
        fortuna = random.randint(1, 2)

        if fortuna == 1:
            wygrana = random.randint(1, 100)
            saldo += wygrana
            print(f"Wygrałeś {wygrana} zł! Nowe saldo: {saldo} zł")
        else:
            przegrana = random.randint(1, 100)
            saldo -= przegrana
            print(f"Przegrałeś {przegrana} zł. Nowe saldo: {saldo} zł")

    elif wybor == "5":
        print("---Ranking---")
        imie_gracza = random.choice(["Kurwigrad", "Kurwołuszy", "Kurwosław", "Kurwomir", "Kurwosławka"])
        ranking = random.randint(10,5000)
        if saldo > ranking:
            print(f"Twoje saldo {saldo} zł jest powyżej losowego gracza z nazwą {imie_gracza} z kwotą {ranking} zł")
            print("Gratki stary jesteś powyżej losowego gracza")
        else:
            print(f"Niestety jesteś poniżej losowego gracza z nazwą {imie_gracza} który posiada {ranking} zł, może zagraj w fortune???")


    elif wybor == "6":
        print("Elo żelo gówno 320!")
        break

    else:
        print("Nie ma takiej opcji. Spróbuj jeszcze raz.")
        print("Wpisz ponownie........")