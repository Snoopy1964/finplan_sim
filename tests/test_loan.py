from datetime import date
from models.loan import Loan

def test_loan_creation():
    loan = Loan(
        name="Mein Kredit",
        opening_date=date(2023, 1, 1),
        principal=100_000,
        interest_rate=2.0,
        monthly_payment=416.67
    )
    assert loan.name == "Mein Kredit"
    assert loan.opening_date == date(2023, 1, 1)
    assert loan.principal == 100_000
    assert loan.initial_interest_rate == 2.0
    assert loan.initial_payment_rate == 3.0
    assert round(loan.initial_monthly_payment, 2) == 416.67  # 100_000 * (2+3)/100/12
    assert len(loan.actions) == 2  # Initial payment and interest rate action

def test_add_extra_payment():
    loan = Loan(
        name="Test",
        opening_date=date(2024, 1, 1),
        principal=50_000,
        interest_rate=1.5,
        monthly_payment=166.67
    )
    assert len(loan.actions) == 2
    loan.add_extra_payment(3_000, date(2025, 5, 1))
    assert len(loan.actions) == 3
    assert [ep["amount"] for ep in loan.actions if ep["type"] == "extra_payment"] == [3_000]
    assert [ep["date"] for ep in loan.actions if ep["type"] == "extra_payment"] == [date(2025, 5, 1)]

def test_change_interest_rate():
    loan = Loan(
        name="Test",
        opening_date=date(2023, 1, 1),
        principal=100_000,
        interest_rate=1.5,
        monthly_payment=333.33
    )
    assert len(loan.actions) == 2
    loan.change_interest_rate(2.0, date(2024, 5, 1))
    assert len(loan.actions) == 3
    assert [ni["new_interest"] for ni in loan.actions if ni["type"] == "interest_change"] == [1.5, 2.0]
    assert [ni["date"] for ni in loan.actions if ni["type"] == "interest_change"] == [date(2023, 1, 1), date(2024, 5, 1)]

def test_pay_off_full():
    loan = Loan(
        name="Test",
        opening_date=date(2023, 1, 1),
        principal=100_000,
        interest_rate=1.5,
        monthly_payment=333.33
    )
    assert len(loan.actions) == 2
    loan.pay_off_full(date(2024, 12, 31))
    assert len(loan.actions) == 3
    assert [po["date"] for po in loan.actions if po["type"] == "full_payoff"] == [date(2024, 12, 31)]

def test_monthly_payment_change():
    # breakpoint()
    from models.loan import Loan  # Ensure Loan is imported here for the test
    loan = Loan(
        name="Test",
        opening_date=date(2023, 1, 1),
        principal=100_000,
        interest_rate=1.5,
        monthly_payment=333.33
    )
    # breakpoint()
    assert len(loan.actions) == 2
    loan.change_monthly_payment(500, date(2024, 6, 1))
    assert len(loan.actions) == 3
    assert [mp["new_payment"] for mp in loan.actions if mp["type"] == "monthly_payment_change"] == [333.33, 500.00]
    assert [mp["date"] for mp in loan.actions if mp["type"] == "monthly_payment_change"] == [date(2023, 1, 1), date(2024, 6, 1)]