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

    values_t = _series_to_var_transform(s)
    assert values_t[0][0] == "A"
    assert isinstance(values_t[1][0], ArithmeticError)


def test_series():
    s = pd.Series(range(3), index=[chr(ord('A') + x) for x in range(3)])

    values = _series_to_var(s)
    expected = [
        ['A', 0],
        ['B', 1],
        ['C', 2]
    ]
    assert values == expected

    values_t = _series_to_var_transform(s)
    expected_t = [
        ['A', 'B', 'C'],
        [0,   1,   2]
    ]
    assert values_t == expected_t


def test_multiindex_series():
    idx = pd.MultiIndex.from_tuples([(1, 1), (1, 2), (2, 1), (2, 2)])
    s = pd.Series(range(len(idx)), index=idx)

    values = _series_to_var(s)
    expected = [
        [1,  1, 0],
        ['', 2, 1],
        [2,  1, 2],
        ['', 2, 3]
    ]
    assert values == expected

    values_t = _series_to_var_transform(s)
    expected_t = [
        [1, '', 2, ''],
        [1, 2,  1, 2],
        [0, 1,  2, 3]
    ]
    assert values_t == expected_t


def test_dataframe():
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    values = _dataframe_to_var(df)
    expected = [
        ['A', 'B'],
        [1, 4],
        [2, 5],
        [3, 6]
    ]
    assert values == expected


def test_dataframe_with_named_index():
    idx = pd.Index([0, 1, 2], name="I")
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}, index=idx)
    values = _dataframe_to_var(df)
    expected = [
        ['I', 'A', 'B'],
        [0, 1, 4],
        [1, 2, 5],
        [2, 3, 6]
    ]
    assert values == expected


def test_dataframe_with_multiindex():
    idx = pd.MultiIndex.from_tuples([(0, 0), (0, 1), (1, 1)], names=["I1", "I2"])
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}, index=idx)
    values = _dataframe_to_var(df)
    expected = [
        ['I1', 'I2', 'A', 'B'],
        [0, 0, 1, 4],
        ['', 1, 2, 5],
        [1, 1, 3, 6]
    ]
    assert values == expected


def test_dataframe_with_multicolumns():
    cols = pd.MultiIndex.from_tuples([('a', 'b'), ('a', 'c'), ('b', 'a')], names=["I1", "I2"])
    df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], columns=cols)
    values = _dataframe_to_var(df)
    expected = [
        ['a', '', 'b'],
        ['b', 'c', 'a'],
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    assert values == expected


def test_dataframe_with_multicolumns_and_index():
    idx = pd.Index([0, 1, 2], name="I")
    cols = pd.MultiIndex.from_tuples([('a', 'b'), ('a', 'c'), ('b', 'a')], names=["I1", "I2"])
    df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], columns=cols, index=idx)
    values = _dataframe_to_var(df)
    expected = [
        ['I1', 'a', '', 'b'],
        ['I \\ I2', 'b', 'c', 'a'],
        [0, 1, 2, 3],
        [1, 4, 5, 6],
        [2, 7, 8, 9]
    ]
    assert values == expected


def test_dataframe_with_multicolumns_and_multiindex():
    idx = pd.MultiIndex.from_tuples([(0, 0), (0, 1), (1, 1)], names=["I1", "I2"])
    cols = pd.MultiIndex.from_tuples([('a', 'b'), ('a', 'c'), ('b', 'a')], names=["C1", "C2"])
    df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], columns=cols, index=idx)
    values = _dataframe_to_var(df)
    expected = [
        ['', 'C1', 'a', '', 'b'],
        ['I1', 'I2 \\ C2', 'b', 'c', 'a'],
        [0, 0, 1, 2, 3],
        ['', 1, 4, 5, 6],
        [1, 1, 7, 8, 9]
    ]
    assert values == expected


def test_multiindex_innermost_level():
    idx = pd.MultiIndex.from_tuples([('a', 'b', 'c'), ('a', 'b', 'c'), ('a', 'b', 'd')], names=["I1", "I2", "I3"])
    cols = pd.Index(['A', 'B', 'C'])
    df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], index=idx, columns=cols)
    values = _dataframe_to_var(df)
    expected = [
        ['I1', 'I2', 'I3', 'A', 'B', 'C'],
        ['a', 'b', 'c', 1, 2, 3],
        ['', '', 'c', 4, 5, 6],
        ['', '', 'd', 7, 8, 9]
    ]
    assert values == expected
