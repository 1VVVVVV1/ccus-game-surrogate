import math
import numpy as np
import pytest
from src.carbon_tree import carbon_tree


def test_physical_tree():
    prices, u, d, p = carbon_tree(2.0)
    assert u > 1
    assert d == 1/u
    assert 0 < p < 1
    assert prices[0,0] == 96.23*2
    assert u*d == d*u
    assert np.isfinite(prices).sum() == 496
    assert p*u + (1-p)*d == pytest.approx(math.exp(.04))
    assert prices[2,1] == pytest.approx(prices[0,0])
