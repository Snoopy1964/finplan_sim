from datetime import date

import pandas as pd
import utils.cfg_parser

from models.assets import RealEstateAsset
# from models.income import IncomeComponent
# from models.expenses import ExpenseComponent
from models.plan import Plan
from simulation.cashflow_simulator import simulate_cashflow
from models.loan import Loan

try:
    loan_lu = Loan(
        name = "BWBank",
        # opening_date = date(2025, 1, 1),
        opening_date = date(2011, 3, 1),
        remaining_principal = 107_103.44,   # principal amount
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
        remaining_principal = 79543.71,    # principal amount
        interest_rate = 3.54,  # annual interest rate
        monthly_payment = 996.33  # monthly payment
    )

    print(loan_wdf.get_amortization_schedule())


    plan = Plan()

    print(f"Plan duration in months: {plan.duration_months}")
    net_income = plan.calculate_net_income(11573)
    print(f"Net income for salary 11573: {net_income}\n\n")

    print(f"Real Estate Assets: {type(plan.real_estate_assets)}\n")
    #
    # Ludwigshafen
    #
    asset_lu = plan.real_estate_assets[0]
    print(f"Real estate asset name: {asset_lu.name}")
    print(f"Real estate asset annual rent: {asset_lu.annual_rent}")
    print(f"Real estate asset rental income series:\n{asset_lu.rental_income_series(plan.df.index)} \n\n")

    print(f"Real estate asset loan payment series:\n{asset_lu.loan_payment_df(plan.df.index)} \n\n")
    #
    # Leipzig
    #
    asset_lpz = plan.real_estate_assets[2]
    print(f"Real estate asset name: {asset_lpz.name}")
    print(f"Real estate asset annual rent: {asset_lpz.annual_rent}")
    print(f"Real estate asset rental income series:\n{asset_lpz.rental_income_series(plan.df.index)} \n\n")
 
    print(f"Real estate asset loan payment series:\n{asset_lpz.loan_payment_df(plan.df.index)} \n\n")

    for asset in plan.real_estate_assets:
        plan.df = pd.concat( [plan.df, 
                              asset.loan_payment_df(plan.df.index), 
                              asset.rental_income_series(plan.df.index)], 
                              axis = 1)
    print(plan.df)


    # Simulate cashflow
    plan.simulate()

    print(f"Plan DataFrame:\n\n{plan.df}\n")

except KeyError as e:
    print(f"An error occurred: {e}")
    raise
    