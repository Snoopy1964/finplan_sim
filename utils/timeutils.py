from datetime import date, datetime
import pandas as pd

def as_date(val):
    """
    Converts a value to a datetime.date object.
    If the value is already a date, it returns it as is.
    If the value is a string, it attempts to parse it as a date.
    Parameters:
        val: The value to convert, can be a date or a string in 'YYYY-MM-DD' format.
    Returns:
        date: A datetime.date object."""
    
    if isinstance(val, date):
        return val
    return datetime.strptime(val, "%Y-%m-%d").date()

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


def zero_series(start: date, end: date, name: str 
                , freq: str = "MS") -> pd.Series:
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
