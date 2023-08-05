# -*- coding: utf-8 -*-
#
#     Copyright (C) 2018 Kevin De Bruycker and Tim Krappitz
#
#     This file is part of pyMacroMS.
#     pyMacroMS allows for high performance quantification of complex high resolution polymer mass spectra.
#
#     pyMacroMS is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     pyMacroMS is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with pyMacroMS.  If not, see <https://www.gnu.org/licenses/>.
#

from __future__ import absolute_import
from math import exp, isclose
from collections import Counter
import itertools
import pymacroms
import IsoSpecPy
import matplotlib.pyplot as plt
from operator import itemgetter, attrgetter
import re
import sys

class Molecule:

    def __init__(self, formula, adductIon = "H+", charge = 1, minRelAbundance = 0.01):
        """
        only the most abundant isotopes with a relative abundance of <minRelAbundance> will be taken into account

        :type formula: Counter or str
        :type adductIon: str
        :type charge: int
        :type minRelAbundance: float
        """
        #input processing: internal formula should be a counter for processing while self.formula should be a str for reporting
        if type(formula) == str:
            # save the formula as an attribute and then convert it to a counter to be able to include the ionisation
            self.formula = formula
            formula = pymacroms.getCounterFromFormula(formula)
        else:
            # transform the formula to a str for the attribute only
            self.formula = pymacroms.getFormulaStrFromCounter(formula)

        # adductIon that is passed must be a str that is present in the database
        self.adductIon = adductIon
        self.charge = charge
        try:
            adductIon = pymacroms.database.ionising_species[adductIon]  # [formula: Counter, charge: int, mass_correction: float]
        except:
            sys.exit("adductIon not found in database!")
        self.amountAdductIons = abs(int(charge / adductIon[1]))
        # add an int amount of ionising species: charge/charge-per-ion
        # again, the internal variable is a counter, the self. variant is a str
        formula_ion = formula + Counter({element: amount*self.amountAdductIons for element, amount in adductIon[0].items()})
        self.formula_ion = pymacroms.getFormulaStrFromCounter(formula_ion)
        # Generate the isotopologues using IsoSpecPy
        isotopologues = IsoSpecPy.IsoThresholdGenerator(formula=self.formula_ion, threshold=minRelAbundance, absolute=False, get_confs=False, use_lprobs=False)
        # IsoSpecPy returns the isotopic distribution as an iterable (mass, 'normalised' abundance (= probability))
        # since IsoSpec generates a list of isotopes with a relative abundance > minimumRelAbundance, further filtering is not necessary
        # total m/z = mass + mass correction (amount of ionising species * correction per ionising specie) devided by charge
        self.isotopicDist = sorted(list(((mass + self.amountAdductIons * adductIon[2])/charge, prob) for mass, prob in isotopologues))
        self.massMin = self.isotopicDist[0][0]
        self.massMax = self.isotopicDist[len(self.isotopicDist)-1][0]
        self.massMostAbundant = sorted(self.isotopicDist, key=itemgetter(1), reverse=True)[0][0]

    def printIsotopicDist(self):
        print(self.formula + " --> " + self.formula_ion)
        print("Mass\tRel. Abundance")
        for mass, relAbund in pymacroms.toRelativeAbundance(self.isotopicDist):
            print(str(mass) + "\t" + str(relAbund))

    def plotIsotopicDist(self, color = "black"):
        mz_axis = []
        relAbund_axis = []
        for mz, relAbund in pymacroms.toRelativeAbundance(self.isotopicDist):
            mz_axis += list([mz - 1e-10, mz, mz + 1e-10])
            relAbund_axis += list([-0.1, relAbund, -0.1])
        plt.plot(mz_axis, relAbund_axis, color=color)
        plt.title(r"Isotopic distribution for {} ({} + {}{})".format(re.sub("([0-9]+)", "$_{\\1}$", self.formula_ion), re.sub("([0-9]+)", "$_{\\1}$", self.formula), self.amountAdductIons, re.sub("([0-9]+)", "$_{\\1}$", re.sub("([+-]+)", "$^{\\1}$", self.adductIon)))) # re.sub("([0-9]+)", "$_{\\1}$", self.formula_ion)
        plt.xlabel("m/z")
        plt.ylabel("Rel. abundance")
        plt.ylim(0, 1.05)
        plt.show()

    def inMassRange(self, massRange: list, completelyInRange: bool = False):
        if completelyInRange and self.massMin >= massRange[0] and self.massMax <= massRange[1]:
            return True
        elif not completelyInRange and self.massMax >= massRange[0] and self.massMin <= massRange[1]:
            return True
        else:
            return False

    def hasIsotopeNearMass(self, experimentalMass: float, ppmDev: float = 5):
        for isotope in self.isotopicDist:
            if isclose(isotope[0], experimentalMass, rel_tol=(ppmDev/1e6)):
                return True
        return False

    def getIsotopesNearMass(self, experimentalMass: float, ppmDev: float = 5, resolution: float = None):
        isotopesNearMass = []
        if resolution is None:
            for isotopeMass, normAbundance in self.isotopicDist:
                deviation = abs(experimentalMass - isotopeMass) / isotopeMass * 1e6
                if deviation <= ppmDev:
                    isotopesNearMass.append((isotopeMass, normAbundance, deviation))
        else:
            if not hasattr(self, "resolution"):
                self.resolution = resolution
                self.isotopicDist_resolution = pymacroms.combineIsotopes(self.isotopicDist, resolution)
                self.massMostAbundant = sorted(self.isotopicDist_resolution, key=itemgetter(1), reverse=True)[0][0]
            elif self.resolution != resolution:
                self.resolution = resolution
                self.isotopicDist_resolution = pymacroms.combineIsotopes(self.isotopicDist, resolution)
                self.massMostAbundant = sorted(self.isotopicDist_resolution, key=itemgetter(1), reverse=True)[0][0]
            for isotopeMass, normAbundance in self.isotopicDist_resolution:
                deviation = abs(experimentalMass - isotopeMass) / isotopeMass * 1e6
                if deviation <= ppmDev:
                    isotopesNearMass.append((isotopeMass, normAbundance, deviation))
        if len(isotopesNearMass) > 0:
            return isotopesNearMass
        else:
            return None




