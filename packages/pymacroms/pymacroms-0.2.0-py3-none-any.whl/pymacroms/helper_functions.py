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
from math import exp, log, sqrt
from collections import Counter
import itertools
import pymacroms
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from operator import itemgetter, attrgetter
import re
import sys
# from numba import jit

def getMonoIsotopicMass(formula: Counter):
    return sum(list(sorted(pymacroms.database.isotopic_abundances[element], key=itemgetter(1), reverse=True)[0][0]*amount for element, amount in formula.items()))
    # totalMass = 0
    # for element, amount in formula.items():
    #     totalMass += pymacroms.database.isotopic_abundances[element][0][0] * amount
    # return totalMass

def getCounterFromFormula(formula: str):
    return Counter({element: int(amount) for element, amount in re.findall("([A-Z][a-z]*)([0-9]+)", re.sub(" ", "", re.sub("  ", " 1 ", re.sub("([A-Z][a-z]*)([0-9]*)", "\\1 \\2 ", re.sub(" ","", formula)))))})
    #first removes all spaces, then replace all elements with optional number by element-space-amount-space
    #because an absent number will result in a double space, the double spaces are then replaced by space-1-space
    #by removing the spaces again, the formula is then guaranteed to have an amount for every element (C9H18NO --> C9H18N1O1)
    #finally, transform in a list and then Counter by matching the element-amount pairs

    '''
    return Counter({element: int(amount) for element, amount in re.findall("([A-Z][a-z]*)([0-9]*)", re.sub("([A-Z][a-z]*)([A-Z]|\Z)", "\g<1>1\g<2>", formula))})
    Is more simple but gives an error on for example C9H18NO because in the first substitution, NO is replaced by N1O, and because O is already matched, it is not replaced by O1
    This results in an O: '' in the library and thus an error when converting to int 
    '''

def getFormulaStrFromCounter(formula: Counter):
    tempFormula = ""
    for element, amount in formula.items():  # sorted(dict) does not influence the calculations, while leaving it out typically gives more OK formulas for the OCDd chemist
        tempFormula += element + str(amount)
    return tempFormula

def toRelativeAbundance(peaklist: list):
    maxAbund = max(list(zip(*peaklist))[1])
    return sorted(list((mass, normAbund/maxAbund) for mass, normAbund in peaklist))

def combineIsotopes(peaklist: list, resolution: float):
    # returns a list of peaks [(mz, normAbundance)]
    if type(peaklist) == list:
        peaklist_df = pd.DataFrame(peaklist, columns=["mz", "abundance"])
    else:
        columns_temp = peaklist.columns
        peaklist_df = peaklist
        peaklist_df.columns = ["mz", "abundance"]

    index = 0
    while index < len(peaklist_df):
        if not peaklist_df.iloc[index].isnull().all():  # checks that 'not all values in a row are NaN', alternative: .any()
            mz = peaklist_df.iloc[index].mz
            # stdDev = mz / (2 * sqrt(2 * log(2)) * resolution); +- 2stdDev contains 95% of the normal distribution while +- 1.17741stdDev is the FWHM range
            dmz = mz / (2 * resolution)
            masses = list(peaklist_df.loc[(peaklist_df.mz >= mz - dmz) & (peaklist_df.mz <= mz + dmz)].mz)
            if len(masses) > 1:
                abundances = list(peaklist_df.loc[(peaklist_df.mz >= mz - dmz) & (peaklist_df.mz <= mz + dmz)].abundance)
                peaklist_df.loc[(peaklist_df.mz >= mz - dmz) & (peaklist_df.mz <= mz + dmz)] = None
                peaklist_df.iloc[index] = np.average(masses, weights=abundances), sum(abundances)
        index += 1
    peaklist_df.dropna(how="all", inplace=True)  # get rid of all the empty lines, how=all limits to rows that are completely empty
    peaklist_df.reset_index(drop=True, inplace=True)
    # peaklist_df.normAbundance = peaklist_df.normAbundance / peaklist_df.normAbundance.sum()  # recalculate normalised abundance
    # if the sum = 1 for the input (normAbundance), then the sum will still be 1 when simply adding peaks together.
    # if the input is no normAbundance, then the recalculation has to be done externally

    if type(peaklist) == list:
        return list(peaklist_df.itertuples(index=False, name=None))
    else:
        peaklist_df.columns = columns_temp
        return peaklist_df

# Try to speed up this step using C
# # @njit
# def combineIsotopes2(peaklist: list, resolution: float):
#     # returns a list of peaks [(mz, normAbundance)]
#     if type(peaklist) == list:
#         peaklist_df = pd.DataFrame(peaklist, columns=["mz", "abundance"])
#     else:
#         columns_temp = peaklist.columns
#         peaklist_df = peaklist
#         peaklist_df.columns = ["mz", "abundance"]
#
#     index = 0
#     while not peaklist_df.iloc[index].isnull().all():
#         mz = peaklist_df.iloc[index].mz
#         range = [mz - mz / resolution / 2, mz + mz / resolution / 2]
#         masses = list(peaklist_df.loc[(peaklist_df.mz >= range[0]) & (peaklist_df.mz <= range[1])].mz)
#         if len(masses) > 1:
#             abundances = list(peaklist_df.loc[(peaklist_df.mz >= range[0]) & (peaklist_df.mz <= range[1])].abundance)
#             peaklist_df.loc[(peaklist_df.mz >= range[0]) & (peaklist_df.mz <= range[1])] = None
#             peaklist_df.iloc[index] = np.average(masses, weights=abundances), sum(abundances)
#             peaklist_df.sort_values(by=["mz"], inplace=True, na_position='last')
#         index += 1
#     peaklist_df.dropna(how="all", inplace=True)  # get rid of all the empty lines, how=all limits to rows that are completely empty
#     peaklist_df.reset_index(drop=True, inplace=True)
#     # peaklist_df.normAbundance = peaklist_df.normAbundance / peaklist_df.normAbundance.sum()  # recalculate normalised abundance
#     # if the sum = 1 for the input (normAbundance), then the sum will still be 1 when simply adding peaks together.
#     # if the input is no normAbundance, then the recalculation has to be done externally
#
#     if type(peaklist) == list:
#         return list(peaklist_df.itertuples(index=False, name=None))
#     else:
#         peaklist_df.columns = columns_temp
#         return peaklist_df