import os
import shutil
import tempfile

import numpy as np

from simple_metrics_manager import NpzStorageInterface, ParameterizedDatedCacheManager


def test_collect_1():
    a = np.array([1,4,5])
    
    temp_dir = tempfile.mkdtemp()
    cm = ParameterizedDatedCacheManager(NpzStorageInterface(temp_dir))

    @cm.collect
    def sample():
        return a
    
    assert hasattr(cm, 'sample')
    assert hasattr(cm.sample, 'original_function')
    assert cm.sample.params_list == ((),)

    assert 'sample' in cm.functions_dict

    assert np.array_equal(cm.sample(), a)
    assert np.array_equal(cm.cache['sample'], a)
    sample(cache=True)

    shutil.rmtree(temp_dir)


def test_collect_2():
    a = np.array([1,4,5])
    a_2_3 = a * 2 + 3
    params_list = [[2, 3], [4, 5]]
    
    temp_dir = tempfile.mkdtemp()
    cm = ParameterizedDatedCacheManager(NpzStorageInterface(temp_dir))

    @cm.collect(params_list=params_list)
    def sample(x, y):
        return a * x + y
    
    assert hasattr(cm, 'sample')
    assert hasattr(cm.sample, 'original_function')
    assert hasattr(cm.sample, 'params_list')
    assert cm.parameterized_metrics[0].__name__ == 'sample'
    assert 'sample_2_3' in cm.functions_dict
    assert 'sample_4_5' in cm.functions_dict
    assert 'sample' not in cm.functions_dict


    assert cm.sample.params_list == params_list

    assert np.array_equal(sample(2, 4), a * 2 + 4)

    try:
        cm.sample(2, 4)
        failed = False
    except ValueError:
        failed = True

    assert failed

    try:
        sample(2, 4, cache=True)
        failed = False
    except ValueError:
        failed = True

    assert failed

    assert np.array_equal(cm.sample(2, 3), a_2_3)
    assert np.array_equal(cm.cache['sample_2_3'], a_2_3)

    def sample_new(x, y):
        return a * x + 2 * y
    
    cm.functions_dict['sample_2_3'] = lambda: sample_new(2, 3)
    a_2_3_a = sample(2, 3, cache=True)
    assert np.array_equal(a_2_3_a, a_2_3)
    a_2_3_b = sample(2, 3, cache=True, use_stored=False)
    assert not np.array_equal(a_2_3_b, a_2_3)
    assert np.array_equal(a_2_3_b, sample_new(2, 3))
    
    shutil.rmtree(temp_dir)

def test_collect_3():
    a = np.array([1,4,5])
    a_2_3 = a * 2 + 3
    params_list = [[2, 3], [4, 5]]
    
    temp_dir = tempfile.mkdtemp()
    cm = ParameterizedDatedCacheManager(NpzStorageInterface(temp_dir), dynamic_metric_creation=True)

    @cm.collect(params_list=params_list)
    def sample(x, y):
        return a * x + y
    
    assert hasattr(cm, 'sample')
    assert hasattr(cm.sample, 'original_function')
    assert hasattr(cm.sample, 'params_list')
    assert cm.parameterized_metrics[0].__name__ == 'sample'
    assert 'sample_2_3' in cm.functions_dict
    assert 'sample_4_5' in cm.functions_dict
    assert 'sample' not in cm.functions_dict


    assert cm.sample.params_list == params_list

    assert np.array_equal(sample(2, 4), a * 2 + 4)
    assert np.array_equal(cm.sample(2, 4), a * 2 + 4)
    assert np.array_equal(cm.sample(2, 4, cache=True), a * 2 + 4)

    assert np.array_equal(cm.sample(2, 3), a_2_3)
    assert np.array_equal(cm.cache['sample_2_3'], a_2_3)

    shutil.rmtree(temp_dir)

    

if __name__ == '__main__':
    test_collect_1()
    test_collect_2()
    test_collect_3()