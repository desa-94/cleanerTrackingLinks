import os
import logging

import win32com.client
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()


class EmailNotifier:
    def __init__(self):
        try:
            self.outlook = win32com.client.GetActiveObject("Outlook.Application")
        except Exception:
            self.outlook = win32com.client.Dispatch("Outlook.Application")

    def generate_and_open_mail(self, send_from: str = "", body: str = "") -> None:
        # Fall back to the address configured in the .env file.
        if not send_from:
            send_from = os.getenv("SEND_FROM_EMAIL", "")
            logger.debug("No 'send_from' set, using default from .env -> %s", send_from)

        mail = self.outlook.CreateItem(0)

        account_found = False
        for account in self.outlook.Session.Accounts:
            if account.SmtpAddress.lower() == send_from.lower():
                """
                pywin32's "mail.SendUsingAccount = account" silently fails because it
                uses the wrong dispatch flag (PUT instead of PUTREF).
                Force it via low-level COM invoke with the correct PROPERTYPUTREF flag (8).

                The 64209 was found via -> print(mail._oleobj_.GetIDsOfNames("SendUsingAccount"))
                """
                mail._oleobj_.Invoke(*(64209, 0, 8, 0, account))

                account_found = True
                logger.debug("Sending from: %s", account.SmtpAddress)
                break

        if not account_found:
            logger.warning("Account '%s' not found - using default.", send_from)

        mail.Subject = "Tracking information for your shipment"
        mail.Body = body
        mail.Display()


if __name__ == "__main__":
    # Quick manual test when running this file directly.
    logging.basicConfig(level=logging.DEBUG)
    notifier = EmailNotifier()
    notifier.generate_and_open_mail(body="Test body")
