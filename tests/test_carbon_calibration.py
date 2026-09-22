import math

import pytest

from src.carbon_calibration import fit_official_gbm


def test_calendar_gaps_and_protocol_variance():
    dates = ['2021-07-16', '2021-07-19', '2021-07-20']
    prices = [50.0, 52.0, 51.0]
    result, diagnostic = fit_official_gbm(dates, prices)
    r1, r2 = math.log(52/50), math.log(51/52)
    dt1, dt2 = 3/365.25, 1/365.25
    m = (r1+r2)/(dt1+dt2)
    variance = ((r1-m*dt1)**2/dt1+(r2-m*dt2)**2/dt2)/2
    assert result['mu'] == pytest.approx(m+variance/2)
    assert result['sigma'] == pytest.approx(math.sqrt(variance))
    assert result['P0'] == 51
    assert diagnostic[0]['dt_years'] == dt1


def test_constant_prices_keep_zero_returns():
    result, diagnostic = fit_official_gbm(['2021-07-16', '2021-07-19'], [50, 50])
    assert result['mu'] == result['sigma'] == 0
    assert len(diagnostic) == 1


@pytest.mark.parametrize('dates,prices', [
    (['2021-07-16'], [50]),
    (['2021-07-16', '2021-07-16'], [50, 51]),
    (['2021-07-19', '2021-07-16'], [50, 51]),
    (['2021-07-16', '2021-07-19'], [50, 0]),
    (['2021-07-16', '2021-07-19'], [50, float('nan')]),
])
def test_invalid_observations_are_rejected(dates, prices):
    with pytest.raises(ValueError):
        fit_official_gbm(dates, prices)
