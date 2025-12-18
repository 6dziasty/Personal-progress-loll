
import os
import shutil


# Prosty interfejs wyboru folderu do sortowania
def wybierz_folder():
    print("Wybierz folder do sortowania:")
    print("1. Pobrane")
    print("2. Dokumenty")
    print("3. Własna ścieżka")
    wybor = input("Twój wybór (1/2/3): ")
    if wybor == "1":
        return os.path.join(os.path.expanduser("~"), "Pobrane")
    elif wybor == "2":
        return os.path.join(os.path.expanduser("~"), "Dokumenty")
    elif wybor == "3":
        return input("Podaj pełną ścieżkę do folderu: ")
    else:
        print("Nieprawidłowy wybór, domyślnie: Pobrane")
        return os.path.join(os.path.expanduser("~"), "Pobrane")

sciezka_pobrane = wybierz_folder()

# Mapowanie rozszerzeń na foldery docelowe
typy_foldery = {
    ".jpg": "Zdjęcia",
    ".jpeg": "Zdjęcia",
    ".png": "Zdjęcia",
    ".gif": "Zdjęcia",
    ".bmp": "Zdjęcia",
    ".mp3": "Muzyka",
    ".wav": "Muzyka",
    ".flac": "Muzyka",
    ".mp4": "Filmy",
    ".avi": "Filmy",
    ".mov": "Filmy",
    ".pdf": "Dokumenty",
    ".doc": "Dokumenty",
    ".docx": "Dokumenty",
    ".txt": "Dokumenty",
    ".zip": "Archiwa",
    ".rar": "Archiwa",
    ".7z": "Archiwa",
    # Dodaj inne rozszerzenia według potrzeb
}


def sortuj_plik(plik, statystyka):
    _, ext = os.path.splitext(plik)
    ext = ext.lower()
    if ext in typy_foldery:
        folder_docelowy = os.path.join(sciezka_pobrane, typy_foldery[ext])
        if not os.path.exists(folder_docelowy):
            os.makedirs(folder_docelowy)
        shutil.move(os.path.join(sciezka_pobrane, plik), os.path.join(folder_docelowy, plik))
        print(f"Przeniesiono {plik} do {typy_foldery[ext]}")
        statystyka[typy_foldery[ext]] = statystyka.get(typy_foldery[ext], 0) + 1
    else:
        folder_docelowy = os.path.join(sciezka_pobrane, "Inne")
        if not os.path.exists(folder_docelowy):
            os.makedirs(folder_docelowy)
        shutil.move(os.path.join(sciezka_pobrane, plik), os.path.join(folder_docelowy, plik))
        print(f"Przeniesiono {plik} do Inne")
        statystyka["Inne"] = statystyka.get("Inne", 0) + 1


def main():
    statystyka = {}
    for plik in os.listdir(sciezka_pobrane):
        sciezka = os.path.join(sciezka_pobrane, plik)
        if os.path.isfile(sciezka):
            sortuj_plik(plik, statystyka)
    print("\nPodsumowanie:")
    for folder, liczba in statystyka.items():
        print(f"{folder}: {liczba} plików")

if __name__ == "__main__":
    main()
