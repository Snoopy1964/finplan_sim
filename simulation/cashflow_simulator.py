import pandas as pd
from models.plan import Plan

def simulate_cashflow(plan: Plan) -> pd.DataFrame:
    income = plan.income.simulate(plan.start, plan.end)
    expenses = plan.expenses.simulate(plan.start, plan.end)
    df = pd.concat([income, expenses], axis=1)
    df["net_cashflow"] = df["income"] - df["expenses"]
    return df