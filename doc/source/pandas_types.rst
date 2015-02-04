Pandas types
============

Pandas DataFrame and Series are commonly used data structures. The Pandas types
modules provide type converters for DataFrame's and Series within PyXLL.

It provides the following bi-directional type converters:

- `dataframe`: converter for the `pandas.DataFrame` objects with support for
  multi-index or columns
- `series`: converter for the `pandas.Series` objects mapped to a column vector
  in Excel
- `series_t`: converte for the `pandas.Series` objects mapped to a row vector
  in Excel


How to use it?
--------------

Once you have loaded the `pyxll_utils.pandastypes` module, you can use the
custom type converters. The following example shows how to use DataFrames as
input and output::

	from pyxll import xl_func
	import pandas as pa

	@xl_func("int rows, int cols, float value: dataframe")
	def make_empty_dataframe(rows, cols, value):
		# create an empty dataframe
		df = pa.DataFrame({chr(c + ord('A')) : value for c in range(cols)}, index=range(rows))
		
		# return it. The custom type will convert this to a 2d array that
		# excel will understand when this function is called as an array
		# function.
		return df
    
    @xl_func("dataframe df, string col: float")
    def sum_column(df, col):
        return df[col].sum()


