import argparse
import logging

from tracker import Tracker

logger = logging.getLogger(__name__)

try:
    import pyperclip

    HAS_CLIPBOARD = True
except ImportError:
    HAS_CLIPBOARD = False


def main():
    parser = argparse.ArgumentParser(description="Tracking-Link Generator")
    parser.add_argument(
        "tracking_number",
        nargs="?",
        default=None,
        help="Provides the tracking number immediately",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Interactive mode (type numbers manually)",
    )
    parser.add_argument(
        "-l", "--link-only", action="store_true", help="Returns the link only"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enables debug information"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s | %(message)s",
    )

    tracker = Tracker()

    if not HAS_CLIPBOARD:
        print(
            "💡Tip: Install 'pyperclip' (pip install pyperclip) so that links are copied automatically to the clipboard."
        )

    # Single-shot mode: a tracking number was passed directly.
    if args.tracking_number:
        process(tracker, [args.tracking_number], args.link_only)
    # Interactive mode: type numbers manually, one at a time.
    elif args.interactive:
        interactive_loop(tracker, args.link_only)
    # Default: watch the clipboard and collect numbers until Enter.
    else:
        watch_loop(tracker, args.link_only)


def build_result(tracker: Tracker, tracking_numbers: list, link_only: bool) -> str:
    if link_only:
        links = [tracker.build_tracking_link(tn) for tn in tracking_numbers]
        links = [l for l in links if l]
        return "\n".join(links)
    return tracker.build_email(tracking_numbers)


def process(tracker: Tracker, tracking_numbers: list, link_only: bool) -> None:
    result = build_result(tracker, tracking_numbers, link_only)

    if not result:
        logger.debug("No result for: %s", tracking_numbers)
        print("We don't support this carrier.")
        return

    if HAS_CLIPBOARD:
        pyperclip.copy(result)
        print("Copied to the clipboard.")


def watch_loop(tracker, link_only):
    from watcher import ClipboardWatcher

    print("=== Tracking-Link Generator (Watch Mode) ===")
    watcher = ClipboardWatcher(tracker)

    while True:
        collected, command = watcher.collect()

        if command in ["x", "exit", "quit"]:
            print("Closing Application.")
            break

        if not collected:
            print("Keine Trackingnummern erfasst.")
            continue

        result = build_result(tracker, collected, link_only)
        if not result:
            print("We don't support this carrier.")
            continue

        if HAS_CLIPBOARD:
            pyperclip.copy(result)
            watcher.remember_written(result)
            print(
                f"\n{len(collected)} Trackingnummer(n) zusammengefasst und in die Zwischenablage kopiert.\n"
            )


def interactive_loop(tracker, link_only):
    print("=== Tracking-Link Generator ===")

    while True:
        tracking_number = input("Tracking-Number: ")

        if tracking_number.lower() in ["x", "exit", "quit"]:
            print("Closing Application.")
            break

        if not tracking_number:
            print("Please provide a valid tracking number!")
            continue

        process(tracker, [tracking_number], link_only)


if __name__ == "__main__":
    main()
