from dataclasses import dataclass
from datetime import date
from models.income import IncomeComponent
from models.expenses import ExpenseComponent

@dataclass
class Plan:
    start: date
    end: date
    income: IncomeComponent
    expenses: ExpenseComponent