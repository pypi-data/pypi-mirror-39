Simple Metrics Manager facilitates managing metrics.

A "metric" as defined here consists of:

 * A string name (and an associated python constant)
 * A function that takes no arguments and returns some data
 * The data returned from the metric function

A StorageInterface is a class that supports storing metric data using some
persistent backend. The current default is the fairly generic '.npy' format
used to store numpy arrays and simple python objects (NpyStorageInterface).
To prevent data corruption, it always saves data to a temp file and then
moves it into the real file (potentially replacing any older copies).

It has a simple save/load/exists API.


The "DatedCacheManager" uses a StorageInterface and supports the following:

 * Automatic caching to both memory and persistent storage,
 * Automatic cache utilization, falling back on memory cache and then
   persistent cache (override with force=False)
 * Dating of all metrics using "side-car" metrics (*_date)
 * Printing of all major actions (disable with verbose=False)


It has the following API:

 * set_functions_dict:
   - Set the core data for the manager, a dictionary that actually defines the metrics.
     Keys are metric names and values are metric functions (no arguments).
     By calling this after \__init__, the manager itself can be used within metric functions.
     See "Usage" below.
 * exists:
   - Boolean, whether the metric is in the memory cache.
 * clear_cache:
   - Remove all metrics from the cache.
 * compute:
   - Call a metric function.
     Caches and returns the data.
 * save:
   - Compute a metric and save the result with the StorageInterface.
     Caches to memory and disk and returns the data.
 * load:
   - Load a metric (assumed to exist)
     Tries the cache, then the StorageInterface, fails otherwise.
     Returns the data
 * get:
   - Call save and then load.
     Caches to disk and the StorageInterface.
     Returns the cached data.
     Overloaded with [] (\__getitem__).

Usage:

    METRIC_1 = 'metric_1'
    METRIC_2 = 'metric_2'

    CM = DataCacheManager(NpyStorageInterface(SOME_DIRECTORY))

    def metric_1_function():
        stuff = do_something()
        return stuff

    def metric_2_function():
        stuff = do_something_else(CM[METRIC_1])
        other_stuff = convert(stuff)
        return other_stuff

    FUNCTIONS_DICT = {
      METRIC_1: metric_1_function,
      METRIC_2: metric_2_function,
      ...
    }

    CM.set_functions_dict(FUNCTIONS_DICT)

Then in some other place, call:

    CM[METRIC_1] or CM[METRIC_2]

This allows for complex dependencies to be handled automatically and efficiently.
