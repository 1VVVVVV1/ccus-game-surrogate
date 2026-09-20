"""Protocol-frozen scrambled Sobol design and scenario-level split."""
import numpy as np
import pandas as pd
from scipy.stats import qmc
from .config import FEATURES, DOMAIN


def design():
    sample = qmc.Sobol(d=6, scramble=True, seed=20260921).random_base2(m=12)
    limits = np.asarray(DOMAIN)
    frame = pd.DataFrame(qmc.scale(sample, limits[:,0], limits[:,1]), columns=FEATURES)
    frame.insert(0, "scenario_id", np.arange(4096))
    return frame


def scenario_split():
    permutation = np.random.default_rng(42).permutation(4096)
    split = np.empty(4096, dtype=object)
    split[permutation[:2868]] = "train"
    split[permutation[2868:3482]] = "validation"
    split[permutation[3482:]] = "test"
    return pd.DataFrame({"scenario_id": np.arange(4096), "split": split})
