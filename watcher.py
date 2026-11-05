import logging
import threading

logger = logging.getLogger(__name__)

try:
    import pyperclip

    HAS_CLIPBOARD = True
except ImportError:
    HAS_CLIPBOARD = False


class ClipboardWatcher:
    """
    Watches the clipboard for tracking numbers while the main thread waits
    for the user to press Enter.

    Workflow per customer:
        1. Start watching -> prints "Waiting for tracking numbers..."
        2. Every copied value that looks like a tracking number is collected
           (duplicates are shown but not collected twice).
        3. The user presses Enter -> the watcher stops, the collected numbers
           are returned, and the main loop builds the email text.
    """

    def __init__(self, tracker, poll_interval: float = 0.5):
        self.tracker = tracker
        self.poll_interval = poll_interval
        self._collected = []  # tracking numbers kept for the email
        self._seen = set()  # everything already collected (for dedup)
        self._carrier = None  # locked to the first detected carrier
        self._stop = threading.Event()
        self._last_clipboard = ""
        self._last_written = None  # our own output, to ignore self-overwrite

    def _looks_like_tracking(self, text: str):
        """Return the cleaned tracking number if text looks like one, else None."""
        candidate = text.strip().upper()

        # Reject empty, multi-line or obviously-too-long clipboard content.
        if not candidate or "\n" in candidate or len(candidate) > 40:
            return None

        fixed = self.tracker.fix_UPS_keyboard_layout_error(candidate)
        if self.tracker.detect_carrier(fixed):
            return fixed
        return None

    def _poll_loop(self):
        while not self._stop.is_set():
            try:
                current = pyperclip.paste()
            except Exception as exc:
                logger.debug("Clipboard read failed: %s", exc)
                current = ""

            if current != self._last_clipboard:
                self._last_clipboard = current

                # Ignore the text we just wrote back ourselves.
                if current != self._last_written:
                    tn = self._looks_like_tracking(current)
                    if tn:
                        self._handle_number(tn)

            self._stop.wait(self.poll_interval)

    def _handle_number(self, tn: str):
        # Duplicate -> show it, but don't collect again.
        if tn in self._seen:
            print(f"Tracking number detected -> {tn}   (already copied)")
            return

        carrier = self.tracker.detect_carrier(tn)

        # Lock the carrier to the first one we see (we never mix UPS + DHL).
        if self._carrier is None:
            self._carrier = carrier
        elif carrier != self._carrier:
            print(
                f"⚠️  {carrier} number detected, but collection is {self._carrier} -> skipped: {tn}"
            )
            return

        self._seen.add(tn)
        self._collected.append(tn)
        print(f"Tracking number detected -> {tn}   ({len(self._collected)} collected)")

    def collect(self):
        """Watch until the user presses Enter. Returns the collected numbers."""
        self._collected = []
        self._seen = set()
        self._carrier = None
        self._stop.clear()
        try:
            self._last_clipboard = pyperclip.paste()
        except Exception:
            self._last_clipboard = ""

        print("\nWaiting for tracking numbers... (Enter = done)")

        thread = threading.Thread(target=self._poll_loop, daemon=True)
        thread.start()

        user_input = input()  # blocks the main thread until Enter

        # Stop the poll thread BEFORE we touch the clipboard ourselves.
        self._stop.set()
        thread.join()

        return self._collected, user_input.strip().lower()

    def remember_written(self, text: str):
        """Tell the watcher which text we wrote, so it won't re-read its own output."""
        self._last_written = text
