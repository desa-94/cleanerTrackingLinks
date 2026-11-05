# Tracking-Link Generator 📦

A small command-line tool I built for my daily work in the mailroom.

We ship ready-to-send parcels on behalf of our customers — per order either via **UPS** or **DHL Express**, never mixed. After booking, the tracking number(s) show up in our internal tool, and a short customer email with the matching tracking links has to go out. This tool takes over that last part: copy the numbers, press Enter, and the finished email text is on the clipboard — ready to paste and send.

---

## Why I built it

For every parcel the routine used to be:

1. Copy the tracking number from the booking tool
2. Figure out whether it's UPS or DHL
3. Open the right tracking page or assemble the link by hand
4. Type the notification text
5. Paste in the number and the link

That's easily **1–2 minutes per parcel** — plus the occasional slip (a classic on a German QWERTZ keyboard: `1Z…` turns into `1Y…`).

With the tool it comes down to: copy the number(s), press Enter, paste the finished text. A few seconds — whether it's one parcel or five.

| | Before (manual) | With the tool |
|---|---|---|
| Per parcel | ~1–2 min | a few seconds |
| ~30 parcels/day | ~45–60 min | ~5 min |
| Several parcels, one customer | each link by hand | all links in one text |
| Typo in the number | happens | auto-corrected |

Rough estimate: around **30–45 minutes saved per day**, and the wording comes out clean and consistent every time.

---

## What it does

- **Watches the clipboard.** Start the tool, then just copy tracking numbers — each one is picked up automatically until you press Enter.
- **Combines multiple numbers into one email.** Several parcels for the same customer? All their links end up in a single text.
- **Detects the carrier** from the number's prefix (UPS or DHL) — no manual picking.
- **Keeps you from mixing carriers.** Since we never mix UPS and DHL, it locks onto the first carrier and skips (with a warning) any stray number from the other one.
- **Flags duplicates.** Copy the same number twice and it shows `(already copied)` instead of adding it again.
- **Fixes the QWERTZ typo** (`1Y…` → `1Z…`) automatically.
- **Configurable via file.** Carriers, prefixes, URLs and the email text live in `config.json` — adding a carrier needs no code change.

---

## Everyday use

I launch it from a desktop shortcut pointing at `run.bat`, which opens the default **watch mode**:

```
=== Tracking-Link Generator (Watch Mode) ===

Waiting for tracking numbers... (Enter = done)
Tracking number detected -> 1Z999AA10123456784   (1 collected)
Tracking number detected -> 1Z999AA10123456785   (2 collected)
Tracking number detected -> 1Z999AA10123456784   (already copied)

2 tracking number(s) combined and copied to the clipboard.

Waiting for tracking numbers... (Enter = done)
```

Flow: start the tool → in the booking tool, double-click a number and Ctrl+C → press Enter → the finished text is on your clipboard. It then waits for the next customer. Type `x` + Enter to quit.

### Other modes

For edge cases there's also a manual and a one-shot mode:

```bash
python main.py                       # watch mode (default)
python main.py -i                    # interactive: type numbers by hand
python main.py 1Z999AA10123456784    # process a single number once
python main.py 1Z999AA10123456784 -l # link only, no email text
```

| Flag | Short | Description |
|------|-------|-------------|
| `--interactive` | `-i` | Type numbers by hand instead of watching the clipboard |
| `--link-only`   | `-l` | Output just the tracking link(s), no email text |
| `--verbose`     | `-v` | Enable debug logging |

---

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

Then run `python main.py` — or double-click `run.bat`.

---

## Configuration

All carrier logic lives in `config.json`:

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

- A new carrier just needs an entry with its `prefixes` and a `url` containing `{}` as the placeholder for the number.
- `email_template` uses `{links}` as the placeholder for the block of all links.
- `link_line` is the template for a single link line (`{link}`), repeated per number.

---

## Project structure

```text
cleanerTrackingLinks/
├── main.py           # Entry point: CLI (argparse), watch / interactive / one-shot modes
├── watcher.py        # ClipboardWatcher: watches the clipboard (threading)
├── tracker.py        # Tracker class: carrier detection & link/email building
├── config.json       # Carriers, prefixes, URLs, email template
├── requirements.txt
├── run.bat           # 1-click launch (watch mode)
├── tests/
│   └── test_tracker.py
├── README.md
└── LICENSE
```

---

## Tests

The `Tracker` logic is covered with [pytest](https://docs.pytest.org/):

```bash
pytest        # run all tests
pytest -v     # verbose
```

---

## License

See [LICENSE](LICENSE).
