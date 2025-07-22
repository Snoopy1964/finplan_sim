# models/loan.py
from __future__ import annotations

import pandas as pd
# from dataclasses import dataclass, field
from datetime import date
# from typing import Dict, List, Union

# @dataclass
# class ExtraPayment:
#     date: date
#     amount: float

# @dataclass
# class InterestChange:
#     date: date
#     new_interest: float


class Loan:

    def __init__(self, name, opening_date, principal, interest_rate, monthly_payment):
        self.name = name                             # name of the loan (Name des Kredites)
        self.opening_date = opening_date             # date when the loan was opened (Auszahlungsdatum des Kredits)
        self.principal = principal                   # principal amount of the loan (Höhe des Kreditbetrages)
        self.initial_interest_rate = interest_rate   # initial interest rate (Anfänglicher Zinssatz)
        # self.initial_repayment_rate = repayment_rate # initial annual repayment rate (Anfängliche jährlicheTilgungsrate)
        self.initial_monthly_payment = monthly_payment
        # Calculate monthly payment based on principal, interest rate and repayment rate
        self.initial_payment_rate = round((self.initial_monthly_payment * 12 / self.principal * 100) - self.initial_interest_rate, 2)  # monthly payment rate in percent (Monatliche Tilgungsrate in Prozent)

        # Initialize action lists
        self.actions = []
        self.actions.append({"type": "interest_change", 
                             "date": self.opening_date, 
                             "new_interest": self.initial_interest_rate})
        self.actions.append({"type": "monthly_payment_change", 
                             "date": self.opening_date, 
                             "new_payment": self.initial_monthly_payment})

    def _create_payment_df(self, months = 12):
        """Create a DataFrame for the loan payments over a specified number of months."""
        data =  []
        remaining = self.principal
        interest_rate = self.initial_interest_rate
        monthly_payment = self.initial_monthly_payment

        for m in range(1, months + 1):
            # Check for interest changes or extra payments in this month
            month_date = (self.opening_date + pd.DateOffset(months=m-1)).date() # convert from pd.Timestamp to date
            # find all actions for this month
            actions_this_month = [action for action in self.actions if action["date"] == month_date]

            for action in actions_this_month:
                # check for extra payments
                if action["type"] == "extra_payment":
                    payment_type = "extra_payment"
                    remaining -= action["amount"]
                    print(f"Extra payment of {action['amount']} applied in month {m}, reducing remaining balance to {remaining}")
                    # since this is a payment, we still need to add a row to the DataFrame
                    # but we do not calculate interest or principal for this month
                    # we just record the extra payment
                    # and set principal and interest to 0
                    data.append({ # type: ignore
                        "month": m,
                        "payment_date": month_date,
                        "payment_type": payment_type,
                        "payment": action["amount"],
                        "interest_rate": interest_rate,
                        "principal": 0.0,  # No principal payment for extra payments
                        "interest": 0.0,   # No interest for extra payments
                        "remaining": max(remaining, 0.0)  # Ensure remaining is not negative
                    })

                # check for monthly payment changes
                if action["type"] == "monthly_payment_change":
                    monthly_payment = action["new_payment"]
                    print(f"Monthly payment set to {monthly_payment} in month {m}")

                # check for interest changes
                if action["type"] == "interest_change":
                    interest_rate = action["new_interest"]
                    print(f"Interest rate set to {interest_rate}% in month {m}")

                # check for full payoff
                if action["type"] == "full_payoff":
                    remaining = 0.0
                    monthly_payment = 0.0
                    print(f"Loan paid off in full in month {m}, remaining balance is now {remaining}")
                    # since this is a payment, we still need to add a row to the DataFrame
                    data.append({ # type: ignore
                        "month": m,
                        "payment_date": month_date,
                        "payment_type": "full_payoff",
                        "payment": 0.0,  # No payment for full payoff
                        "interest_rate": interest_rate,
                        "principal": 0.0,  # No principal payment for full payoff
                        "interest": 0.0,   # No interest for full payoff
                        "remaining": remaining  # Remaining is now 0
                    })

                

            # Calculate interest and principal payment for this month
            interest          = round(remaining * (interest_rate / 100) / 12, 2)
            principal_payment = round(monthly_payment - interest, 2)
            remaining         = round(remaining - principal_payment, 2)
 
            # Stop if remaining <= 0:
            if remaining > 0:
                # add the monthly payment to the DataFrame
                data.append({ # type: ignore
                    "month": m,
                    "payment_date": pd.Timestamp(self.opening_date + pd.DateOffset(months=m-1)).date(),  # convert from pd.Timestamp to date
                    "payment_type": "monthly",
                    "payment": monthly_payment,
                    "interest_rate": interest_rate,
                    "principal": min(principal_payment, remaining),  # Ensure principal does not exceed remaining   
                    "interest": interest,
                    "remaining": max(remaining, 0.0)                 # Ensure remaining is not negative
                })
                
        return pd.DataFrame(data)

    def get_amortization_schedule(self) -> pd.DataFrame:
        """Return amortization schedule as pandas DataFrame."""
        
        return self._create_payment_df(1000)

    def add_extra_payment(self, amount: float, payment_date: date):
        print(f"Adding extra payment of {amount} on {payment_date}")
        self.actions.append({"type": "extra_payment", 
                             "date": payment_date, 
                             "amount": amount})
        pass

    def change_interest_rate(self, new_interest: float, change_date: date):
        """Change interest rate on given date."""
        print(f"Changing interest rate to {new_interest}% on {change_date}")
        self.actions.append({"type": "interest_change", 
                             "date": change_date, 
                             "new_interest": new_interest})
        
    def change_monthly_payment(self, new_payment: float, change_date: date):
        """Change monthly payment on given date."""
        print(f"Changing monthly payment to {new_payment} on {change_date}")
        self.actions.append({"type": "monthly_payment_change", 
                             "date": change_date, 
                             "new_payment": new_payment})

    def pay_off_full(self, payoff_date: date):
        """Simulate full payoff on given date."""
        print(f"Paying off loan in full on {payoff_date}")
        self.actions.append({"type": "full_payoff", 
                             "date": payoff_date})
        pass
