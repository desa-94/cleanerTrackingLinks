from tracker import Tracker

try:
    import pyperclip
    HAS_CLIPBOARD = True
except ImportError:
    HAS_CLIPBOARD = False

def main():
    tracker = Tracker()
    print("=== Tracking-Link Generator ===\n")

    if not HAS_CLIPBOARD:
        print("💡Tip: Install 'pyperclip' (pip install pyperclip) so that links are copied automatically.")

    while True:
        user_input = input("Tracking-Number: ")

        if user_input.lower() in ["x", "exit", "quit"]:
            print("Bye!")
            break  

        if not user_input:
            print("Please only insert a valid tracking number!")
            continue

        email_text = tracker.build_email(user_input)

        if email_text:
            print("\n--- Generated Email: ---")
            print(email_text)
            print("-------------------------\n")

            if HAS_CLIPBOARD:
                pyperclip.copy(email_text)
                print("Email copied to the clipboard.")
        else:
            print("We dont support this service or carrier.\n")

if __name__ == "__main__":
    main()