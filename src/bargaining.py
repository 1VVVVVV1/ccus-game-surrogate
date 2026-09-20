"""Generalized Nash bargaining from reservation values."""
from dataclasses import dataclass
from math import nan
from .config import CONFIG


@dataclass(frozen=True)
class Bargain:
    matched: bool
    price: float


def bargain(ask, bid, weight=0.5):
    if ask > bid:
        return Bargain(False, nan)
    return Bargain(True, ask + weight * (bid - ask))


def operating_bargains(mode, carbon_price, scenario):
    carbon_value = carbon_price * scenario["effective_abatement_fraction"]
    c_c = CONFIG["carbon_source"]["variable_opex_per_ton"]
    u = CONFIG["utilization_storage"]
    bid = u["utilization_revenue_per_ton"] - u["utilization_cost_per_ton"]
    if mode == "STATE_OWNED":
        return Bargain(False, nan), Bargain(False, nan)
    transport = (scenario["transport_market_price"] if mode == "TRANSFER"
                 else CONFIG["transport_market"]["variable_opex_per_ton"])
    co2 = bargain(c_c + transport - carbon_value, bid,
                  CONFIG["bargaining"]["co2_seller_weight"])
    storage = Bargain(False, nan)
    if mode == "TRANSFER":
        storage = bargain(max(0.0, u["storage_cost_per_ton"] - scenario["storage_subsidy"]),
                          carbon_value - c_c - transport,
                          CONFIG["bargaining"]["storage_provider_weight"])
    return co2, storage
