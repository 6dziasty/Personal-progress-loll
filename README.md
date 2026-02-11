# 🚀 Progress log - 6dziasty!!!!

## Cel❗❗❗
Chcę dokumentować mój progres na temat informatyki i związanymi z nią rzeczami. Robię to, aby w przyszłości móc dać to w CV kiedyś albo komuś pokazać. Może to, co tu będę opisywał, przyda się komuś!

---

## 📚 Moja Nauka (Szkola)
Wszystkie moje notatki z lekcji zawodowych, zadania i projekty znajdziesz w moim głównym repozytorium szkolnym:
👉 [**Repozytorium SZKOŁA**](https://github.com/6dziasty/Szkola)

---

# 📖 Wpisy

### **29.11.25** - Podsumowanie podłączenia Access Pointa (AP) do mojej sieci  
**Cel**
- Wyeliminowanie "blind spotów" w moim pokoju i dodatkowo ulepszenie przesyłu na piętrze.

**Przebieg**
- Znalazłem w garażu stary ruter Huawei B525s-23a. Jest w miarę spoko i do spełniania funkcji jako AP sprawdza się idealnie. Posiada 2.4 GHz i 5 GHz, co daje duży plus, bo zasięg 2.4 jest wystarczający na całe piętro.
- Ostatecznie AP jest podłączony do głównego rutera przez kabel sieciowy.

**Problemy!**
- W sumie to problem jedyny był z samym wejściem w konfigurację rutera i pingowaniem go. Samym problemem był wadliwy kabel RJ-45, który wymieniłem na inny jakie miałem.
- Tymczasowy problem to brak tego "dzyndzla" od kabla i jest na razie przyklejony na taśmę izolacyjną, co wygląda śmiesznie, ale jako rozwiązanie na razie wystarczy.
- AKTUALIZACJA- Kabel wymieniłem niedługo po wstawieniu tego wpisu na nowy.

--

### **19.11.25** - Konfiguracja Laptopa ThinkPad T510
**Przebieg**
- Kupiłem go za... nie powiem ile, ale można się spodziewać dużej ceny jak na taki stary sprzęt.
- Sam laptop posiada 2x 4GB RAM-u DDR3 i Intela i5 pierwszej generacji. Nie są to najlepsze dane, lecz nadaje się do podstawowych prac z programowaniem i zadań szkolnych.

**Problemy**
- Napotkałem tylko problem z samą słabą baterią, który rozwiążę kupieniem nowej baterii, przez co będę mógł ją wymienić.
- Laptop czasami wywalił "Blue Screen" – prawdopodobnie winowajcą jest [tutaj dopisz swoje podejrzenia, np. dysk lub sterowniki].

--

### **??.01.26** - Wielka modernizacja sieci: Funbox 3.0 + Switch + Archer A6
**Cel**
- Rozwiązanie problemu "martwej strefy" na dole u kolegi przy zachowaniu pełnej prędkości światłowodu (300 Mb/s+) na jednym kablu w ścianie.

**Przebieg**
- Początkowo walczyłem ze starym Huawei B315, ale to był "syf" – porty 100 Mb/s i brak pasma 5 GHz ucinały neta do marnych 50 mega. 
- Zapadła męska decyzja: zakup **TP-Link Archer A6 (AC1200)** za 150 zł. To był strzał w dziesiątkę ze względu na porty Gigabitowe.
- Przebudowałem całą strukturę: Funbox 3.0 wylądował na górze przy skrzynce (jako główny router/mózg), stamtąd sygnał leci na **Switch Mercusys**, a potem jednym kablem w ścianie na dół do Archera.
- Archer został skonfigurowany w dedykowanym trybie **Access Point (AP Mode)**.

**Problemy!**
- **Konflikt IP i błąd 169.254:** Urządzenia wariowały, bo dwa routery próbowały nadawać własne adresy (DHCP). Rozwiązane przez wyłączenie DHCP na dole i zrobienie z Archera "przezroczystej anteny".
- **Ograniczenia sprzętowe:** Stary Huawei kompletnie nie radził sobie z routingiem sygnału ze światłowodu i blokował dostęp do sieci.
- **Logistyka kablowa:** Brak możliwości przeciągnięcia drugiego kabla zmusił mnie do kombinowania z topologią, aby wszystko obsłużyć na jednej nitce LAN.

**Rozwiązanie**
- Zmiana "szefa" sieci na Funboxa przy ONT i ustawienie Archera A6 jako AP. Teraz kumpel ma pełne 300 Mb/s po WiFi na dole i dodatkowe porty LAN pod TV i konsolę. System śmiga stabilnie, a błąd 169.254 zniknął na zawsze.

--

### **27.01.26** - Batalia o Lenovo IdeaPad: Od "hakingu" po Windows 10 Max Performance
**Cel**
- Próba odzyskania dostępu do zablokowanego konta ze zdjęciami oraz testy stabilności Linux Mint na starym hardware.

**Przebieg**
- **Operacja "Backdoor":** Wykorzystałem pendrive z instalatorem Windows 10, aby przez wiersz poleceń (CMD) uzyskać dostęp administracyjny przed ekranem logowania. 
- Utworzyłem drugie konto administratora, próbując "przebić się" do danych na koncie nr 1, ale stary system był zbyt powolny i zaśmiecony, by
umożliwić sprawną pracę.
- Podjąłem próbę instalacji Linux Mint Cinnamon, aby tchnąć nowe życie w laptopa.
- W trakcie instalacji komputer całkowicie się zawiesił ("freeze"). Po twardym resecie sektor rozruchowy został uszkodzony – system Windows przestał startować, a laptop zaczął sypać błędami przy próbie bootowania z USB.
- Zgodnie z radą cioci, zrezygnowałem z dalszych prób odzyskiwania plików i przeprowadziłem czystą instalację Windows 10, optymalizując go pod kątem wydajności.

**Problemy!**
- **Błędy bootowania:** System rzucał komunikatami `failed to open \EFI\BOOT\mmx64.efi - Not Found` oraz `shim_lock protocol not found` przy próbie startu z pendrive.
- **Konflikt formatów:** Pendrive przygotowany w Rufusie miał ustawiony schemat partycjonowania MBR, co gryzło się z wymaganiami UEFI starego IdeaPada.
- **Brak miejsca:** Partycja rozruchowa (ESP) na pendrive miała zaledwie 5 MB, co uniemożliwiło ręczne dorzucenie brakujących plików rozruchowych.

**Rozwiązanie**
- Całkowity format dysku i nowa instalacja Windows 10 w trybie GPT/UEFI.
- Skonfigurowanie systemu w trybie "Max Performance" – wyłączyłem zbędne efekty wizualne i procesy w tle, aby wycisnąć maksimum z i5 pierwszej generacji.
- **Efekt:** Laptop działa płynnie, ciocia może bez problemów obsługiwać pocztę i grać w pasjansa. Wszystkie "blind spoty" systemowe zostały wyeliminowane.


---

## 🛠️ Co planuję zrobić? (To-Do)

- [ ] **Serwer na Ubuntu Server** 🖥️
  - Chcę go postawić na moim starym komputerze.
  - **Plan:** Muszę dokupić dysk i dodatkowe wiatraki, bo na razie jest tylko ten od procesora, co przy serwerze może nie starczyć. Postawiłbym na nim prawdopodobnie serwer plików oparty na programie "Samba", a póżniej rozwinąć to do dysku w chmurze który bedzie dostępny z mojego telefonu i innych urządzeń.
- [ ] **Kolejny Access Point** 📶
  - Planuję dodać jeszcze jeden AP, żeby kompletnie wyeliminować wszystkie "blind spoty" w całym domu.
- [ ] **Nowa bateria do ThinkPada** 🔋
  - Żeby sprzęt był w 100% sprawny i mobilny.

---
*Repozytorium stworzone przez 6dziasty*
