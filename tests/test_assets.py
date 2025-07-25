from datetime import date
from models.assets import RealEstateAsset

def test_asset_factory():
    asset_cfg = {
        "name": "Meine Immobilie",
        "purchase_price": 250_000,
        "estimated_value": 300_000,
        "valuation_date": date(2023, 1, 1),
        "annual_rent": 12_000,
        "loans": [
            {
                "name": "Bank A",
                "opening_date": date(2020, 1, 1),
                "principal": 200_000,
                "interest_rate": 2.5,
                "monthly_payment": 1000
            },
            {
                "name": "Bank B",
                "opening_date": date(2023, 1, 1),
                "principal": 400_000,
                "interest_rate": 1.5,
                "monthly_payment": 900.00
            }
        ]
    }
    asset = RealEstateAsset.from_cfg(asset_cfg)
    assert isinstance(asset, RealEstateAsset)

    assert asset.name == "Meine Immobilie"
    assert asset.purchase_price == 250_000
    assert asset.estimated_value == 300_000
    assert asset.valuation_date == date(2023, 1, 1)
    assert asset.annual_rent == 12_000
    assert len(asset.loans) == 2
    assert asset.loans[0].name == "Bank A"
    assert asset.loans[1].name == "Bank B"