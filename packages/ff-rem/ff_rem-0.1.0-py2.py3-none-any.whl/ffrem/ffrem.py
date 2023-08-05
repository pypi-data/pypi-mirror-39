import logging

import numpy as np

from .transforms import compute_hankel_3d
from .util import detect_cut_off
from .util import shifted_stoddard_ford
from .util import calc_fitness
from .util import find_excluded_volume_cut
from .util import fit_excluded_volume


logger = logging.getLogger(__name__)


class FFREM:

    def __init__(self, target, r_min, r_max, alpha=1.0, beta=1.0, c=0.1,
                 eps_b=0.3, eps_gr=0.5, shift=True, k_excluded_volume=4,
                 r_excl=0.9, r_width=1000, k_max=100, k_width=1000, _r_min=0.1):
        """
        Initialize an instance of the Fourier-filtered Relative Entropy
        Minimization (FF-REM) method [1].

        [1] Carl S. Adorf, James Antonaglia, Julia Dshemuchadse, Sharon C. Glotzer,
            Submitted, arXiv: 1711.04154 [cond-mat.soft] (2017)

        :param target:
            The target pair correlation function: (r, g(r))
        :param r_min:
            The minimum range of the real-space potential.
        :param r_max:
            The maximum range of the real-space potential.
        :param alpha:
            The learning rate.
        :param beta:
            The inverse temperature.
        :param c:
            The strength of the low-pass Fourier filter.
        :param eps_b:
            The boundary for the real-space potential truncation.
        :param eps_gr:
            The boundary for the gradient of the real-space potential truncation.
        :param shift:
            Shift the potential to zero using the Stoddard-Ford algorithm.
        :param r_width:
            The width (number of discrete bins) of the real-space potential.
        :param k_max:
            The maximum k-value of the Fourier potential.
        :param k_width:
            The number of discrete bins used for the representation of the Fourier potential.
        :param _r_min:
            The internal minimum length employed for real-space transformations.
        """
        assert alpha > 0
        assert beta > 0
        assert _r_min < r_min < r_max
        self.k = np.linspace(0, k_max, k_width)
        self.r_min = r_min
        self.alpha = alpha
        self.beta = beta
        self.c = c
        self.eps_b = eps_b
        self.eps_gr = eps_gr
        self.shift = shift
        self.k_excluded_volume = k_excluded_volume
        self.r_excl = r_excl

        self._iteration = -1
        self.target = target
        self.last_response = None

        self._r = np.linspace(_r_min, r_max, r_width)
        self.ansatz_function(target)

    @property
    def iteration(self):
        return self._iteration

    def ansatz_function(self, target):
        "Determine the ansatz function."
        rt, grt = target
        assert rt.min() < self._r.min() < self._r.max() < rt.max()
        grt_ = np.interp(self._r, rt, grt)

        # Determine excluded volume cut
        eps = 0.1
        assert self._r[1] - self._r[0] < eps

        if self.r_excl is None:
            try:
                self.r_excl = find_excluded_volume_cut(self._r, grt_)
                self.r_excl = min(max(self.r_excl + eps, 0.7), 0.9)
            except RuntimeError as error:
                logger.warn(str(error))
                self.r_excl = 0.7
        i_cut = np.argmin(np.absolute(self._r - self.r_excl))

        # Calculte potential of mean force
        V0 = - self.beta * np.log(grt_)
        fit_excluded_volume(r=self._r, V=V0, i_cut=i_cut, k=self.k_excluded_volume)

        # need to truncate for numerical stability
        r_min = self.r_excl + 0.1
        i_min = np.argmin(np.absolute(rt - r_min))
        for i in range(len(V0) - i_min):
            if V0[i_min:].max() < 50:
                break
            i_min += 1
        else:
            raise RuntimeError("Unable to find correct truncation.")

        Vk0 = compute_hankel_3d(self._r[i_min:], V0[i_min:], self.k)
        Vk0_s = np.exp(-self.c * self.k) * Vk0
        self.Vk = Vk0_s.copy()

    def update(self, response, alpha=None):
        if alpha is None:
            alpha = self.alpha
        rt, grt = self.target
        ri, gri = response
        gri_ = np.interp(rt, ri, gri)
        hr_delta = gri_ - grt
        hk_delta = compute_hankel_3d(rt, hr_delta, self.k)

        self.Vk += alpha * self.beta * hk_delta * np.exp(- self.c * self.k)
        self.last_response = response
        self._iteration += 1
        return np.linalg.norm(hk_delta)

    def k_potential(self):
        return np.vstack((self.k, self.Vk))

    def _potential(self):
        k, Vk = self.k_potential()
        V = compute_hankel_3d(k, Vk, self._r)
        r_cut = self.r_excl or 0.5
        i_cut = np.argmin(np.absolute(self._r - r_cut))
        fit_excluded_volume(r=self._r, V=V, i_cut=i_cut, k=self.k_excluded_volume)
        return np.vstack((self._r, V))

    def potential(self, r_min=None):
        if r_min is None:
            r_min = self.r_min
        r, V = self._potential()
        try:
            i_cut = detect_cut_off(r, V, r_min=self.r_min, eps_b=self.eps_b, eps_gr=self.eps_gr)
        except RuntimeError as error:
            logger.warn(str(error))
            delta_r0 = 1.0
            assert r.max() > delta_r0
            eps = 0.01
            r0 = r.max() - delta_r0
            a = - np.log(eps) / delta_r0
            V /= (1 + np.exp(a * (r - r0)))
        else:
            r = np.copy(r[:i_cut])
            V = np.copy(V[:i_cut])
        if self.shift:
            V = shifted_stoddard_ford(r, V)
        F = - np.gradient(V, r[1] - r[0])
        return np.vstack((r, V, F))

    def fitness(self):
        "Return the fitness of the last iteration as numpy array."
        assert self.iteration >= 0
        return calc_fitness(self.target, self.last_response)

    def complexity(k, Vk):
        return np.trapz(np.power(k * Vk, 2), x=k) / k.max()

    def to_dict(self):
        return {
            '_version': 0,
            '_r_min': float(self._r.min()),
            'r_min': float(self.r_min),
            'r_max': float(self._r.max()),
            'r_width': len(self._r),
            'alpha': float(self.alpha),
            'beta': float(self.beta),
            'c': float(self.c),
            'eps_b': float(self.eps_b),
            'eps_gr': float(self.eps_gr),
            'shift': bool(self.shift),
            'k_excluded_volume': int(self.k_excluded_volume),
            'k_max': float(self.k.max()),
            'k_width': len(self.k),
        }

    @classmethod
    def from_dict(cls, target, p):
        assert p.pop('_version') >= 0
        return cls(target=target, **p)
