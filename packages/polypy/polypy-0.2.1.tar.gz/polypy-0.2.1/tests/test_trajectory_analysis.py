import sys 

sys.path.append('/home/adam/data/adam/progs/PolyPy/PolyPy/polypy/')
import TrajectoryAnalysis as ta
import numpy as np
import numpy.testing as npt
from numpy.testing import assert_almost_equal, assert_equal

def test_distances():
    distance = ta.distances(10, 5)
    expect = 5
    assert distance == expect

def test_msd_stats():
    data = np.genfromtxt("tests/data/MSD.txt", dtype="float")
    a, b, c, d = ta.msd_stats(data[:,0], data[:,1], data[:,2], data[:,3], data[:,4])
    assert_almost_equal(a, 100.0)
    assert_almost_equal(b, 10.0)
    assert_almost_equal(c, 10.0)
    assert_almost_equal(d, 10.0)

def test_diffusion_coefficient():
    a, b, c, d = ta.diffusion_coefficient(24, 25, 14, 73)
    assert_almost_equal(a, 40)
    assert_almost_equal(b, 125)
    assert_almost_equal(c, 70)
    assert_almost_equal(d, 365)

def test_system_volume():
    data = np.genfromtxt("tests/data/Volume.txt", dtype=float)
    expected_vol = np.array([3375.000, 4096.000, 4913.000, 5832.000, 6859.000, 8000.000, 9261.000, 10648.000, 12167.000, 13824.000])
    expected_time = np.arange(10)
    a, b = ta.system_volume(data, 10, 1)

    assert_almost_equal(expected_vol, a)
    assert_almost_equal(expected_time, b)

def test_conductivity():
    a = ta.conductivity(1, 2, 3, 4)
    a = round(a, 0)
    expected = 697219
    assert_almost_equal(a, expected)
    
def test_square_distance():
    data = np.genfromtxt("tests/data/SD.txt", dtype="float")
    a = ta.square_distance(data, 1)
    b = ta.square_distance(np.array([1, 2, 3]), 0)
    expected_a = np.array([102, 408, 918, 1632, 2550, 3672, 4998, 6528, 8262, 10200])
    expected_b = 14
    assert_almost_equal(a, expected_a)
    assert b == expected_b

    
    