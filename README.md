# Tracking-Link Generator 📦

Ein kleines Kommandozeilen-Tool, das ich für meine tägliche Arbeit im Versand geschrieben habe.

Wir (als Mailroom) verschicken für unsere Kunden versandfertige Sendungen – pro Vorgang entweder per **UPS** oder per **DHL Express**, nie gemischt. Nach der Buchung bekommen wir die Sendungsnummer(n) in unserem internen Buchungstool angezeigt. Aus diesen Nummern muss dann eine Kunden-E-Mail mit den passenden Tracking-Links entstehen. Genau das nimmt mir das Tool ab: Nummern kopieren, Enter drücken, fertiger E-Mail-Text liegt in der Zwischenablage – einfügen und absenden.

---

## Warum das Tool? (Der Zeitgewinn)

Vorher lief das bei jeder Sendung so ab:

1. Sendungsnummer aus dem Buchungstool kopieren
2. Überlegen, ob es UPS oder DHL ist
3. Die richtige Tracking-Seite aufrufen bzw. den Link von Hand zusammenbauen
4. Den Benachrichtigungstext tippen
5. Nummer und Link einsetzen

Das sind pro Sendung schnell **1–2 Minuten** – und dabei schleichen sich Flüchtigkeitsfehler ein (klassisch: auf der deutschen QWERTZ-Tastatur wird aus `1Z…` versehentlich `1Y…`).

Mit dem Tool bleibt davon übrig:

1. Nummer(n) kopieren (Doppelklick + Strg+C)
2. Enter drücken
3. Fertigen Text aus der Zwischenablage einfügen

Das dauert **ein paar Sekunden** – egal ob eine oder fünf Nummern. Bei zum Beispiel 30 Sendungen am Tag spare ich damit rund **30–45 Minuten täglich**, und der Text sieht jedes Mal gleich sauber aus.

| | Vorher (manuell) | Mit Tool |
|---|---|---|
| Pro Sendung | ca. 1–2 Min | wenige Sekunden |
| 30 Sendungen/Tag | ~45–60 Min | ~5 Min |
| Mehrere Pakete pro Kunde | jeder Link einzeln | alle Links in einem Text |
| Tippfehler bei der Nummer | passiert | wird automatisch korrigiert |

---

## Was es kann

- **Zwischenablage überwachen (Watch-Modus)** – das Tool lauscht auf die Zwischenablage. Jede kopierte Sendungsnummer wird automatisch erfasst, bis ich Enter drücke.
- **Mehrere Nummern → eine E-Mail** – bei mehreren Paketen für denselben Kunden landen alle Tracking-Links gesammelt in einem Text.
- **Carrier automatisch erkennen** – anhand des Nummern-Präfixes wird UPS oder DHL erkannt.
- **Carrier-Sicherheitsnetz** – da wir nie UPS und DHL mischen, merkt sich das Tool den Carrier der ersten Nummer und überspringt (mit Warnung) eine versehentlich dazwischengeratene Nummer des anderen Carriers.
- **Doppelt-kopiert-Hinweis** – kopiere ich dieselbe Nummer zweimal, zeigt das Tool „(wurde bereits kopiert)" an und nimmt sie nicht doppelt in den Text.
- **Tippfehler korrigieren** – das QWERTZ-Problem (`1Y…` statt `1Z…`) wird automatisch zu `1Z…` korrigiert.
- **Direkt in der Zwischenablage** – das fertige Ergebnis landet sofort in der Zwischenablage, ich muss es nur noch einfügen.
- **Über Datei konfigurierbar** – Carrier, Präfixe, Links und der E-Mail-Text stehen in `config.json`. Einen neuen Carrier füge ich dort hinzu, ohne Code anzufassen.

---

## Nutzung im Alltag

Ich starte das Tool über eine Verknüpfung auf dem Desktop, die auf `run.bat` zeigt. Das öffnet direkt den **Watch-Modus**:

```
=== Tracking-Link Generator (Watch Mode) ===

Warten auf Trackingnummern... (Enter = fertig)
Trackingnummer erkannt -> 1Z999AA10123456784   (1 gesammelt)
Trackingnummer erkannt -> 1Z999AA10123456785   (2 gesammelt)
Trackingnummer erkannt -> 1Z999AA10123456784   (wurde bereits kopiert)

2 Trackingnummer(n) zusammengefasst und in die Zwischenablage kopiert.

Warten auf Trackingnummern... (Enter = fertig)
```

Ablauf: Tool starten → Nummer(n) im Buchungstool mit Doppelklick markieren und Strg+C → Enter → der fertige Text liegt in der Zwischenablage. Danach wartet das Tool direkt auf den nächsten Kunden. Zum Beenden `x` + Enter.

### Weitere Aufrufvarianten

Für Sonderfälle gibt es daneben noch den manuellen und den Einmal-Modus:

```bash
python main.py                      # Watch-Modus (Standard)
python main.py -i                   # interaktiv: Nummern von Hand eintippen
python main.py 1Z999AA10123456784   # einmalig eine Nummer verarbeiten
python main.py 1Z999AA10123456784 -l  # nur den Link, ohne E-Mail-Text
python main.py -i -v                # interaktiv + Debug-Ausgaben
```

| Flag | Kurz | Bedeutung |
|------|------|-----------|
| `--interactive` | `-i` | Nummern von Hand eintippen statt Zwischenablage überwachen |
| `--link-only`   | `-l` | Nur den/die Tracking-Link(s) ausgeben, ohne E-Mail-Text |
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
    "email_template": "Dear Team, ... {links} ...",
    "link_line": "👉 {link}"
}
```

- Ein neuer Carrier braucht nur einen Eintrag mit seinen `prefixes` und einer `url`, in der `{}` als Platzhalter für die Nummer steht.
- `email_template` enthält `{links}` als Platzhalter für den Block aller Links.
- `link_line` ist die Vorlage für eine einzelne Link-Zeile (`{link}`). Bei mehreren Nummern wird sie je Nummer wiederholt.

Kein Eingriff in den Code nötig.

---

## Projektstruktur

```text
cleanerTrackingLinks/
├── main.py           # Einstiegspunkt: CLI (argparse), Watch-/Interaktiv-/Einmal-Modus
├── watcher.py        # ClipboardWatcher: überwacht die Zwischenablage (Threading)
├── tracker.py        # Tracker-Klasse: Carrier-Erkennung & Link-/E-Mail-Aufbau
├── config.json       # Carrier, Präfixe, Links, E-Mail-Vorlage
├── requirements.txt  # Abhängigkeiten
├── run.bat           # 1-Klick-Start (Watch-Modus)
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
