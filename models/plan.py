from dataclasses import dataclass
from datetime import date
from .income import IncomeComponent
from .expenses import ExpenseComponent

@dataclass
class Plan:
    start: date
    end: date
    income: IncomeComponent
    expenses: ExpenseComponent