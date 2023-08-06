"""
    MHCLovac - MHC binding prediction based on modeled physicochemical properties of peptides
    Copyright (C) 2018  Stefan Stojanovic

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

import numpy as np
from scipy.stats import norm
import warnings
from mhclovac.misc import norm_array


def get_profile(peptide, schema, scale=0.8, peptide_lengths=None,
                vector_length=100, normalize=False):
    """
    :param peptide: Peptide sequence
    :param schema: pandas DataFrame with "amino_acid" and "value" columns
    :param scale: Modeling parameter: distribution scale or st.deviation
    :param peptide_lengths:
    :param vector_length: Length of return profile vector
    :param normalize: Normalize profile values to 0-1 range
    :return: Numpy array
    """
    # Prepare data
    peptide = peptide.upper()
    schema['amino_acid'] = schema['amino_acid'].str.upper()
    schema['value'] = norm_array(schema['value'], -1, 1)
    schema.replace(0, 0.0001, inplace=True)

    peptide_lengths = peptide_lengths or len(peptide)
    prod = np.prod(peptide_lengths)
    while prod < 1000:
        prod *= 10
    span = prod / len(peptide)
    pep_vector = np.zeros(int(prod + 2 * span))
    for i, aa in enumerate(peptide):
        row = schema[schema['amino_acid'] == aa]
        if len(row) != 1:
            warnings.warn('Ambiguous schema for amino acid {}. Value '
                          'will be set to mean value.'.format(aa),
                          Warning)
            hphob = np.mean(schema['value'])
        else:
            hphob = float(row['value'])
        x = np.linspace(norm.ppf(0.01), norm.ppf(0.99), int(3 * span))
        pdf = norm.pdf(x, scale=scale) * hphob
        pep_vector[int(i * span):int((i + 3) * span)] += pdf
    pep_vector = pep_vector[int(span):int(-span)]
    vector = []
    offset = 0
    step = int(len(pep_vector) / vector_length)
    for i in range(vector_length):
        tick = pep_vector[offset]
        offset += step
        vector.append(tick)
    if normalize:
        vector = (vector-np.min(vector))/(np.max(vector)-np.min(vector))
    return vector
