import random
import time



saldo = 500
poziom = 1
dzień = 1

 

def menu():
    print(f"\n Dzień {dzień} | 💰Saldo: {saldo} zł | 🧠Poziom: {poziom}")
    print("1. Idź do pracy")
    print("2. Wydaj hajs")
    print("3. Sprawdź wydarzenia")
    print("4. Wyjdź z życia")

while True:
    menu()
    wybor = input("Co robisz? (1-4): ")

    if wybor == "1":
        zarobek = random.randint(100 * poziom, 200 * poziom)
        saldo += zarobek
        print(f"Poszedłeś do roboty i zarobiłeś {zarobek} zł!")
        dzień += 1

        if random.random() < 0.2:
            poziom += 1
            print("Gratulacje! Awansowałeś!")

    elif wybor == "2":
        wydatek = random.choice([("Hot-dog", 15), ("Nowy telefon", 1000), ("Bilet do kina", 40), ("Kawa", 10), ("Zestaw do gier", 500), ("Książka", 30), 
                                 ("Kulig z znajomymi", 200), ("Wycieczka", 1500)])
        nazwa, koszt = wydatek
        if saldo >= koszt:
            saldo -= koszt
            print(f"Kupiłeś: {nazwa} za {koszt} zł")
            dzień += 1
        else:
            print("Nie stać cię na to!")

    elif wybor == "3":
        wydarzenia = [
            ("Znalazłeś 50 zł na chodniku!", +50),
            ("Twoja babcia dała ci 200 zł na urodziny!", +200),
            ("Zgubiłeś portfel z 300 zł!", -300),
            ("Dostałeś mandat za parkowanie -150 zł", -150),
            ("Wygrałeś na loterii 1000 zł!", +1000),
            ("Zruchałeś konia i straciłeś 300 zł", -300),
            ("Musiałeś zapłacić rachunki -250 zł", -350),
            ("Kupiłeś nową konsolę za 1200 zł", -1200),
            ("Zgubiłeś 100 zł w tramwaju.", -100),
            ("Ktoś cię okradł! -200 zł", -200),
            ("Wygrałeś 500 zł w zdrapce!", +500),
            ("Zepsuł ci się telefon, naprawa kosztuje 150 zł", -150),
            ("Znalazłeś przystojnego mężczyzne imieniem, Maksymilian i dales mu całe swoje oszczędności", "all"),
        
        ]
        opis, zmiana = random.choice(wydarzenia)
        if zmiana == "all":
            saldo = 0
        else:
            saldo += zmiana
        print(f" Wydarzenie: {opis}")
        dzień += 1

    elif wybor == "4":
        print("🫡 Życie zakończone. Dziękujemy za grę!")
        break

    if saldo < 0:
        print("Nie masz już pieniędzy! Gra zakończona.")
        break

    if wybor not in ["1", "2", "3", "4"]:
        print("Nie ma takiej opcji.")

     
