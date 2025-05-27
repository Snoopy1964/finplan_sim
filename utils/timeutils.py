from datetime import date
import pandas as pd


def date_range_index(start: date, end: date, freq: str = "MS") -> pd.Index:
    """
    Returns a pd.Index of datetime.date values covering the specified period.
    Useful for consistent date-based indexing when comparing against datetime.date values.

    Parameters:
        start (date): Start date (inclusive)
        end (date): End date (inclusive)
        freq (str): Frequency string compatible with pandas (default: 'MS' = Month Start)

    Returns:
        pd.Index: Index of datetime.date values
    """
    return pd.Index([d.date() for d in pd.date_range(start, end, freq=freq)])


def zero_series(start: date, end: date, name: str = None, freq: str = "MS") -> pd.Series:
    """
    Creates a zero-initialized pandas Series with a datetime.date index.

    Parameters:
        start (date): Start date (inclusive)
        end (date): End date (inclusive)
        name (str): Optional name for the Series
        freq (str): Frequency string compatible with pandas (default: 'MS')

    Returns:
        pd.Series: Zero-initialized Series with datetime.date index
    """
    index = date_range_index(start, end, freq)
    return pd.Series(0.0, index=index, name=name)
