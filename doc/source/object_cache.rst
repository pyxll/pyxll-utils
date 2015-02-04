Object cache
============

The object cache module provides useful additional functionality to PyXLL. Excel
can display the returned value of PyXLL functions when it can make sense of the
data type. Basic types are supported directly. When a PyXLL
function wants to return a reference to an object things get more
complicated. The intention is to keep this reference alive in the spreadsheet
while doing some other computation. The object cache can be activated within
PyXLL to take care of the conversion from Python to Excel and from Excel to
Python of object references. By using the object cache developers don't have
to implement a mechanism to store and track references between Excel and
Python.

The object cache module contributes a new PyXLL custom type, `cached_object`,
which can then be used to pass and retrieve objects from PyXLL functions.

The object cache also takes care of cleaning up the cache when cached objects
are no longer needed.

How to use it
-------------

Once you have imported the module (`pyxll_utils.object_cache`), you can use the
PyXLL custom type in your PyXLL function definition. In the example here below,
the `generate_random_data` function returns a cached object (a potentially
large Numpy array). The second function, `compute_mean`,  makes us of this
cached object.::

    @xl_func("int rows, int columns: cached_object")
    def generate_random_data(rows, columns):
        """ Generate an array with random data for the gives size (rows,
        columns). """

        return numpy.random.random(rows, columns)

    @xl_func("cached_object data: float)
    def compute_mean(data):
        if not isinstance(data, np.ndarray):
            raise ValueError('compute_mean only support NumPy arrays as input')

        return data.mean()
