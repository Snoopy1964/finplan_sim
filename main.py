from datetime import date

import pandas as pd
from models.income import IncomeComponent
from models.expenses import ExpenseComponent
from models.plan import Plan
from simulation.cashflow_simulator import simulate_cashflow
from models.loan import Loan

loan_lu = Loan(
    name = "BWBank",
    # opening_date = date(2025, 1, 1),
    opening_date = date(2011, 3, 1),
    principal = 107_103.44,   # principal amount
    interest_rate = 1.8700,   # annual interest rate
    monthly_payment = 310.92  # monthly payment
)

# loan_lu.add_extra_payment(amount=1000, payment_date=date(2025, 3, 1))
# loan_lu.change_interest_rate(new_interest=1.8700, change_date=date(2021, 10, 1))
# loan_lu.change_monthly_payment(new_payment=310.92, change_date=date(2021, 10, 1))
# loan_lu.pay_off_full(payoff_date=date(2030, 9, 1))
# print(loan_lu.get_amortization_schedule())

#   - name: AXA
#     remaining_principal: 79543.71
#     interest_rate: 0.0354
#     number_of_payments: 92
#     monthly_payment: 996.33

loan_wdf = Loan(
    name = "AXA",
    opening_date = date(2025, 6, 1),
    principal = 79543.71,    # principal amount
    interest_rate = 3.54,  # annual interest rate
    monthly_payment = 996.33  # monthly payment
)

# print(loan_wdf.get_amortization_schedule())


plan = Plan()

df = plan.simulate()
# print(df.head())
# print(".........")
# print(df.tail())

print(f"Plan duration in months: {plan.duration_months}")
print(df)

print(df.loc[date(2025, 6, 1):date(2035, 12, 31)])

print("Hack um alles zu drucken")
tmp = df.copy()
tmp.index = pd.to_datetime(tmp.index)
with pd.option_context('display.max_rows', None):
    print(tmp.loc["2025-06-01":"2035-12-31"])

net_income = plan.calculate_net_income(11573)
print(f"Net income for salary 11573: {net_income}")


# df = simulate_cashflow(plan)
# print(df.head())