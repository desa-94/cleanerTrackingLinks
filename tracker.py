import json

import logging
logger = logging.getLogger(__name__)

class Tracker:
    _KEYBOARD_SWAP = str.maketrans({"Z":"Y", "Y":"Z"})

    def __init__(self, config_path="config.json"):
        with open(config_path, encoding="utf-8") as conf:
            config = json.load(conf)

        self.carriers = config["carriers"] 
        self.email_template = config["email_template"]

        logger.debug(f"Loaded config file: {config_path}.")

    def fix_UPS_keyboard_layout_error(self, tn: str) -> str:
        clean_tn = tn.strip().upper()
        if clean_tn.startswith("1Y"):
            logger.debug("Keyboard fix applied: %s -> %s", tn.upper(), self.swap(clean_tn))
            return self.swap(clean_tn)
        return clean_tn

    def swap(self, tn: str) -> str:
        return tn.translate(self._KEYBOARD_SWAP)

    def detect_carrier(self, tn: str) -> str:
        for carrier, data in self.carriers.items():
            prefixes = tuple(data.get("prefixes", []))
            if prefixes and tn.startswith(prefixes):
                return carrier
        logger.debug("No carrier detected for: %s", tn)
        return None

    def build_tracking_link(self, tn: str) -> str:
        clean_tn = self.fix_UPS_keyboard_layout_error(tn)

        if not clean_tn: 
            return ""

        carrier = self.detect_carrier(clean_tn)
        template = self.carriers.get(carrier)

        if not template or "url" not in template:
            return ""

        return template["url"].format(clean_tn)

    def build_email(self, tn: str) -> str:
        link = self.build_tracking_link(tn)

        if not link:
            return ""

        return self.email_template.format(link)
