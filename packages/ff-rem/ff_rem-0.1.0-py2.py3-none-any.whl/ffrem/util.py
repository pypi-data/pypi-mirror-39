import freud
import numpy as np
from scipy.signal import argrelextrema


def calc_rdf(traj, type_a, type_b, r_cut, delta_r=0.01):
    rdf = freud.density.RDF(r_cut, delta_r)
    for frame in traj:
        types = frame.particles.types
        id_a, id_b = types.index(type_a), types.index(type_b)
        box = freud.box.Box.from_box(frame.configuration.box)
        typeid = frame.particles.typeid
        pos_a = frame.particles.position[typeid == id_a]
        pos_b = frame.particles.position[typeid == id_b]
        rdf.accumulate(box, pos_a, pos_b)
    return np.vstack((rdf.R, rdf.RDF))


def detect_cut_off(r, V, r_min, eps_b, eps_gr):
    assert eps_b >= 0 and eps_gr >= 0
    if eps_b > 0:
        dV = np.gradient(V, r)
        candidates = np.logical_and(
            r >= r_min,
            np.logical_and(
                np.absolute(V) <= eps_b,
                np.absolute(dV) <= eps_gr))
        if candidates.any():
            minima = argrelextrema(V[candidates], np.less)
            maxima = argrelextrema(V[candidates], np.greater)
            extrema = np.array(sorted(set(np.concatenate(minima + maxima))))
            if len(extrema):
                r_cut = r[candidates][extrema].min()
            else:   # use value with minimal gradient if no extrema found
                r_cut = r[candidates][np.absolute(dV[candidates]).argmin()]
            return np.argmin(np.absolute(r-r_cut))
    else:
        zero_crossings = np.where(np.diff(np.sign(V)))[0]
        for i, i_cut in enumerate(zero_crossings):
            if r[i_cut] >= r_min:
                return i_cut
    raise RuntimeError("No suitable cut-off!")


def shifted_stoddard_ford(r, V):
    "Shift the potential according to the Stoddard-Ford method."
    F = - np.gradient(V, r)
    V += (r - r[-1]) * F[-1]
    V -= V[-1]
    return V


def calc_fitness(target, response):
    "Calculate the fitness between target and response function."
    r = np.asarray(response)
    t = np.asarray(target)
    r_ = t[0], np.interp(t[0], r[0], r[1])
    a = np.abs(r_[1] - t[1])
    b = np.abs(r_[1]) + np.abs(t[1])
    return 1.0 - (np.sum(a) / np.sum(b))


def find_excluded_volume_cut(r, gr):
    """Determine where the excluded volume cut should be made."""
    assert len(r) == len(gr)
    i_min = len(gr)
    while i_min > 0:
        if gr[i_min - 1] <= 0:
            break
        i_min -= 1
    else:
        raise RuntimeError("Did not find i_min.")
    return r[i_min]


def fit_excluded_volume(r, V, i_cut, k=12, a_min=0.0, a_max=10.0, dr=0.02):
    # Determine the differentation window length.
    di = int(dr // (r[1] - r[0]))
    di += 1 - di % 2
    dr = r[di] - r[0]

    # Determine the fitting parameters *a* and *b*.
    dvdr_c = (V[i_cut + di] - V[i_cut - di]) / (2 * dr)
    r_c = r[i_cut + di // 2]
    V_c = V[i_cut + di // 2]
    a = - pow(r_c, k + 1) * dvdr_c / k
    good_range = a_min < a <= a_max
    b = V_c - a * pow(r_c, -k)
    assert not np.isnan(a) or np.isnan(b)

    # Generate and stitch the potential with excluded volume.
    V[:i_cut] = a * np.power(r[:i_cut], -k) + b
    if not good_range:
        raise RuntimeError(
            "Potential not within acceptable range. "
            "The excluded volume cut is at {}, with a={} ({}, {}). ".format(r_c, a, a_min, a_max),
            np.vstack((r, V)))
