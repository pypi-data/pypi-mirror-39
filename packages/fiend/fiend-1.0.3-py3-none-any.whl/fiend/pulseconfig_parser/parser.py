"""
DAMDIDAM
"""

import configparser
import random
import re
import os
import errno
from typing import Text, Union, List, no_type_check, Dict, Tuple

import numpy as np
from fiend.pulseconfig_parser.laser import *


@no_type_check
def _parse_parameter(string):
    """Parses input string either to a float or list of colon-separated floats"""
    try:
        return float(string)
    except BaseException:
        prange = string.split('#')[0]
        prange = prange.split(':')
        prange = [float(d) for d in prange]
        return prange
    else:
        raise Exception("Invalid option value: " + string)

# Parses a '[PulseN]' section of the input file
#
# Input:
#   parser    an instance of the parser
#   pulsename name of the section to be parsed
# Output:
#   config    dictionary of the laser parameters/variables
#


def _parse_pulse(parser, pulsename: str) -> Dict[str, Union[float,
                                                            Tuple[float, float]]]:
    params = parser.items(pulsename)
    for key in params:
        if key[0] not in ['a', 'w', 'k', 'tcenter', 'cep', 'fwhm']:
            raise Exception("No such option: " + pulsename + "::" + key[0])

    config = {}
    config['A'] = _parse_parameter(parser.get(pulsename, "A"))
    config['w'] = _parse_parameter(parser.get(pulsename, "w"))
    config['k'] = _parse_parameter(parser.get(pulsename, "k"))
    config['tau'] = _parse_parameter(parser.get(pulsename, "tcenter"))
    config['phi'] = _parse_parameter(parser.get(pulsename, "cep"))
    config['sigma'] = _parse_parameter(parser.get(pulsename, "fwhm"))
    return config

# Parses the input file
#
# Input:
#   path   folder from which we look for the file 'input'
# Output:
#   simulation_config   dictionary of parameters for the simulation of TDSE
#   laser               an instance of the laser class
#   oct_config          dictionary of parameters for the optimization routines
#   variable_limits     upper and lower bound for optimization parameters
#   initial_values      a quess for the initial values
# false/true          true if we should enforce constraint of the zero
# electric field


def parse_laser(path: Text) -> Laser:
    parser = configparser.ConfigParser()
    out = parser.read(path)
    if len(out) == 0:
        raise RuntimeError("Input file does not exist: " +
                           path)

    # Get names of all sections which define a single-color pulse
    pulsenames = filter(lambda item: item[0:5] == "Pulse", parser.sections())
    variable_limits = np.empty([0, 2])
    initial_values = np.array([])
    laser = Laser()
    random.seed()
    # Parse each laser pulse and add it to the total laser
    for pulsename in pulsenames:
        pparams = _parse_pulse(parser, pulsename)
        if(isinstance(pparams['A'], float)):
            A = Parameter(pparams['A'], True)
        else:
            A = Parameter(random.uniform(
                pparams['A'][0], pparams['A'][1]), False)
            initial_values = np.append(initial_values, A.val)
            variable_limits = np.concatenate(
                (variable_limits, [pparams['A']]))
        if(isinstance(pparams['w'], float)):
            w = Parameter(pparams['w'], True)
            wmin = w.val
        else:
            w = Parameter(random.uniform(
                pparams['w'][0], pparams['w'][1]), False)
            wmin = pparams['w'][0]
            initial_values = np.append(initial_values, w.val)
            variable_limits = np.concatenate(
                (variable_limits, [pparams['w']]))
        if(isinstance(pparams['k'], float)):
            k = Parameter(pparams['k'], True)
        else:
            k = Parameter(random.uniform(
                pparams['k'][0], pparams['k'][1]), False)
            initial_values = np.append(initial_values, k.val)
            variable_limits = np.concatenate(
                (variable_limits, [pparams['k']]))
        if(isinstance(pparams['tau'], float)):
            tau = Parameter(pparams['tau'], True)
        else:
            tau = Parameter(random.uniform(
                pparams['tau'][0], pparams['tau'][1]), False)
            initial_values = np.append(initial_values, tau.val)
            variable_limits = np.concatenate(
                (variable_limits, [pparams['tau']]))
        if(isinstance(pparams['phi'], float)):
            phi = Parameter(pparams['phi'], True)
        else:
            phi = Parameter(random.uniform(
                pparams['phi'][0], pparams['phi'][1]), False)
            initial_values = np.append(initial_values, phi.val)
            variable_limits = np.concatenate(
                (variable_limits, [pparams['phi']]))
        if(isinstance(pparams['sigma'], float)):
            sigma = Parameter(pparams['sigma'], True)
            sigmamin = sigma.val
        else:
            sigma = Parameter(random.uniform(
                pparams['sigma'][0], pparams['sigma'][1]), False)
            sigmamin = pparams['sigma'][0]
            initial_values = np.append(initial_values, sigma.val)
            variable_limits = np.concatenate(
                (variable_limits, [pparams['sigma']]))
        laser.add_pulse(SingleColorLaserPulse(A, w, k, tau, phi, sigma))

    return laser
