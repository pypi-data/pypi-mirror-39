"""
    MIT License

Copyright (c) 2018 Stefan Stojanovic

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

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
