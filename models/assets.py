# models/assets.py
# from __future__ import annotations

import pandas as pd
# from dataclasses import dataclass, field
from datetime import date
# from typing import Dict, List, Union
from models.loan import Loan
from utils.cfg_parser import parse_date, parse_float
from utils.constants import PERIOD_FREQ


class RealEstateAsset:
    def __init__(self, name, purchase_price, estimated_value, valuation_date, annual_rent, loans=None):
        self.name = name
        self.purchase_price = purchase_price
        self.estimated_value = estimated_value
        self.valuation_date = valuation_date
        self._initial_annual_rent = annual_rent
        self.loans = loans or []

    @classmethod
    def from_cfg(cls, cfg):
        """Liste von Asset-Configs zu Asset-Objekten."""
        try:
            return cls(
                name=cfg["name"],
                purchase_price=parse_float(cfg["purchase_price"]),
                estimated_value=parse_float(cfg["estimated_value"]),
                valuation_date=parse_date(cfg["valuation_date"]),
                annual_rent=parse_float(cfg["annual_rent"]),
                loans=[Loan.from_cfg(loan_cfg) for loan_cfg in cfg.get(("loans"), [])]
            )
        except KeyError as e:
            raise ValueError(f"Missing required field in asset config: {e}")

    @property
    # Definiere eine property für den jährlichen Mietwert, 
    # damit diese später als function gekapselt ist
    # und z.B. mit einer Indexmiete versehen werden kann
    def annual_rent(self):
        if self._initial_annual_rent is not None:
            return self._initial_annual_rent
        return 0
    
    def rental_income_series(self, index) -> pd.Series:
        """
        Returns a pandas Series with the rental income for each date in the index.
        """
        return pd.Series(self.annual_rent / 12, index=index, name=f"Miete_{self.name}")

    def loan_payment_df(self, index) -> pd.DataFrame:
        """
        Returns a DataFrame with the loan payments for each date in the index.
        Each column corresponds to a loan, and the values are the monthly payments.
        If a loan does not have a payment for a date, the value is 0.
        """
        # Create a DataFrame with the loan payments for each date in the index
        data = {}
        for loan in self.loans:
            sched = loan.get_amortization_schedule()
            # For Konvertierung in period, 
            # immer zuerst mit pd.to_datetime() explizit zu einem datetime Objekt konvertieren!
            # dann erst mit .dt.to_period() in Perioden konvertieren
            # .dt ist ein pandas-Special für Zeitserien.
            # Es ermöglicht, Datumsmethoden (wie .year, .month, .to_period(), .weekday, etc.)
            # auf einer kompletten Series (z. B. DataFrame-Spalte) anzuwenden.
            # Funktioniert nur, wenn die Series/Spalte einen Zeitstempel-Typ (datetime64[ns]) hat.
            sched["period"] = pd.to_datetime(sched["payment_date"]).dt.to_period(PERIOD_FREQ)
            sched = sched.set_index("period")
            
            # Reindex to ensure all periods in the index are included
            payments = sched["payment"].reindex(index, fill_value=0.00)
            data[loan.name] = payments

        df = pd.DataFrame(data, index=index)
        return df



#----------------------------------------------------
# wird ersteinmal nicht benötigt
# die Assets werden in Plan verwaltet und
# Summen von Mieteinnahmen und Kreditzahlungen
# werden im zentralen dataframe der Plan-Klasse
# berechnet.
#----------------------------------------------------
# # verwaltet eine Liste von RealEstateAsset-Objekten
# # und bietet Methoden zum Zugriff auf deren Daten
# class RealEstateAssets:
#     def __init__(self, assets):
#         # assets: Liste von RealEstateAsset-Objekten
#         self.assets = assets

#     def by_name(self):
#         # Optional: Dict für schnellen Zugriff per Name
#         return {asset.name: asset for asset in self.assets}

#     def rental_income_df(self, index):
#         # Liefert DataFrame mit allen Assets (und ggf. Gesamtsumme) als Spalten
#         data = {asset.name: asset.rental_income_series(index) for asset in self.assets}
#         df = pd.DataFrame(data)
#         df["Summe"] = df.sum(axis=1)
#         return df

#     def loan_payment_df(self, index):
#         # Liefert DataFrame mit allen Kreditzahlungen je Asset (und Summe)
#         data = {asset.name: asset.loan_payment_series(index) for asset in self.assets}
#         df = pd.DataFrame(data)
#         df["Summe"] = df.sum(axis=1)
#         return df
