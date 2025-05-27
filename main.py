from datetime import date
from models.income import IncomeComponent
from models.expenses import ExpenseComponent
from models.plan import Plan
from simulation.cashflow_simulator import simulate_cashflow

plan = Plan(
    start=date(2025, 1, 1),
    end=date(2050, 12, 1),
    income=IncomeComponent(salary=5000, pension=3000, pension_start=date(2030, 9, 1)),
    expenses=ExpenseComponent(loan=1000, living=2000)
)

df = simulate_cashflow(plan)
print(df.head())