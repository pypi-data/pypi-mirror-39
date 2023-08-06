from typing import Union, List, Text

import numpy as np
from fiend.pulseconfig_parser.parameter import *
from scipy.integrate import quad
import logging

Param_or_float = Union[Parameter, float]
Array = Union[List, np.array]
Array_or_float = Union[np.array, float]


def _conv_type(x):
    if isinstance(x, Parameter):
        return x
    else:
        return Parameter(x, True)


class SingleColorLaserPulse:

    """
    This class represents a single-color laser pulse. Internally, it's
    implemented as vector potential.
    """

    def __init__(self, A: Param_or_float,
                 w: Param_or_float,
                 k: Param_or_float,
                 tau: Param_or_float,
                 phi: Param_or_float,
                 sigma: Param_or_float):
        A = _conv_type(A)
        w = _conv_type(w)
        k = _conv_type(k)
        tau = _conv_type(tau)
        phi = _conv_type(phi)
        sigma = _conv_type(sigma)

        self.params = np.array([A, w, k, tau, phi, sigma])
        self.A = self.params[0]
        self.w = self.params[1]
        self.k = self.params[2]
        self.tau = self.params[3]
        self.phi = self.params[4]
        self.sigma = self.params[5]
        self.logger = logging.getLogger('')
        self.num_variables = 0
        for param in self.params:
            if(not param.is_const):
                self.num_variables += 1

    def T(self) -> float:
        return 2 * self.sigma

    def get_copy(self):
        pulse = SingleColorLaserPulse(
            self.A, self.w, self.k, self.tau, self.phi, self.sigma)
        return pulse

    def set_vars(self, varlist: Union[List[float], np.array]) -> None:
        assert len(
            varlist) == self.num_variables, "Invalid number of parameters for LaserPulse"
        n = 0
        for i in range(len(self.params)):
            if(not self.params[i].is_const):
                self.params[i] = varlist[n]
                n = n + 1
        assert n == len(varlist), "Invalid number of parameters for LaserPulse"
        self.A = self.params[0]
        self.w = self.params[1]
        self.k = self.params[2]
        self.tau = self.params[3]
        self.phi = self.params[4]
        self.sigma = self.params[5]

    def get_vars_str(self) -> Text:
        return "    Pulse: A=%.6f, w=%.6f, k=%.6f, τ=%.6f, φ=%.6f, σ=%.6f" % (
            self.A, self.w, self.k, self.tau, self.phi, self.sigma)

    def print_vars(self) -> None:
        self.logger.info("    Pulse: A=%.2f, w=%.4f, k=%.2f, τ=%.2f, φ=%.2f, σ=%.2f" % (
            self.A, self.w, self.k, self.tau, self.phi, self.sigma))

    def carrier(self, t: Array_or_float) -> Array_or_float:
        arg = (self.w + self.k * (t - self.tau)) * (t - self.tau) + self.phi
        if isinstance(arg, float):
            return np.cos(arg)
        elif isinstance(arg, np.ndarray):
            return np.cos(arg.astype(float))
        else:
            raise RuntimeError("Unsupported type of 'arg'")

    def envelope(self, t: Array_or_float) -> Array_or_float:
        fun = np.vectorize(self._envelope_core)
        return fun(t)

    def _envelope_core(self, t: float) -> float:
        if np.fabs(t - self.tau) < self.T():
            return np.exp(-np.log(2.0) * ((t - self.tau) / self.sigma)
                          ** 2 / (1 - (t - self.tau)**2 / self.T()**2))
        else:
            return 0.0

    def _sin_carrier(self, t: Array_or_float) -> Array_or_float:
        return np.sin((self.w + self.k * (t - self.tau))
                      * (t - self.tau) + self.phi)

    def partial_t_carrier(self, t: Array_or_float) -> Array_or_float:
        return -(2 * self.k * (t - self.tau) + self.w) * self._sin_carrier(t)

    def partial_t_envelope(self, t: Array_or_float) -> Array_or_float:
        fun = np.vectorize(self._partial_t_envelope_core)
        return fun(t)

    def _partial_t_envelope_core(self, t: float) -> float:
        if np.fabs(t - self.tau) < self.T():
            return -2 * np.log(2) * self.envelope(t) * (t - self.tau) / (self.sigma**2 * (1 - ((t - self.tau) / self.T())
                                                                                          ** 2)) * (1 + ((t - self.tau) / self.T())**2 * 1.0 / (1 - ((t - self.tau) / self.T())**2))
        else:
            return 0.0

    def __call__(self, t: Array_or_float) -> Array_or_float:
        return self.A / self.w * self.envelope(t) * self.carrier(t)

    def beginning_of_pulse(self) -> float:
        return self.tau - 2 * self.sigma

    def end_of_pulse(self) -> float:
        return self.tau + 2 * self.sigma

    def get_number_of_variables(self) -> int:
        return self.num_variables

    def electric_field(self, t: Array_or_float) -> Array_or_float:
        return -self.A / self.w * \
            (self.partial_t_carrier(t) * self.envelope(t) +
             self.partial_t_envelope(t) * self.carrier(t))

    def is_A_const(self) -> bool:
        return self.A.is_const

    def is_w_const(self) -> bool:
        return self.w.is_const

    def is_k_const(self) -> bool:
        return self.k.is_const

    def is_tau_const(self) -> bool:
        return self.tau.is_const

    def is_phi_const(self) -> bool:
        return self.phi.is_const

    def is_sigma_const(self) -> bool:
        return self.sigma.is_const

    def partial_A(self, t: Array_or_float) -> Array_or_float:
        return self.__call__(t) / self.A

    def partial_w(self, t: Array_or_float) -> Array_or_float:
        return -self.envelope(t)\
            * self.A / (self.w**2)\
            * (self._sin_carrier(t) * (t - self.tau)
               + self.carrier(t))

    def partial_k(self, t: Array_or_float) -> Array_or_float:
        return -(t - self.tau)**2 * self.envelope(t) * self._sin_carrier(t)\
            * self.A / self.w

    def partial_tau(self, t: Array_or_float) -> Array_or_float:
        return -self.A / self.w * self.envelope(t) * self._sin_carrier(t)\
            * (-2 * self.k * (t - self.tau) - self.w) \
            + self.A / self.w * self.envelope(t) * self.carrier(t)\
            * 32 * self.sigma * (t - self.tau)**2 * np.log(2)\
            / (-4 * self.sigma**2 + (t - self.tau)**2)**2

    def partial_phi(self, t: Array_or_float) -> Array_or_float:
        return -self.A / self.w * self.envelope(t) * self._sin_carrier(t)

    def partial_sigma(self, t: Array_or_float) -> Array_or_float:
        return self.envelope(t) * self.carrier(t) * self.A / self.w\
            * 32 * self.sigma * (t - self.tau)**2 * np.log(2)\
            / (-4 * self.sigma**2 + (t - self.tau)**2)**2
