from datetime import date
import pandas as pd
from .base_component import BaseComponent
from utils.timeutils import date_range_index, zero_series

class IncomeComponent(BaseComponent):
    def __init__(self, salary: float, pension: float, pension_start: date):
        self.salary = salary
        self.pension = pension
        self.pension_start = pension_start

    def simulate(self, start: date, end: date) -> pd.Series:
        date_index = date_range_index(start, end, freq="MS")

        income = pd.Series(0.0, index=date_index)
        income.loc[date_index < self.pension_start] = self.salary
        income.loc[date_index >= self.pension_start] = self.pension
        return income.rename("income")