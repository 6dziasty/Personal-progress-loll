import requests

sites = [
    "https://twitter.com/{nickname}",
    "https://instagram.com/{nickname}",
    "https://github.com/{nickname}",
    "https://www.reddit.com/user/{nickname}",
    "https://www.linkedin.com/in/{imie}-{nazwisko}/",
    "https://www.tiktok.com/@{nickname}",
    "https://www.pinterest.com/{nickname}/",
    "https://steamcommunity.com/id/{nickname}/",
    "https://soundcloud.com/{nickname}",
    "https://www.twitch.tv/{nickname}",
    "https://www.roblox.com/users/{nickname}/profile",
    "https://www.youtube.com/{nickname}",
    "https://www.youtube.com/c/{nickname}",
    "https://www.youtube.com/user/{nickname}",


    "https://www.facebook.com/{nickname}",
    "https://facebook.com/{nickname}",
    "https://www.facebook.com/profile.php?id={nickname}",
    "https://www.facebook.com/{imie}.{nazwisko}",
    "https://facebook.com/{imie}.{nazwisko}",
]

def get_input(prompt, allow_empty=False, validator=None):
    while True:
        value = input(prompt)
        if not value and not allow_empty:
            print("Pole nie może być puste!")
            continue
        if validator and not validator(value):
            print("Nieprawidłowa wartość!")
            continue
        return value

def simple_nickname(nick):
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-"
    return 3 <= len(nick) <= 30 and all(c in allowed for c in nick)

def simple_name(name):
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZżźćńółęąśŻŹĆĄŚĘŁÓŃ-"
    return 2 <= len(name) <= 30 and all(c in allowed for c in name)

imie = get_input("Podaj imię: ", validator=simple_name)
nazwisko = get_input("Podaj nazwisko: ", validator=simple_name)
nickname = get_input("Podaj nickname: ", validator=simple_nickname)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

znalezione = []
brak = []
bledy = []
przekierowania = []

for site in sites:
    url = site.format(imie=imie, nazwisko=nazwisko, nickname=nickname)
    try:
        response = requests.get(url, timeout=10, allow_redirects=True, headers=headers)
        if response.history:
            print(f"[PRZEKIEROWANIE] {url} -> {response.url}")
            przekierowania.append((url, response.url))
        if response.status_code == 200:
            print(f"[ZNALEZIONO] {url} (status: 200)")
            znalezione.append(url)
        elif response.status_code == 404:
            print(f"[BRAK] {url} (status: 404)")
            brak.append(url)
        elif response.status_code in (301, 302):
            print(f"[PRZEKIEROWANIE] {url} (status: {response.status_code})")
            przekierowania.append((url, response.headers.get('Location', 'nieznany')))
        elif response.status_code == 403:
            print(f"[ZABLOKOWANO/PRYWATNE] {url} (status: 403)")
            bledy.append(url)
        else:
            print(f"[INNY STATUS {response.status_code}] {url}")
            bledy.append(url)
    except requests.RequestException as e:
        print(f"[BŁĄD] {url} ({e})")
        bledy.append(url)

print("\n--- PODSUMOWANIE ---")
print(f"Znalezione: {len(znalezione)}")
print(f"Brak: {len(brak)}")
print(f"Błędy: {len(bledy)}")
print(f"Przekierowania: {len(przekierowania)}")
if znalezione:
    print("\nLista znalezionych profili:")
    for url in znalezione:
        print(url)