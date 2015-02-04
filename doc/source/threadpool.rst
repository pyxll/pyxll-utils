Threadpool
==========

In many cases, there is a need to distribute some work. The threadpool module
exposes a `concurrent.futures.Executor` that can be shared between PyXLL
modules instead of seeing threads being created by any PyXLL module without
common management of the resources.

The user should be aware of the `pyxll.async_func` method that takes care of
the COM marshalling with a background thread.


How to use it?
--------------

The example below shows how to use the shared threadpool::

    from pyxll_utils.threadpool import get_executor

    executor = get_executor()
    
    def _save_data_to_file(data):
        ...

    @xl_func('dataframe:str')
    def save_data(dataframe)
        executor.submit(save_data_to_file, dataframe)
        return 'Saving data to file'

