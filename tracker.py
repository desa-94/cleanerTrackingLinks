class Tracker:
    CARRIER_URLS = {
        "UPS": "https://www.ups.com/track?tracknum={}&loc=de_DE",
        "DHL": "https://www.dhl.de/de/privatkunden/pakete-empfangen/verfolgen.html?piececode={}",
    }

    _KEYBOARD_SWAP = str.maketrans({"Z":"Y", "Y":"Z"})

    def fix_UPS_keyboard_layout_error(self, tn: str) -> str:
        clean_tn = tn.strip().upper()
        if clean_tn.startswith("1Y"):
            return self.swap(clean_tn)
        return clean_tn

    def swap(self, tn: str) -> str:
        return tn.translate(self._KEYBOARD_SWAP)
    
    def detect_carrier(self, tn: str) -> str:
        if tn.startswith("1Z"):
            return "UPS"
        if tn.startswith(("JD", "JJ", "0034")):
            return "DHL"

    def build_tracking_link(self, tn: str, used_carrier: str = None) -> str:
        clean_tn = self.fix_UPS_keyboard_layout_error(tn)

        if not clean_tn:
            return ""

        carrier = used_carrier.upper() if used_carrier else self.detect_carrier(clean_tn)
        template = self.CARRIER_URLS.get(carrier)

        return template.format(clean_tn) if template else ""