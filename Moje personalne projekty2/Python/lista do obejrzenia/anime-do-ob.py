import json
import os
import random
from tabulate import tabulate

FILE_NAME = "anime.json"

categories = [
    "Akcja",
    "Romans",
    "Psychologiczne",
    "Dramat",
    "Fantasy",
    "Klasyki"
]


# ----------------- Wczytanie danych -----------------
def load_data():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                data = json.load(f)
                for cat in categories:
                    if cat not in data:
                        data[cat] = []
                return data
        except:
            return {cat: [] for cat in categories}
    return {cat: [] for cat in categories}

def save_data():
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(anime_list, f, ensure_ascii=False, indent=4)

# ----------------- Menu -----------------
def show_menu():
    print("\n========== ANIME TRACKER ==========")
    print("1. ➕ Dodaj nowe anime")
    print("2. 📂 Zobacz anime w danej kategorii")
    print("3. 📜 Zobacz wszystkie anime")
    print("4. ✅ Oznacz jako obejrzane")
    print("5. ❌ Usuń anime")
    print("6. 🎲 Wybierz losowe anime do obejrzenia")
    print("7. 🚪 Wyjście")
    print("===================================")

# ----------------- Funkcje -----------------
def add_anime():
    title = input("Podaj tytuł anime: ").strip()
    print("\nWybierz kategorię:")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
    choice = int(input(">> "))
    category = categories[choice - 1]
    
    desc = input("Dodaj krótki opis (lub zostaw puste): ").strip()
    seasons = input("Ile sezonów? ").strip()
    episodes = input("Ile odcinków? ").strip()
    
    anime_list[category].append({
        "title": title,
        "desc": desc,
        "watched": False,
        "seasons": seasons,
        "episodes": episodes,
        "category": category
    })
    anime_list[category] = sorted(anime_list[category], key=lambda x: x['title'].lower())
    save_data()
    print(f"✅ Dodano: {title} do kategorii {category}")

def show_category():
    print("\nWybierz kategorię:")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
    choice = int(input(">> "))
    category = categories[choice - 1]
    if not anime_list[category]:
        print("Brak anime w tej kategorii.")
        return
    table = []
    for anime in anime_list[category]:
        status = "!!!!!obejrzane!!!!!" if anime["watched"] else "?????????nieobejrzane????????"
        table.append([anime["title"], anime["desc"], anime["seasons"], anime["episodes"], status])
    print(f"\n--- {category} ---")
    print(tabulate(table, headers=["Tytuł", "Opis", "Sezony", "Odcinki", "Status"], tablefmt="fancy_grid"))

def show_all():
    for category in categories:
        if anime_list[category]:
            table = []
            for anime in anime_list[category]:
                status = "!!!!!obejrzane!!!!!" if anime["watched"] else "??????nieobejrzane???????"
                table.append([anime["title"], anime["desc"], anime["seasons"], anime["episodes"], status])
            print(f"\n--- {category} ---")
            print(tabulate(table, headers=["Tytuł", "Opis", "Sezony", "Odcinki", "Status"], tablefmt="fancy_grid"))
            print()  # <-- ta linia daje przerwę między kategoriami


def mark_watched():
    show_all()
    title = input("Podaj dokładny tytuł anime, które obejrzałeś: ").strip()
    found = False
    for cat in categories:
        for anime in anime_list[cat]:
            if anime["title"].lower() == title.lower():
                anime["watched"] = True
                # tu dodajemy ocenę
                while True:
                    try:
                        rating = int(input("Oceń anime w skali 1–10: "))
                        if 1 <= rating <= 10:
                            anime["rating"] = rating
                            break
                        else:
                            print("❌ Ocena musi być 1–10")
                    except:
                        print("❌ Wpisz liczbę od 1 do 10")
                save_data()
                print(f"✅ Oznaczono jako obejrzane: {anime['title']} (Ocena: {anime['rating']})")
                found = True
    if not found:
        print("❌ Nie znaleziono anime o takim tytule.")


def delete_anime():
    show_all()
    title = input("Podaj dokładny tytuł anime do usunięcia: ").strip()
    found = False
    for cat in categories:
        for anime in anime_list[cat]:
            if anime["title"].lower() == title.lower():
                anime_list[cat].remove(anime)
                save_data()
                print(f"❌ Usunięto: {anime['title']}")
                found = True
                break
    if not found:
        print("❌ Nie znaleziono anime o takim tytule.")

def random_anime():
    unwatched = []
    for cat in categories:
        for anime in anime_list[cat]:
            if not anime["watched"]:
                unwatched.append(anime)
    if not unwatched:
        print("🎉 Wszystkie anime zostały obejrzane!")
        return
    choice = random.choice(unwatched)
    print("\n🎲 Losowe anime do obejrzenia:")
    print(tabulate([[choice["title"], choice["desc"], choice["seasons"], choice["episodes"], "?????????nieobejrzane????????"]],
                   headers=["Tytuł", "Opis", "Sezony", "Odcinki", "Status"], tablefmt="fancy_grid"))        

# ----------------- GŁÓWNA PĘTLA -----------------
anime_list = load_data()

while True:
    show_menu()
    option = input("Wybierz opcję: ").strip()
    if option == "1":
        add_anime()
    elif option == "2":
        show_category()
    elif option == "3":
        show_all()
    elif option == "4":
        mark_watched()
    elif option == "5":
        delete_anime()
    elif option == "6":
        random_anime()
    elif option == "7":
        print("👋 Do zobaczenia!")
        break
    else:
        print("❌ Nieprawidłowa opcja.")
