from tracker import Tracker
import argparse
import logging

logger = logging.getLogger(__name__)

try:
    import pyperclip
    HAS_CLIPBOARD = True
except ImportError:
    HAS_CLIPBOARD = False

def main():
    tracker = Tracker()

    parser = argparse.ArgumentParser(description="Tracking-Link Generator")
    parser.add_argument("tracking_number", nargs="?", default=None, help="Provides the tracking number immediately")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactive mode (loop)")
    parser.add_argument("-l", "--link-only", action="store_true", help="Returns the link only")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enables debug information")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO ,
        format="%(levelname)s | %(message)s"
    )

    if not HAS_CLIPBOARD:
        print("💡Tip: Install 'pyperclip' (pip install pyperclip) so that links are copied automatically to the clipboard.")

    if args.tracking_number:
        process(tracker, args.tracking_number, args.link_only)
    else:
        interactive_loop(tracker, args.link_only)

def process(tracker: Tracker, tracking_number: str, link_only: bool) -> None:
    if link_only:
        result = tracker.build_tracking_link(tracking_number)
    else:
        result = tracker.build_email(tracking_number)

    if not result:
        logger.debug("No result for tracking number: %s", tracking_number)
        print("We don't support this carrier.")
        return

    if HAS_CLIPBOARD:
        pyperclip.copy(result)
        print("Copied to the clipboard.")

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

        process(tracker, tracking_number, link_only)

if __name__ == "__main__":
    main()