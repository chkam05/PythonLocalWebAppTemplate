# PythonLocalWebAppTemplate

## Jezyki

- [English](README.md)
- [Polski](README_pl-PL.md)

---

Szablon lokalnej aplikacji webowej w Pythonie, ktora uruchamia backend Flask na komputerze uzytkownika i wyswietla interfejs w natywnym oknie desktopowym przez PyWebView.

![Zrzut ekranu aplikacji](doc/screenshot.png)

## Co robi aplikacja

Aplikacja startuje lokalny serwer HTTP pod adresem `127.0.0.1:5000`, renderuje widok HTML z katalogu `templates`, udostepnia zasoby statyczne z katalogu `assets`, a nastepnie otwiera ten adres w oknie WebView. Dzieki temu projekt zachowuje wygode tworzenia aplikacji webowej, ale dziala jak prosta aplikacja desktopowa dla macOS, Windows i Linux.

Aktualny widok startowy prezentuje informacje o aplikacji: nazwe, wersje, autora i lokalny adres uslugi. Projekt zawiera tez gotowy mechanizm zapisu ustawien okna, w tym szerokosci, wysokosci oraz pozycji na ekranie.

## Po co zostala stworzona

Projekt jest baza startowa do budowania lokalnych narzedzi desktopowych z webowym interfejsem. Ma zdejmowac z aplikacji powtarzalna infrastrukture: uruchamianie lokalnego backendu, wybieranie backendu WebView, przechowywanie ustawien, organizacje kontrolerow, modeli i storage oraz pakowanie aplikacji do dystrybucji.

## Kluczowe funkcje

- Lokalny backend Flask uruchamiany w osobnym watku.
- Natywne okno aplikacji tworzone przez PyWebView.
- Automatyczny wybor backendu WebView dla macOS, Windows i Linux.
- Walidacja dostepnosci runtime WebView na Windows i Linux.
- Szablon HTML renderowany przez Jinja2.
- Statyczne zasoby aplikacji w katalogu `assets`.
- Kontrolery HTTP oparte o Flask Blueprint.
- Endpointy `GET /settings` i `POST /settings` do odczytu oraz zapisu ustawien.
- Thread-safe storage JSON z cache, atomowym zapisem i domyslna inicjalizacja danych.
- Zapamietywanie rozmiaru i pozycji okna po zamknieciu aplikacji.
- Skrypt budujacy aplikacje przez PyInstaller i tworzacy paczke release dla aktualnego systemu.

## Wersja Pythona

Projekt zostal sprawdzony lokalnie na:

```text
Python 3.13.14
```

Skrypty uruchomieniowe korzystaja z interpretera z `.venv`, jesli istnieje. W przeciwnym razie uzywaja `python3` na macOS/Linux albo `python` na Windows.

## Technologie

- Python 3.13.14
- Flask 3.1.3
- Jinja2 3.1.6
- Werkzeug 3.1.8
- pywebview 6.2.1
- PyInstaller 6.20.0
- Pillow, uzywany przy procesie builda
- HTML i CSS dla warstwy UI
- JSON jako format lokalnych ustawien

Pelna lista zaleznosci znajduje sie w pliku `requirements.txt`.

## Struktura plikow

```text
.
|-- app.py                         # Glowny punkt wejscia aplikacji
|-- config.py                      # Konfiguracja runtime aplikacji
|-- build.py                       # Skrypt czyszczenia, instalacji zaleznosci, builda i release
|-- build_conf.py                  # Konfiguracja procesu builda
|-- requirements.txt               # Zaleznosci Pythona
|-- run.sh / run.bat               # Uruchomienie aplikacji lokalnie
|-- build.sh / build.bat           # Uruchomienie procesu builda
|-- cleanup.sh / cleanup.bat       # Usuniecie katalogow __pycache__
|-- assets/
|   |-- icons/                     # Ikony aplikacji
|   `-- index/index.css            # Style widoku startowego
|-- templates/
|   `-- index/index.html           # Szablon glownego widoku
|-- controllers/
|   |-- window_controller.py       # Trasa / i renderowanie UI
|   `-- settings_controller.py     # Endpointy /settings
|-- core/
|   |-- api/base_controller.py     # Bazowy kontroler Flask Blueprint
|   |-- models/                    # Modele danych i serializacja
|   |-- storage/                   # Storage JSON i ustawienia aplikacji
|   `-- service.py                 # Lokalny serwer Flask
|-- utils/
|   |-- path_utils.py              # Sciezki ustawien zalezne od systemu
|   `-- webview_runtime.py         # Dobor i walidacja runtime WebView
`-- doc/
    `-- screenshot.png             # Zrzut ekranu aplikacji uzyty w README
```

## Skrypty

### Uruchomienie aplikacji

macOS/Linux:

```sh
./run.sh
```

Windows:

```bat
run.bat
```

Skrypt przechodzi do katalogu projektu, wybiera lokalne `.venv`, jesli istnieje, i uruchamia `app.py`.

### Build aplikacji

macOS/Linux:

```sh
./build.sh
```

Windows:

```bat
build.bat
```

Skrypty uruchamiaja `build.py`. Proces builda wykonuje kolejno:

1. Usuniecie katalogow `bin/dist`, `bin/build`, `bin/release` oraz wygenerowanych plikow pomocniczych.
2. Aktualizacje `pip`.
3. Instalacje zaleznosci z `requirements.txt`.
4. Instalacje narzedzi buildowych `pyinstaller` i `pillow`.
5. Zbudowanie aplikacji przez PyInstaller dla aktualnego systemu operacyjnego.
6. Dodanie metadanych aplikacji i spakowanie wyniku do katalogu `bin/release`.

Wyniki builda trafiaja do:

- `bin/dist` - wygenerowana aplikacja.
- `bin/build` - pliki robocze PyInstaller.
- `bin/release` - gotowe archiwum release i plik `APP_METADATA.txt`.

### Czyszczenie cache Pythona

macOS/Linux:

```sh
./cleanup.sh
```

Windows:

```bat
cleanup.bat
```

Skrypty usuwaja katalogi `__pycache__` w projekcie.

## Parametry konfiguracyjne aplikacji

Konfiguracja runtime znajduje sie w `config.py`.

| Parametr | Znaczenie | Wartosc domyslna |
| --- | --- | --- |
| `APP_NAME` | Nazwa aplikacji i tytul okna | `Python Local WebApp Template` |
| `APP_AUTHOR` | Autor aplikacji | `Kamil Karpinski` |
| `APP_DESCRIPTION` | Opis aplikacji uzywany rowniez przy buildzie | Szablon lokalnej aplikacji webowej |
| `APP_VERSION` | Wersja aplikacji | `1.0.0.0` |
| `HOST` | Host lokalnego serwera Flask | `127.0.0.1` |
| `PORT` | Port lokalnego serwera Flask | `5000` |
| `SERVICE_TIMEOUT` | Maksymalny czas oczekiwania na start serwera | `10` sekund |
| `STATIC_FOLDER` | Katalog zasobow statycznych | `assets` |
| `STATIC_URL_PATH` | Publiczna sciezka zasobow statycznych | `/assets` |
| `TEMPLATE_FOLDER` | Katalog szablonow HTML | `templates` |
| `APP_ICON` | Ikona PNG uzywana m.in. poza Windows | `assets/icons/favicon.png` |
| `APP_ICON_WINDOWS` | Ikona ICO dla Windows | `assets/icons/favicon.ico` |
| `SETTINGS_DIR` | Systemowy katalog ustawien aplikacji | Wyliczany przez `PathUtils` |
| `SETTINGS_FILE_NAME` | Nazwa pliku ustawien | `settings.json` |

Ustawienia uzytkownika sa przechowywane w systemowym katalogu konfiguracji:

- Windows: `%APPDATA%/<APP_NAME bez spacji>`
- macOS: `~/Library/Application Support/<APP_NAME bez spacji>`
- Linux: `$XDG_CONFIG_HOME/<APP_NAME bez spacji>` albo `~/.config/<APP_NAME bez spacji>`

Domyslne ustawienia okna sa zdefiniowane w `core/models/settings_data_model.py`:

| Parametr | Wartosc domyslna |
| --- | --- |
| `window_width` | `1200` |
| `window_height` | `800` |
| `window_pos_x` | `100` |
| `window_pos_y` | `100` |

## Parametry builda

Konfiguracja builda znajduje sie w `build_conf.py`.

| Parametr | Znaczenie | Wartosc domyslna |
| --- | --- | --- |
| `ROOT_DIR` | Katalog glowny projektu | Katalog z `build_conf.py` |
| `BIN_DIR` | Katalog plikow builda | `bin` |
| `BUILD_DIR` | Katalog roboczy PyInstaller | `bin/build` |
| `DIST_DIR` | Katalog wynikowy PyInstaller | `bin/dist` |
| `RELEASE_DIR` | Katalog paczek release | `bin/release` |
| `BUILD_FOLDERS` | Katalogi dolaczane do aplikacji przez `--add-data` | `assets`, `templates` |
| `ENTRY_FILE` | Punkt wejscia aplikacji dla PyInstaller | `app.py` |
| `RELEASE_METADATA_FILE` | Nazwa pliku z metadanymi release | `APP_METADATA.txt` |
| `WINDOWS_VERSION_FILE` | Generowany plik metadanych wersji Windows | `bin/version_info.txt` |
| `MACOS_APP_NAME` | Techniczna nazwa aplikacji macOS | `python-local-webapp-template` |
| `MACOS_BUNDLE_IDENTIFIER` | Identyfikator bundle macOS | `com.example.python-local-webapp-template` |
| `MACOS_CATEGORY_TYPE` | Kategoria aplikacji macOS | `public.app-category.developer-tools` |

Build korzysta z metadanych aplikacji importowanych z `config.py`, takich jak `APP_NAME`, `APP_AUTHOR`, `APP_DESCRIPTION`, `APP_VERSION` oraz ikony PNG/ICO.

PyInstaller jest uruchamiany w trybie:

- `--windowed` - bez konsoli systemowej.
- `--onedir` - aplikacja jako katalog z plikami.
- `--clean` i `--noconfirm` - czysty build bez pytan interaktywnych.
- `--add-data` dla katalogow z `BUILD_FOLDERS`.

Paczki release sa tworzone zalezne od systemu:

- Windows: archiwum ZIP z katalogu `bin/dist/<APP_NAME>`.
- macOS: archiwum ZIP z aplikacja `.app`, tworzone przez `ditto`.
- Linux: archiwum `tar.gz` z katalogu `bin/dist/<APP_NAME>`.

## Endpointy

| Metoda | Sciezka | Opis |
| --- | --- | --- |
| `GET` | `/` | Renderuje glowny widok aplikacji. |
| `GET` | `/settings` | Zwraca ustawienia okna jako JSON. |
| `POST` | `/settings` | Zapisuje ustawienia okna z payloadu JSON. |

Przy zamykaniu okna aplikacja zapisuje aktualny rozmiar i pozycje, a po kolejnym uruchomieniu odtwarza je z pliku `settings.json`.
