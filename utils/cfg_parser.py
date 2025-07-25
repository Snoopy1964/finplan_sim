import yaml
from datetime import date, datetime
# from models.assets import RealEstateAsset
# from models.loan import Loan

def parse_date(val):
    """Konvertiere ein Datum im ISO-Format in ein Python date-Objekt."""
    if isinstance(val, date):
        return val
    try:
        return datetime.strptime(val, "%Y-%m-%d").date()
    except Exception:
        raise ValueError(f"Ungültiges Datumsformat: {val}")

def parse_float(val):
    if val is None:
        return None
    try:
        return float(val)
    except Exception:
        raise ValueError(f"Keine Zahl: {val}")
