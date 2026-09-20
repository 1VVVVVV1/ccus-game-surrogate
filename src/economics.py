"""Annual profits in million CNY; flow uses pre-investment built states."""
from dataclasses import dataclass
import math
from .bargaining import operating_bargains
from .config import CONFIG


@dataclass(frozen=True)
class Outcome:
    profits: tuple  # C, U, T, system; SOE C/U are decision values, T is inapplicable
    q_u: float
    q_s: float
    co2_price: float
    storage_fee: float
    co2_matched: bool
    storage_matched: bool
    accounting_error: float


def stage_outcome(mode, scenario, carbon_price, state, action):
    x_c, x_u = state
    d_c, d_u = action
    c = CONFIG["carbon_source"]
    tr = CONFIG["transport_market"]
    u = CONFIG["utilization_storage"]
    co2, storage = operating_bargains(mode, carbon_price, scenario)
    base = CONFIG["co2_quantity"]["Q_bar"] * x_c * x_u
    xi = CONFIG["co2_quantity"]["utilization_fraction"]
    q_u = xi * base * (co2.matched if mode != "STATE_OWNED" else 1)
    q_s = (1-xi) * base * (storage.matched if mode == "TRANSFER" else 1)
    quantity = q_u + q_s
    rc = carbon_price * scenario["effective_abatement_fraction"] * quantity
    oc = c["fixed_opex"] * x_c + c["variable_opex_per_ton"] * quantity
    ou = u["fixed_opex"] * x_u + u["utilization_cost_per_ton"] * q_u + u["storage_cost_per_ton"] * q_s
    ct = tr["fixed_opex_if_active"] * (quantity > 0) + tr["variable_opex_per_ton"] * quantity
    ic = c["capex_initial"] * scenario["capex_C_multiplier"] * d_c
    iu = u["capex_initial"] * scenario["capex_U_multiplier"] * d_u
    oil = u["utilization_revenue_per_ton"] * q_u
    subsidy = scenario["storage_subsidy"] * q_s
    direct = rc + oil + subsidy - oc - ou - ct - ic - iu
    # A failed bargain has a NaN quote and zero flow; never multiply NaN by zero.
    payment_u = co2.price * q_u if co2.matched else 0.0
    payment_s = storage.price * q_s if storage.matched else 0.0
    if mode == "TRANSFER":
        transport_payment = scenario["transport_market_price"] * quantity
        pc = rc + payment_u - transport_payment - payment_s - oc - ic
        pu = oil - payment_u + payment_s + subsidy - ou - iu
        pt = transport_payment - ct
        system = pc + pu + pt
        error = abs(system - direct)
    elif mode == "JOINT_VENTURE":
        pool = rc + payment_u + subsidy - oc - ct - u["fixed_opex"] * x_u - u["storage_cost_per_ton"] * q_s - ic - iu
        application = oil - payment_u - u["utilization_cost_per_ton"] * q_u
        shares = CONFIG["joint_venture"]
        pc = shares["theta_C"] * pool
        pt = shares["theta_T"] * pool
        pu = application + shares["theta_U"] * pool
        system = pool + application
        error = max(abs(system - (pc + pu + pt)), abs(system - direct))
    elif mode == "STATE_OWNED":
        system = direct
        pc = pu = system
        pt = math.nan
        error = abs(system - math.fsum((rc, oil, subsidy, -oc, -ou, -ct, -ic, -iu)))
    else:
        raise ValueError(mode)
    if not all(math.isfinite(v) for v in (pc, pu, system)) or (mode != "STATE_OWNED" and not math.isfinite(pt)):
        raise RuntimeError("NONFINITE_VALUE")
    if not error < 1e-10:
        raise RuntimeError(f"STATIC_ACCOUNTING_FAILURE: {error}")
    return Outcome((pc, pu, pt, system), q_u, q_s, co2.price, storage.price,
                   co2.matched, storage.matched, error)
