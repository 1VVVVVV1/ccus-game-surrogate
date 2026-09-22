"""Linear axis calibration and cumulative Li variable costs; no curve fitting."""
import math


LI_FRESH_TOTAL_TONNES = 10.68e6


def pixel_to_value(pixel_y, top_px, bottom_px, minimum, maximum):
    if bottom_px <= top_px or maximum <= minimum:
        raise ValueError("Invalid axis calibration")
    return minimum + (bottom_px - pixel_y) * (maximum - minimum) / (bottom_px - top_px)


def point_interval(pixel_y, marker_height_px, top_px, bottom_px, minimum, maximum):
    radius = marker_height_px / 2 + 1
    return tuple(pixel_to_value(y, top_px, bottom_px, minimum, maximum)
                 for y in (pixel_y, pixel_y + radius, pixel_y - radius))


def li_variable_opex_usd_per_fresh_tonne(recycled_total_tonnes, oil_total_bbl):
    if not all(math.isfinite(x) and x >= 0 for x in
               (recycled_total_tonnes, oil_total_bbl)):
        raise ValueError("Cumulative quantities must be finite and nonnegative")
    fresh = LI_FRESH_TOTAL_TONNES
    total = .085 * (10.2 * (fresh + recycled_total_tonnes)
                   + 38 * recycled_total_tonnes + 22 * oil_total_bbl) + 8.2 * oil_total_bbl
    return total / fresh
