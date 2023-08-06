#!/usr/bin/env python3

import logging
import numpy as np
from typing import Union, Text, List
from scipy.integrate import simps, quadrature

from fiend.pulseconfig_parser.parameter import *
from fiend.pulseconfig_parser.singlecolorlaserpulse import *

# Class representing a total laser pulse composed of many single-color
# channels (singlecolorlaserpulse.py)


class Laser:
    def __init__(self):
        self.number_of_variables = 0
        self.variable_limits = np.array([])
        self.pulses = np.array([])
        self.partial_derivative_functions = np.empty([0, 2])
        self.varlist = np.array([])
        self.logger = logging.getLogger('')

    def get_copy(self):
        laser = Laser()
        for pulse in self.pulses:
            laser.add_pulse(pulse.get_copy())
        return laser

    def get_number_of_pulses(self) -> int:
        return len(self.pulses)

    def print_parameters(self) -> None:
        vals = (self.end_of_pulse() - self.beginning_of_pulse(),
                self.duration_fwhm(),
                self.duration_intensity_fwhm(),
                self.calculate_fluence(),
                self.max_field())
        self.logger.info(
            "Laser, duration = %.2f, fwhm (field) = %.2f, fwhm (intensity) = %.2f, fluence = %e, peak field = %.3f" % vals)
        for i in range(len(self.pulses)):
            self.pulses[i].print_vars()

    def get_parameters_str(self) -> Text:
        string = "Laser, duration = %.2f, fwhm (field) = %.2f, fwhm (intensity) = %.2f, fluence = %e, peak field = %.3f\n" % (self.end_of_pulse(
        ) - self.beginning_of_pulse(), self.duration_fwhm(), self.duration_intensity_fwhm(), self.calculate_fluence(), self.max_field())
        for i in range(len(self.pulses)):
            string = string + self.pulses[i].get_vars_str() + "\n"
        return string

    def calculate_fluence(self, dt: float = 0.05) -> float:
        T0 = self.beginning_of_pulse()
        Tmax = self.end_of_pulse()

        def field2(t): return self.electric_field(t)**2
        return quadrature(field2, T0, Tmax, maxiter=200, tol=1e-4)[0]

    def set_vars(self, varlist: List[float]) -> None:
        self.varlist = np.array(varlist)
        assert self.number_of_variables == len(
            varlist), "Wrong number of variables given"
        for i in range(len(self.pulses)):
            pvars = self.get_pulse_variables(varlist, i)
            self.pulses[i].set_vars(pvars)

    def __call__(self, t: Union[List[float],
                                np.array,
                                float]) -> Union[List[float],
                                                 np.array,
                                                 float]:
        if(isinstance(t, float)):
            A = 0
        else:
            A = np.zeros(len(t))
        for i in range(len(self.pulses)):
            A += self.pulses[i](t)
        return A

    def add_pulse(self, pulse: SingleColorLaserPulse) -> None:
        self.pulses = np.append(self.pulses, pulse)
        self.number_of_variables += pulse.get_number_of_variables()
        n = len(self.pulses) - 1
        if(not pulse.A.is_const):
            self.partial_derivative_functions = np.concatenate(
                (self.partial_derivative_functions, [[n, pulse.partial_A]]))
        if(not pulse.w.is_const):
            self.partial_derivative_functions = np.concatenate(
                (self.partial_derivative_functions, [[n, pulse.partial_w]]))
        if(not pulse.k.is_const):
            self.partial_derivative_functions = np.concatenate(
                (self.partial_derivative_functions, [[n, pulse.partial_k]]))
        if(not pulse.tau.is_const):
            self.partial_derivative_functions = np.concatenate(
                (self.partial_derivative_functions, [[n, pulse.partial_tau]]))
        if(not pulse.phi.is_const):
            self.partial_derivative_functions = np.concatenate(
                (self.partial_derivative_functions, [[n, pulse.partial_phi]]))
        if(not pulse.sigma.is_const):
            self.partial_derivative_functions = np.concatenate(
                (self.partial_derivative_functions, [[n, pulse.partial_sigma]]))

    def get_pulse_variables(self, varlist: Union[List[float], np.array],
                            pulse_number: int) -> np.array:
        assert pulse_number < len(self.pulses), "Not that many pulses."
        i_begin = 0
        for i in range(pulse_number):
            i_begin += self.pulses[i].get_number_of_variables()

        i_end = i_begin + self.pulses[pulse_number].get_number_of_variables()
        return self.varlist[i_begin:i_end]

    def beginning_of_pulse(self) -> float:
        begin = self.pulses[0].end_of_pulse()
        for i, pulse in enumerate(self.pulses):
            if(pulse.beginning_of_pulse() < begin):
                begin = pulse.beginning_of_pulse()
        return begin

    def end_of_pulse(self) -> float:
        end = self.pulses[0].beginning_of_pulse()
        for i, pulse in enumerate(self.pulses):
            if(pulse.end_of_pulse() > end):
                end = pulse.end_of_pulse()
        return end

    def duration(self) -> float:
        return self.end_of_pulse() - self.beginning_of_pulse()

    def duration_fwhm(self) -> float:
        Ta = self.beginning_of_pulse()
        Tb = self.end_of_pulse()
        T = np.linspace(Ta, Tb, 1000)
        field = np.fabs(self.electric_field(T))
        Emax = np.max(field)
        idx = np.where(field > 0.5 * Emax)[0]
        if np.isclose(Emax, 0.0):
            return 0.0
        return T[idx[-1]] - T[idx[0]]

    def duration_intensity_fwhm(self) -> float:
        Ta = self.beginning_of_pulse()
        Tb = self.end_of_pulse()
        T = np.linspace(Ta, Tb, 1000)
        field = np.fabs(self.electric_field(T))
        Imax = np.max(field**2)
        idx = np.where(field**2 > 0.5 * Imax)[0]
        if np.isclose(Imax, 0.0):
            return 0.0
        return T[idx[-1]] - T[idx[0]]

    def max_field(self) -> float:
        T0 = self.beginning_of_pulse()
        Tmax = self.end_of_pulse()
        field = self.electric_field(np.linspace(T0, Tmax, 1000))
        return np.fabs(field).max()

    def partial_deriv(self, t: Union[List[float], np.array, float],
                      var_number: int):
        assert var_number < len(
            self.partial_derivative_functions), "Not that many variables"
        n, func = self.partial_derivative_functions[var_number]
        return func(t)

    def electric_field(self, t: Union[List[float], np.array, float]):
        field = np.zeros_like(t)
        for pulse in self.pulses:
            field += pulse.electric_field(t)
        return field
