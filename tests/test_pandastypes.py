"""
Unit tests for pandastypes conversions
"""
from pyxll_utils.pandastypes import _dataframe_to_var, _series_to_var, _series_to_var_transform
import pandas as pd


def test_nat_df():
    """Test that NaT gets converted to an ArithmeticError exception"""
    df = pd.DataFrame({"A": [pd.NaT]})
    values = _dataframe_to_var(df)
    assert values[0][0] == "A"
    assert isinstance(values[1][0], ArithmeticError)


def test_nat_series():
    """Test that NaT gets converted to an ArithmeticError exception"""
    s = pd.Series([pd.NaT], index=["A"])
    values = _series_to_var(s)
    assert values[0][0] == "A"
    assert isinstance(values[0][1], ArithmeticError)

    values = _series_to_var_transform(s)
    assert values[0][0] == "A"
    assert isinstance(values[1][0], ArithmeticError)
