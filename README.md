# Auto Tracker Link Generator 📦

A compact Python tool for everyday use that quickly generates tracking links and pre-formatted email notifications.

---

## 🚀 Key Features

* **Automatic Carrier Detection:** Detects the shipping carrier (e.g., UPS, DHL) based on the entered number format.
* **Keyboard Correction (QWERTY / QWERTZ):** Automatically corrects common typos (e.g., automatically converting `1Y...` to `1Z...` for UPS tracking numbers).
* **Clipboard integration:** Immediately copies the generated tracking link to the clipboard (`pyperclip`).
* **Email template:** Simultaneously creates a ready-to-use notification text for easy communication with customers and clients.
* **1-Click Launch:** Convenient launch by double-clicking `run.bat` or via a desktop shortcut.

---

## 📂 Project Structure

```text
├── tests/
│   └── test_tracker.py      # Unit tests for the Tracker class
├── main.py                  # Main program & interactive CLI loop
└── tracker.py               # Tracker class (logic for detection & link generation)

```

---

## 🛠️ Installation & Setup

1. Install **Python 3.x** on your system.
2. Download and unzip the project folder.
3. Install dependencies in the console or terminal:
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Usage

There are three different ways to run the program:

### 1. Via the console (default)
```bash
python main.py
```

### 2. By double-clicking (`run.bat`)
To run the program quickly without typing in the terminal, simply double-click the **`run.bat`** file in the project folder.

> **Tip for `run.bat`:**
> File contents, e.g.:
> ```bat
> @echo off
> python main.py
> pause
> ```

### 3. As a desktop shortcut (1-click launch)
1. Right-click the **`run.bat`** file → *Send To* → **Desktop (Create Shortcut)**.
2. (Optional) Rename the shortcut on the desktop (e.g., to `Tracking Link Generator`).
3. From now on, you can conveniently launch the script directly from the desktop by double-clicking it.

---

## 🧪 Testing

This project uses [pytest](https://docs.pytest.org/) for unit testing.

```bash
# Install dev dependencies
pip install pytest

# Run all tests
pytest

# Run with verbose output (shows each test individually)
pytest -v
```
