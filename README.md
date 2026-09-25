# Auto Tracker Link Generator 📦

A compact Python CLI tool for everyday use that quickly generates tracking links and pre-formatted email notifications from a shipping tracking number — and optionally opens the text directly in a new Outlook mail.

---

## 🚀 Key Features

* **Automatic Carrier Detection:** Detects the shipping carrier (UPS, DHL) based on the tracking number's prefix.
* **Keyboard Correction (QWERTY / QWERTZ):** Automatically corrects a common typo where `1Y...` is entered instead of `1Z...` for UPS tracking numbers.
* **Clipboard integration:** Copies the generated tracking link / email text straight to the clipboard (`pyperclip`).
* **Email template:** Produces a ready-to-use customer notification text.
* **Outlook integration (optional):** Opens the generated text in a new Outlook mail, pre-selecting the correct sender account (`--email`, Windows + Outlook only).
* **Config-driven:** Carriers, prefixes, URLs and the email template live in `config.json` — no code changes needed to add a carrier.
* **Configurable logging:** `--verbose` enables debug output.

---

## 📂 Project Structure

```text
cleanerTrackingLinks/
├── main.py              # CLI entry point (argparse) & interactive loop
├── tracker.py          # Tracker class: carrier detection & link/email generation
├── email_notifier.py   # Optional Outlook integration via pywin32 (COM)
├── config.json         # Carriers, prefixes, URLs, email template
├── .env.example        # Template for your local .env (sender address)
├── requirements.txt    # Dependencies
├── run.bat             # 1-click launch (interactive mode)
├── tests/
│   └── test_tracker.py # Unit tests for the Tracker class
├── README.md
└── LICENSE
```

---

## 🛠️ Installation & Setup

1. Install **Python 3.x**.
2. Clone the repository and enter the folder.
3. (Recommended) create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. (Only for `--email` / Outlook) create a `.env` file from the template and set your sender address:
   ```bash
   copy .env.example .env        # Windows
   ```
   ```ini
   # .env
   SEND_FROM_EMAIL=your-email@example.com
   ```

> **Note:** The Outlook integration (`--email`) relies on `pywin32` and a local Outlook installation, so it only works on **Windows**. The core link/email generation works on any platform.

---

## 💻 Usage

### Interactive mode (default)
```bash
python main.py
```
Enter tracking numbers one after another. Type `x`, `exit` or `quit` to close.

### Single-shot mode
```bash
python main.py 1Z999AA10123456784
```

### CLI flags

| Flag | Short | Description |
|------|-------|-------------|
| `--interactive` | `-i` | Force interactive loop (even if a number is passed) |
| `--link-only`   | `-l` | Output only the tracking link, without the email text |
| `--email`       | `-e` | Open the generated text in a new Outlook mail (Windows only) |
| `--verbose`     | `-v` | Enable debug logging |

### Examples
```bash
python main.py 1Z999AA10123456784            # email text → clipboard
python main.py 1Z999AA10123456784 -l         # link only → clipboard
python main.py 1Z999AA10123456784 -e         # email text → new Outlook mail
python main.py -i -v                          # interactive loop + debug output
```

### 1-Click launch (`run.bat`)
Double-click **`run.bat`** to start the interactive mode without opening a terminal. You can also create a desktop shortcut: right-click `run.bat` → *Send To* → *Desktop (Create Shortcut)*.

---

## ⚙️ Configuration

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
    "email_template": "Dear Team, ... 👉 {} ..."
}
```

To **add a carrier**, add a new entry with its `prefixes` and a `url` containing `{}` as the placeholder for the tracking number. No code changes required.

---

## 🧪 Testing

This project uses [pytest](https://docs.pytest.org/) for unit testing.

```bash
# Run all tests
pytest

# Verbose output (shows each test individually)
pytest -v
```

---

## 📄 License

See [LICENSE](LICENSE).
