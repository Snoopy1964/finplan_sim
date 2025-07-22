# from dataclasses import dataclass
from datetime import date, datetime
import os

import pandas as pd
import yaml

# from models.income import IncomeComponent
# from models.expenses import ExpenseComponent
from utils.timeutils import as_date

# @dataclass
class Plan:

    def __init__(self, config_file = None):
        if config_file is None:
            # Default config file path
            config_file = 'plan-default.yaml'
        
        # Resolve the path relative to the current file
        config_file = os.path.join(os.path.dirname(__file__), '..', 'config', config_file)

        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        self.plan = config["plan"]
        self.cashflow = config["cashflow"]
        self.real_estate_assets = config["real_estate_assets"]
        
        # Optional: Konvertiere Start/Ende in datetime.date
        self.start = as_date(self.plan["start"])
        self.end = as_date(self.plan["end"])

        # Create main data structure
        dates = pd.date_range(self.start, self.end, freq='MS').date
        self.df = pd.DataFrame(index=dates)

    # Property für Dauer des Plans
    @property
    def duration_months(self):
        return (self.end.year - self.start.year) * 12 + (self.end.month - self.start.month) + 1
    
    def simulate(self):
        """
        Simulates the plan by creating income and expenses components.
        """
       
        # Simulate and add income and expenses to dataframe
        self.df["salary"] = self._simulate_salary()
        self.df["pension_ralf"] = self._simulate_pension_ralf()
        self.df["pension_conni"] = self._simulate_pension_conni()
        self.df["rental_income"] = self._simulate_rental_income()
        self.df["sum_cross_income"] = self.df["salary"] + self.df["pension_ralf"] + self.df["pension_conni"] + self.df["rental_income"]
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
    
    # def _simulate_income(self):
    #     """
    #     Simulates the income component of the plan and add it to the netral data frame.
    #     """
    #     # Get salary configurations

    #     # Get Ralf's pension configurations
    #     pension_ralf=self.cashflow["income"]["pension_ralf"]
    #     pension_start_date=as_date(self.cashflow["income"]["pension_start"])
    #     pension_end_date=as_date(self.cashflow["income"]["end"])

    #     # Get Conni's pension configurations
    #     pension_conni=self.cashflow["income"]["pension_conni"]
    #     pension_conni_start_date=as_date(self.cashflow["income"]["pension_conni_start"])
    #     pension_conni_end_date=as_date(self.cashflow["income"]["end"])

    def _simulate_salary(self):
        """
        Simulates the salary income component and returns a pandas Series.
        """
        # Get salary configurations
        salary=self.cashflow["income"]["gross_salary"]
        salary_start_date = as_date(self.plan["start"])
        salary_end_date   = as_date(self.plan["planned_end_of_salary_date"])

        # Create an empty pd.Series with index from Plan
        s = pd.Series(0.0, index=self.df.index, name="income_salary")
        s[(self.df.index >= salary_start_date) & (self.df.index <= salary_end_date)] = salary
        return s
    
    def _simulate_pension_ralf(self):
        """
        Simulates Ralf's pension income component and returns a pandas Series.
        """
        pension_ralf = self.cashflow["income"]["pension_ralf"]
        pension_start_date = as_date(self.plan["planned_retirement_date_ralf"])
        pension_end_date = as_date(self.plan["end"])

        # Create an empty pd.Series with index from Plan
        s = pd.Series(0.0, index=self.df.index, name="income_pension_ralf")
        s[(self.df.index >= pension_start_date) & (self.df.index <= pension_end_date)] = pension_ralf
        return s
    
    def _simulate_pension_conni(self):
        """
        Simulates Conni's pension income component and returns a pandas Series.
        """
        pension_conni = self.cashflow["income"]["pension_conni"]
        pension_start_date = as_date(self.plan["planned_retirement_date_conni"])
        pension_end_date = as_date(self.plan["end"])

        # Create an empty pd.Series with index from Plan
        s = pd.Series(0.0, index=self.df.index, name="income_pension_conni")
        s[(self.df.index >= pension_start_date) & (self.df.index <= pension_end_date)] = pension_conni
        return s

    def _simulate_rental_income(self):
        """
        Simulates rental income component and returns a pandas Series.
        For now, it uses a fixed value from the config.
        In the future, it could be extended to calculate based on real estate assets.
        """

        # assets_by_name = {asset["name"]: asset for asset in self.real_estate_assets}

        rental_income = self.cashflow["income"]["rental_income"]
        rental_start_date = as_date(self.plan["start"])
        rental_end_date = as_date(self.plan["end"])

        # Create an empty pd.Series with index from Plan
        s = pd.Series(0.0, index=self.df.index, name="rental_income")
        s[(self.df.index >= rental_start_date) & (self.df.index <= rental_end_date)] = rental_income
        return s

    def _simulate_expenses(self):
        """
        Simulates the expenses component of the plan and add it to the netral data frame.
        """
        loan_expenses = self.cashflow["expenses"]["loan"]
        living_expenses = self.cashflow["expenses"]["living"]

        # Create a DataFrame for expenses
        expenses_df = pd.DataFrame(index=self.df.index)
        expenses_df['loan'] = loan_expenses
        expenses_df['living'] = living_expenses

        return expenses_df
