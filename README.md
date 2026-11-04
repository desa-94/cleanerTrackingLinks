# Tracking-Link Generator 📦

Ein kleines Kommandozeilen-Tool, das ich für meine tägliche Arbeit im Versand geschrieben habe.

Wir verschicken Kundensendungen per **UPS** oder **DHL Express**. Nach der Buchung bekommen wir die Sendungsnummer in unserem internen Tool angezeigt. Aus dieser Nummer muss dann eine Kunden-E-Mail mit dem passenden Tracking-Link entstehen. Genau diesen Schritt nimmt mir das Tool ab: Nummer rein, fertiger E-Mail-Text liegt in der Zwischenablage – einfügen und absenden.

---

## Warum das Tool? (Der Zeitgewinn)

Vorher lief das bei jeder einzelnen Sendung so ab:

1. Sendungsnummer aus dem Buchungstool kopieren
2. Überlegen, ob es UPS oder DHL ist
3. Die richtige Tracking-Seite aufrufen bzw. den Link von Hand zusammenbauen
4. Eine neue E-Mail öffnen
5. Den Benachrichtigungstext tippen
6. Nummer und Link einsetzen

Das sind pro Sendung schnell **1–2 Minuten** – und dabei schleichen sich Flüchtigkeitsfehler ein (klassisch: auf der deutschen QWERTZ-Tastatur wird aus `1Z…` versehentlich `1Y…`).

Mit dem Tool bleibt davon übrig:

1. Sendungsnummer eingeben
2. Fertigen Text aus der Zwischenablage einfügen

Das dauert **ein paar Sekunden**. Bei zum Beispiel 30 Sendungen am Tag spare ich damit rund **30–45 Minuten täglich** – und der Text sieht jedes Mal gleich sauber aus.

| | Vorher (manuell) | Mit Tool |
|---|---|---|
| Pro Sendung | ca. 1–2 Min | wenige Sekunden |
| 30 Sendungen/Tag | ~45–60 Min | ~5 Min |
| Tippfehler bei der Nummer | passiert | wird automatisch korrigiert |

---

## Was es kann

- **Carrier automatisch erkennen** – anhand des Nummern-Präfixes wird UPS oder DHL erkannt, ich muss das nicht mehr auswählen.
- **Tippfehler korrigieren** – das häufige QWERTZ-Problem (`1Y…` statt `1Z…`) wird automatisch zu `1Z…` umgedreht.
- **Fertiger E-Mail-Text** – der Tracking-Link wird in eine fertige Kunden-E-Mail eingebaut.
- **Direkt in der Zwischenablage** – das Ergebnis landet sofort in der Zwischenablage, ich muss es nur noch einfügen.
- **Über Datei konfigurierbar** – Carrier, Präfixe, Links und der E-Mail-Text stehen in `config.json`. Einen neuen Carrier füge ich dort hinzu, ohne Code anzufassen.

---

## Nutzung im Alltag

Ich starte das Tool über eine Verknüpfung auf dem Desktop, die auf `run.bat` zeigt. Das öffnet direkt den interaktiven Modus:

```
=== Tracking-Link Generator ===
Tracking-Number: 1Z999AA10123456784
Copied to the clipboard.
Tracking-Number:
```

Nummer eingeben, Enter, Text ist in der Zwischenablage. Mit `x`, `exit` oder `quit` beende ich das Tool.

### Weitere Aufrufvarianten

```bash
python main.py                      # interaktiver Modus (Standard)
python main.py 1Z999AA10123456784   # einmalig eine Nummer verarbeiten
python main.py 1Z999AA10123456784 -l  # nur den Link, ohne E-Mail-Text
python main.py -i -v                # interaktiv + Debug-Ausgaben
```

| Flag | Kurz | Bedeutung |
|------|------|-----------|
| `--interactive` | `-i` | Interaktiven Modus erzwingen |
| `--link-only`   | `-l` | Nur den Tracking-Link ausgeben |
| `--verbose`     | `-v` | Debug-Ausgaben einschalten |

---

## Installation

```bash
# Repository klonen und hineinwechseln
python -m venv .venv
.venv\Scripts\activate          # Windows

pip install -r requirements.txt
```

Danach `python main.py` starten – oder `run.bat` doppelklicken.

---

## Konfiguration

Die ganze Carrier-Logik steckt in `config.json`:

```json
{
    "carriers": {
        "UPS": {
            "prefixes": ["1Z"],
            "url": "https://www.ups.com/track?tracknum={}&loc=de_DE"
        },
        "DHL": {
            "prefixes": ["JD", "JJ", "0034"],
            "url": "https://www.dhl.de/.../verfolgen.html?piececode={}"
        }
    },
    "email_template": "Dear Team, ... 👉 {} ..."
}
```

Ein neuer Carrier braucht nur einen Eintrag mit seinen `prefixes` und einer `url`, in der `{}` als Platzhalter für die Nummer steht. Kein Eingriff in den Code nötig.

---

## Projektstruktur

```text
cleanerTrackingLinks/
├── main.py           # Einstiegspunkt: CLI (argparse) & interaktive Schleife
├── tracker.py        # Tracker-Klasse: Carrier-Erkennung & Link-/E-Mail-Aufbau
├── config.json       # Carrier, Präfixe, Links, E-Mail-Vorlage
├── requirements.txt  # Abhängigkeiten
├── run.bat           # 1-Klick-Start (interaktiver Modus)
├── tests/
│   └── test_tracker.py
├── README.md
└── LICENSE
```

---

## Tests

Die Logik der `Tracker`-Klasse ist mit [pytest](https://docs.pytest.org/) abgedeckt:

```bash
pytest        # alle Tests
pytest -v     # ausführlich
```

---

## Lizenz

Siehe [LICENSE](LICENSE).
