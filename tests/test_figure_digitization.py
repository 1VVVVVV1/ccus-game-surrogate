import csv
import json
import math
from pathlib import Path

import pytest

from src.figure_digitization import (LI_FRESH_TOTAL_TONNES, li_variable_opex_usd_per_fresh_tonne,
                                     pixel_to_value, point_interval)


FOLDER = Path(__file__).resolve().parents[1] / "results/source_backed_formal/source_audit/li_fig5_digitization"


@pytest.mark.parametrize("maximum", [2000, 3000])
@pytest.mark.parametrize("pixel,fraction", [(49, 1), (424.5, .5), (800, 0)])
def test_axis_ticks(pixel, fraction, maximum):
    assert pixel_to_value(pixel, 49, 800, 0, maximum) == maximum * fraction


def test_saved_points_are_only_fifteen_oil_markers():
    with (FOLDER / "li_fig5_digitized_points.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert [int(r["year"]) for r in rows] == list(range(1, 16))
    assert all(float(a["pixel_x"]) < float(b["pixel_x"]) for a, b in zip(rows, rows[1:]))
    assert {r["series"] for r in rows} == {"oil_production"}
    for r in rows:
        values = point_interval(float(r["pixel_y"]), float(r["marker_height_px"]), 49, 800, 0, 3000)
        assert values == tuple(float(r[k]) for k in ("central_value", "lower_value", "upper_value"))
        assert values[1] <= values[0] <= values[2]
        assert r["status"] == "MODEL_ASSUMPTION"


def test_text_total_not_overwritten_or_rescaled():
    metadata = json.loads((FOLDER / "digitization_metadata.json").read_text(encoding="utf-8"))
    totals = json.loads((FOLDER / "li_fig5_digitized_totals.json").read_text(encoding="utf-8"))
    assert totals["fresh_total_tonnes"] == LI_FRESH_TOTAL_TONNES == 10680000
    assert not metadata["fresh_curve_digitized"]
    assert not metadata["rescaling_applied"]
    assert totals["recycled_total_tonnes"] is None
    assert totals["variable_opex_usd_per_tonne"] is None


def test_only_cumulative_inputs_and_fresh_denominator():
    recycled, oil = [1e5, 2e5, 3e5], [2e5, 1e5, 4e5]
    value = li_variable_opex_usd_per_fresh_tonne(math.fsum(recycled), math.fsum(oil))
    assert value == li_variable_opex_usd_per_fresh_tonne(math.fsum(reversed(recycled)), math.fsum(reversed(oil)))
    expected = (.085 * (10.2 * (10680000 + 600000) + 38 * 600000 + 22 * 700000) + 8.2 * 700000) / 10680000
    assert value == expected
