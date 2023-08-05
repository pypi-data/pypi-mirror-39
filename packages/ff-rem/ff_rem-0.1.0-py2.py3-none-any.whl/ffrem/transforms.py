import numpy as np
from scipy.special import jv


def compute_hankel_3d(r, f, k):
    """Compute the Hankel transformation in three dimensions."""
    assert r.shape == f.shape
    if k[0] == 0:
        F0 = (np.sqrt(2) / np.pi) * np.trapz(np.power(r, 2) * f, x=r)
        k = k[1:]
    else:
        F0 = None
    F = [np.trapz(np.power(r, 3/2) * f * jv(0.5, k_ * r), x=r) / np.sqrt(k_) for k_ in k]
    if F0 is None:
        return np.array(F)
    else:
        return np.concatenate(([F0], F))
