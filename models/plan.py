# from dataclasses import dataclass
from datetime import date, datetime
import os

import pandas as pd
import yaml

# from models.income import IncomeComponent
# from models.expenses import ExpenseComponent
from models.assets import RealEstateAsset
from utils.timeutils import as_date, as_period
from utils.constants import PERIOD_FREQ

# @dataclass
class Plan:

    def __init__(self, config_file = None):
        if config_file is None:
            # Default config file path
            config_file = 'plan-default.yaml'
        
        # Resolve the path relative to the current file
        config_file = os.path.join(os.path.dirname(__file__), '..', 'config', config_file)

        with open(config_file, 'r', encoding='utf-8') as f:
            full_cfg = yaml.safe_load(f)

        self.plan_cfg = full_cfg["plan"]
        self.cashflow_cfg = full_cfg["cashflow"]
        self.real_estate_assets_cfg = full_cfg.get("real_estate_assets", [])
        if len(self.real_estate_assets_cfg) > 0:
            self.real_estate_assets = [RealEstateAsset.from_cfg(asset_cfg) for asset_cfg in self.real_estate_assets_cfg]

        # Konvertiere Start/Ende in datetime.date
        self.start_date = as_date(self.plan_cfg["start"])
        self.end_date = as_date(self.plan_cfg["end"])

        # Erzeuge PeriodIndex für start und end, als Index für das zentrale DataFrame df
        self.start = pd.Period(self.start_date, freq=PERIOD_FREQ)
        self.end = pd.Period(self.end_date, freq=PERIOD_FREQ)   

        # Initialize the main data frame structure
        period = pd.period_range(
            self.start, self.end,
            freq=PERIOD_FREQ
        )
        self.df = pd.DataFrame(index=period)

    # Property für Dauer des Plans
    @property
    def duration_months(self):
        return (self.end.year - self.start.year) * 12 + (self.end.month - self.start.month) + 1
    
    def simulate(self):
        """
        Simulates the plan by creating income and expenses components.
        """
        index = self.df.index
        # Simulate and add income and expenses to dataframe
        self.df["salary"] = self._simulate_salary(index)
        self.df["pension_ralf"] = self._simulate_pension_ralf(index)
        self.df["pension_conni"] = self._simulate_pension_conni(index)
        self.df  = pd.merge(self.df, self._simulate_rental_income(index), how="outer")
        self.df["sum_cross_income"] = self.df.sum(axis=1)
        self.df["sum_net_income"] = self.df["sum_cross_income"].apply(self.calculate_net_income)
        return self.df

    def calculate_net_income(self, salary):
        """
        Calculates the net income based on the gross salary and tax rate including social insurance.
        ToDo:
        - currently modul netto is used, which uses "Environment Variables" as config
          That's really not good, because it's a dirty hack
        - in the future, it will be replaced by a proper configuration or introducing API parameters. 
        """
        import netto
        import netto.config

        # set Environment Variables for netto
        # os.environ["YEAR"] = "2025"
        # os.environ["IS_MARRIED"] = "True"
        # os.environ["EXTRA_HEALTH_INSURANCE"] = "0.025"
        # os.environ["CHURCH_TAX"] = "0.00"

        # netto.config.load_config()

        netto.config.year = 2024   # 2025 liefert eiinen dump :-(
        netto.config.is_married = True
        netto.config.extra_health_insurance = 0.025
        netto.config.church_tax = 0.00

        # Calculate net salary using netto module with annual salary
        net_salary = netto.calc_netto(salary*12, verbose=False)

        return net_salary/12  # return monthly net income
    
    def _simulate_salary(self, index) -> pd.Series:
        """
        Simulates the salary income component and returns a pandas Series.
        """
        # Get salary configurations
        salary=self.cashflow_cfg["income"]["gross_salary"]
        salary_start_date = as_date(self.plan_cfg["start"])
        salary_end_date   = as_date(self.plan_cfg["planned_end_of_salary_date"])

        # Create an empty pd.Series with index from Plan
        s = pd.Series(0.0, index=index, name="income_salary")
        s[(index >= as_period(salary_start_date)) & 
          (index <= as_period(salary_end_date))]        = salary
        return s
    
    def _simulate_pension_ralf(self, index) -> pd.Series:
        """
        Simulates Ralf's pension income component and returns a pandas Series.
        """
        pension_ralf = self.cashflow_cfg["income"]["pension_ralf"]
        pension_start_date = as_date(self.plan_cfg["planned_retirement_date_ralf"])
        pension_end_date = as_date(self.plan_cfg["end"])

        # Create an empty pd.Series with index from Plan
        s = pd.Series(0.0, index=self.df.index, name="income_pension_ralf")
        s[(index >= as_period(pension_start_date)) & 
          (index <= as_period(pension_end_date))]      = pension_ralf
        return s

    def _simulate_pension_conni(self, index) -> pd.Series:
        """
        Simulates Conni's pension income component and returns a pandas Series.
        """
        pension_conni = self.cashflow_cfg["income"]["pension_conni"]
        pension_start_date = as_date(self.plan_cfg["planned_retirement_date_conni"])
        pension_end_date = as_date(self.plan_cfg["end"])

        # Create an empty pd.Series with index from Plan
        s = pd.Series(0.0, index=self.df.index, name="income_pension_conni")
        s[(index >= as_period(pension_start_date)) & 
          (index <= as_period(pension_end_date))]      = pension_conni
        return s

    def _simulate_rental_income(self, index) -> pd.DataFrame:
        """
        Simulates rental income component and returns a pandas DataFrame.
        For now, it uses a fixed value from the config.
        In the future, it could be extended to calculate based on real estate assets.
        """
        rental_income_df = pd.DataFrame(index=index)
        for asset in self.real_estate_assets:
            name = f"Miete_{asset.name}"
            # Add the rental income series to the DataFrame
            rental_income_df[name] = asset.rental_income_series(self.df.index)
        # Add a total rental income column
        rental_income_df["rental_income"] = rental_income_df.sum(axis=1)
        return rental_income_df

            

    def _simulate_expenses(self, index) -> pd.DataFrame:
        """
        Simulates the expenses component of the plan and add it to the central data frame.
        """
        # Create a DataFrame for expenses
        expenses_df = pd.DataFrame(index=index)
        for asset in self.real_estate_assets:
            # Get the loan payment DataFrame for the asset
            loan_payments = asset.loan_payment_df(index)
            # Add the loan payments to the main DataFrame
            expenses_df = expenses_df.join(loan_payments, how='outer')
        
        # expenses_df['loan'] = loan_expenses
        # expenses_df['living'] = living_expenses

        return expenses_df
