import logging
from math import pi, exp, log

import numpy as np
import mpmath as mp

from ..compatutil import reduce
from .corrector_base import *
from ..database.thermo_data import *
from ..errors.error import *
from ..parsers.rxn_parser import *


# Constants.
_kJmol2eV = 0.01036427


class ThermodynamicCorrector(CorrectorBase):
    ''' Energy data corrector class

    :param owner: The kinetic model that own this solver
    :type owner: KineticModel
    '''
    def __init__(self, owner):
        super(ThermodynamicCorrector, self).__init__(owner)

        self._zpe_dict = {}
        self._enthalpy_dict = {}
        self._entropy_dict = {}

        # set logger object
        self.__logger = logging.getLogger('model.correctors.ThermodynamicCorrector')

    def shomate_correction(self, gas_name, T=None):
        """ Function to get energy correction dict for gas in model using Shomate equation.

        :param gas_name: The species site name of gas species, e.g. :obj:`CO_g`
        :type gas_name: str

        :param T: Temperature(K)
        :type T: float

        :return: The correction energy value
        :rtype: float

        Example::
            >>> shomate_correction("CO_g")
        """
        # {{{
        # Check gas name.
        formula = ChemFormula(gas_name)
        if formula.type() != "gas":
            # If it's not a gas, no correction.
            return 0.0

        # Set temperature.
        temperature = self._owner.temperature if T is None else T
        temperature_ref = 298.15

        # Nested functions for thermodynamic parameters.
        def H(T, params):
            A, B, C, D, E, F, G, H = params
            t = T/1000.0
            H = A*t + (B/2.0)*t**2 + (C/3.0)*t**3 + (D/4.0)*t**4 - E/t + F - H
            #kJ/mol
            return H

        def S(T, params):
            A, B, C, D, E, F, G, H = params
            t = T/1000.0
            S = A*np.log(t) + B*t + (C/2.0)*t**2 + (D/3.0)*t**3 - E/(2.0*t**2) + G  # J/mol*K
            return S

        def Cp(T, params):
            A, B, C, D, E, F, G, H = params
            t = T/1000.0
            Cp = A + B*t + C*t**2 + D*t**3 + E/(t**2)
            return Cp

        not_there = True
        for key in shomate_params.keys():
            gas_key, T_range = key.split(':')
            T_min, T_max = [float(t) for t in T_range.split('-')]

            # Check.
            if gas_key != gas_name:
                continue

            # Set flag.
            not_there = False

            if temperature >= T_min and temperature <= T_max:
                params = shomate_params[key]
                Cp_ref = Cp(temperature_ref, params)

                # deltaH(298-T) = shomate(T) - shomate(298)
                dH = H(temperature, params) - H(temperature_ref, params)
                dS = S(temperature, params)

                # dH = 298*Cp(298) + dH(298-T)
                dH = (temperature_ref*Cp_ref/1000.0 + dH)*(_kJmol2eV)  # eV
                dS = dS*(_kJmol2eV/1e3)  # eV/K

                #ZPE = sum(self.frequencies[gas_name])/2.0
                #free_energy = ZPE +  dH - temperature*dS

                free_energy = dH - temperature*dS
                enthalpy = dH
                entropy = -temperature*dS

            elif temperature < T_min and T_min < 300:
                params = shomate_params[key]
                Cp_ref = Cp(T_min, params)
                dS = S(T_min, params)
                dH = (temperature*Cp_ref/1000.0)*(_kJmol2eV)  # eV
                dS = dS*(_kJmol2eV/1e3)  # eV/K

                #ZPE = sum(self.frequencies[gas_name])/2.0
                free_energy = dH - temperature*dS
                enthalpy = dH
                entropy = -temperature*dS

            else:
                not_there = True

            if not not_there:
                break

        if not_there:
            msg = "No Shomate parameters specified for species '{}' at {}K"
            msg = msg.format(gas_name, temperature)
            self.__logger.warning(msg)
            #raise ValueError(msg)
            free_energy = 0.0

        return free_energy
        # }}}

    def entropy_correction(self, gas_name, m=None, p=None, T=None):
        """ Function to get free energy constributions from translational and 
        internal modes of species in **GAS**.

        :param gas_name: gas molecular formula
        :type gas_name: str

        :param m: absolute molecular mass, species mass by default
        :type m: float

        :param p: partial pressure (**bar**), model's pressure by default
        :type p: float

        :param T: temperature, model's temperature by default
        :param T: float

        Example::
            >>> m.corrector.entropy_correction('CO_g')
            >>> -1.1538116935108251
        """
        # {{{
        # Check gas name.
        formula = ChemFormula(gas_name)
        if formula.type() != "gas":
            #msg = "A gas name is expected, '{}' is recieved.".format(gas_name)
            #raise ParameterError(msg)
            return 0.0

        # Extract species_site and species name.
        species_site = formula.species_site()
        species_name = formula.species()

        # Match species in database
        rotation_included = species_site in rotation_temperatures
        vibration_included = species_site in vibration_temperatures

        if not (rotation_included and vibration_included):
            msg = "'{}' is not in database (thermodynamic_corrector.py)"
            msg = msg.format(species_site)
            self.__logger.warning(msg)
            #raise SpeciesError(msg)
            return 0.0

        # Set default parameter values.
        if m is None:
            parser = self._owner.parser
            m = parser.get_molecular_mass(species_name, absolute=True)
        if p is None:
            species_definitions = self._owner.species_definitions
            p = P0*species_definitions[species_site]['pressure']
        if T is None:
            T = self._owner.temperature

        # Calculate partition functions.

        # Translation partition functions.
        try:
            V = kB_J*T/p
        except ZeroDivisionError:
            msg_template = "Pressure of '{}' is 0.0, please check your input file."
            msg = msg_template.format(species_site)
            raise ZeroDivisionError(msg)

        qt = V*(2*pi*m*kB_J*T/(h_J**2))**(3/2.0)

        # Rotation partition function.
        sigma = rotation_temperatures[species_site]['sigma']
        thetas = rotation_temperatures[species_site]['theta']

        # Linear molecule.
        if len(thetas) == 1:
            theta, = thetas
            ratio = theta/T
            if ratio <= 0.01:
                qr = T/(sigma*theta)
            else:
                qr = T/(sigma*theta)*(1 + theta/(3*T) + theta**2/(15*T**2))
                if ratio >= 0.3:
                    msg_template = "T/theta = {:.3e} is larger than 0.3, big error may be expected"
                    msg = msg_template.format(ratio)
                    self.logger.warning(msg)
        # Nonlinear molecule.
        elif len(thetas) == 3:
            product = reduce(lambda x, y: x*y, thetas)
            qr = (pi)**0.5/sigma*(T**3/(product))**0.5

        # Vibration partition functions.
        thetas = vibration_temperatures[species_site]

        # Linear molecule.
        if len(thetas) == 1:
            theta, = thetas
            qv = exp(-theta/(2*T)) / (1 - exp(-theta/T))
        # Nonlinear molecule.
        else:
            temp_list = [1./(1 - exp(-theta/T)) for theta in thetas]
            qv = reduce(lambda x, y: x*y, temp_list)

        # Molecular partition function.
        q = qt*qr*qv

        return -kB_eV*T*log(q)  # eV
        # }}}

    def correct_relative_energies(self, relative_energies, method="shomate"):
        """ Function to correct given relative energies.

        :param relative_energies: Relative energies to be corrected
        :type relative_energies: dict

        :param method: Energy correctness method name, could be 'shomate' or 'entropy'
        :type method: str
        """
        if method == "shomate":
            correct_func = self.shomate_correction
        elif method == "entropy":
            correct_func = self.entropy_correction
        else:
            raise ValueError("Unknown method: '{}'".format(method))

        # Loop over all elementary reactions.
        if self._owner.log_allowed:
            self.__logger.info("Use {} method to correct relative energies".format(method))
            self.__logger.info("------------------------------------------")
        for idx, rxn_expression in enumerate(self._owner.rxn_expressions):
            # Data used for info output.
            Gaf = relative_energies["Gaf"][idx]
            Gar = relative_energies["Gar"][idx]
            dG = relative_energies["dG"][idx]

            self.__correct_single_relative_energies(relative_energies, idx, correct_func)

            # Data used for info output.
            Gaf_prime = relative_energies["Gaf"][idx]
            Gar_prime = relative_energies["Gar"][idx]
            dG_prime = relative_energies["dG"][idx]

            msg = ("{}: Gaf({:.2f} -> {:.2f}), Gar({:.2f} -> {:.2f}), " +
                   "dG({:.2f} -> {:.2f})").format(rxn_expression,
                                                  Gaf, Gaf_prime,
                                                  Gar, Gar_prime,
                                                  dG, dG_prime)
            if self._owner.log_allowed:
                self.__logger.info(msg)

        if self._owner.log_allowed:
            self.__logger.info("------------------------------------------\n")

        return relative_energies

    def __correct_single_relative_energies(self, relative_energies, rxn_idx, correct_func):
        """
        Private helper function to correct relative energies for a single elementary reaction.

        Parameters:
        -----------
        rxn_idx     : The index of the reaction expression, int.
        correct_func: The function object to correct energy.
        """
        formula_lists = self._owner.elementary_rxns_list[rxn_idx]
        deltas = [] # energy changes for IS, TS, FS
        for formula_list in formula_lists:
            delta = 0.0
            for formula in formula_list:
                delta += correct_func(formula.formula())
            deltas.append(delta)

        self.__change_relative_energies(relative_energies, rxn_idx, deltas)

    def __change_relative_energies(self, relative_energies, rxn_idx, deltas):
        """
        Change the relative energies of solver from the enegies changes of
        a single elementary reaction.

        Parameters:
        -----------
        rxn_idx: The index of the reaction expression, int.
        deltas : The energy change vector for the corresponding elementary reaction,
                 float list.
        """
        Gaf = relative_energies["Gaf"][rxn_idx]
        Gar = relative_energies["Gar"][rxn_idx]
        dG = relative_energies["dG"][rxn_idx]

        # We have to treat adsorption and desorption particularly.
        if len(deltas) == 2:
            E_IS = 0.0
            E_FS = E_IS + dG
            delta_is, delta_fs = deltas
            E_IS += delta_is
            E_FS += delta_fs
            E_TS = max(E_IS, E_FS)
            # Calculate relative energies again.
            Gaf = E_TS - E_IS
            Gar = E_TS - E_FS
            dG = E_FS - E_IS
        elif len(deltas) == 3:
            # Correct relative energies.
            d_is, d_ts, d_fs = deltas
            d_Gaf = d_ts - d_is
            d_Gar = d_ts - d_fs
            d_dG = d_fs - d_is
            Gaf += d_Gaf
            Gar += d_Gar
            dG += d_dG

        # Update relative energies.
        relative_energies["Gaf"][rxn_idx] = Gaf
        relative_energies["Gar"][rxn_idx] = Gar
        relative_energies["dG"][rxn_idx] = dG

