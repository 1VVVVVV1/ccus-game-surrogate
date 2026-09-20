from math import isnan
from src.bargaining import bargain, operating_bargains
from src.config import BASELINE


def test_bargaining_reservations():
    assert bargain(100,200).price == 150
    assert bargain(100,200).matched
    assert not bargain(201,200).matched
    assert isnan(bargain(201,200).price)
    assert bargain(-300,-100).price == -200
    assert bargain(100,100).matched


def test_negative_co2_and_nonnegative_storage():
    co2, storage = operating_bargains("TRANSFER", 3000, BASELINE)
    assert co2.price < 0
    assert storage.price >= 0
