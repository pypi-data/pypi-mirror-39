from __future__ import print_function

import time
import functools
from human_time_formatter import format_seconds

_DATE = '_date'

def today():
    return time.strftime('%Y-%m-%d')

class DatedCacheManager(object):
    def __init__(self, storage_interface):
        '''An object that contains:
           * functions needed to compute each metric
           * in-memory copy of a set of the metrics
           * a storage interface to save and load metrics from disk (or something else)
           '''
        self.functions_dict = {}
        self.cache = {}
        self.storage_interface = storage_interface
    
    def set_functions_dict(self, functions_dict):
        self.functions_dict = functions_dict
    
    def exists(self, name):
        return (self.storage_interface.exists(name) and
                self.storage_interface.exists(name + _DATE))
    
    def compute(self, name, force=False, verbose=True):
        if force or name not in self.cache:
            if name not in self.functions_dict:
                raise ValueError('{} does not have a compute function defined!'.format(name))
            if verbose:
                print('Compute {}'.format(name))
            t = time.time()
            self.cache[name] = self.functions_dict[name]()
            if verbose:
                print('Completed {} in {}'.format(name, format_seconds(time.time() - t, ndigits=6)))
            
        return self.cache[name]
    
    def _save(self, name, data, verbose=True):
        '''Save data as the name metric (and today's date in a sidecar)'''
        if verbose:
            print('Save {}'.format(name))
        self.storage_interface.save(name, data)
        self.storage_interface.save(name + _DATE, today())
    
    def save(self, name, force=False, verbose=True):
        '''Save the name metric
           Does nothing if there is a previous save and force is False'''
        if force or not self.exists(name):
            v = self.compute(name, force, verbose)
            self._save(name, v, verbose)
        
    def _load(self, name, verbose=True):
        '''Load the stored value into the in-memory cache'''
        self.cache[name + _DATE] = self.storage_interface.load(name + _DATE)
        if verbose:
            print('Load {} pulled on {}'.format(name, self.cache[name + _DATE]))
        self.cache[name] = self.storage_interface.load(name)
    
    def load(self, name, force=False, verbose=True):
        '''Load the name metric and return the value
           Does not reload if the value is in cache and force is False'''
        if force or name not in self.cache:
            self._load(name, verbose)
        return self.cache[name]
    
    def get(self, name, use_stored=True, verbose=True):
        '''Make sure a metric is saved to disk and loaded into memory,
           then return the value
           Only computes+saves/ reloads when needed (or if force is True)'''
        force = not use_stored
        self.save(name, force, verbose)
        return self.load(name, force, verbose)
    
    def clear_cache(self):
        for k in self.cache.keys():
            del self.cache[k]
    
    def __getitem__(self, key):
        return self.get(key)

class CollectingDatedCacheManager(DatedCacheManager):
    def __init__(self, *args, **kwds):
        return DatedCacheManager.__init__(self, *args, **kwds)

    def collect(self, f, name=None):
        name = f.__name__ if name is None else name
        
        self.functions_dict[name] = f
        
        @functools.wraps(f)
        def newf(cache=False, use_stored=True):
            if cache:
                return self.get(name, use_stored=use_stored)
            else:
                return f()
        
        return newf

def doublewrap_class_method(f):
    '''
    a decorator decorator, allowing the decorator to be used as:
    @decorator(with, arguments, and=kwargs)
    or
    @decorator
    lifted from this StackOverflow answer:
    http://stackoverflow.com/questions/653368/how-to-create-a-python-decorator-that-can-be-used-either-with-or-without-paramet
    '''
    @functools.wraps(f)
    def new_dec(self, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            # actual decorated function
            return f(self, args[0]) # use the basic decorator pattern
        else:
            # decorator arguments
            def newf(realf):
                return f(self, realf, *args, **kwargs) # use the nested decorator pattern
            return newf

    return new_dec

def _default_name_generation_function(base_name, params):
    return '_'.join(([base_name] + list(map(str, params)))).replace('.', 'p')

class ParameterizedDatedCacheManager(DatedCacheManager):
    def __init__(self, *args, **kwds):
        self.dynamic_metric_creation = kwds.pop('dynamic_metric_creation', False)
        self.parameterized_metrics = []
        return DatedCacheManager.__init__(self, *args, **kwds)
    
    def build_metric_name(self, f, base_name, params, name_generation_function, create_missing=False):
        create_missing = create_missing or self.dynamic_metric_creation
        metric_name = name_generation_function(base_name, params)
        if metric_name not in self.functions_dict:
            if create_missing:
                self.functions_dict[metric_name] = functools.partial(f, *params)
            else:
                raise ValueError('This function with these parameters is not implemented for caching')
        return metric_name

    def create_parameterized_metric(self, f, base_name, params_list, name_generation_function):
        '''Also adds the function to self as a method and appends it to parameterized_metrics'''
        @functools.wraps(f)
        def f_caching(*params, **kwds):
            use_stored = kwds.pop('use_stored', True)
            metric_name = self.build_metric_name(f, base_name, params, name_generation_function)
            return self.get(metric_name, use_stored=use_stored)

        def get_all(**kwds):
            return [f_caching(*params, **kwds)
                    for params in params_list]

        f_caching.original_function = f
        f_caching.base_name = base_name
        f_caching.params_list = params_list
        f_caching.name_generation_function = name_generation_function
        f_caching.get_all = get_all

        self.parameterized_metrics.append(f_caching)
        setattr(self, base_name, f_caching)

        return f_caching
    
    @doublewrap_class_method
    def collect(self,
                f,
                base_name=None,
                params_list=((),),
                name_generation_function=None):
        base_name = f.__name__ if base_name is None else base_name
        name_generation_function = (
            _default_name_generation_function
            if name_generation_function is None else
            name_generation_function
        )
        
        # Add metrics to functions dict
        for params in params_list:
            self.build_metric_name(f, base_name, params, name_generation_function, create_missing=True)

        f_caching = self.create_parameterized_metric(f, base_name, params_list, name_generation_function)

        @functools.wraps(f)
        def newf(*params, **kwds):
            cache = kwds.pop('cache', False)
            
            if cache:
                return f_caching(*params, **kwds)
            else:
                return f(*params)

        return newf
