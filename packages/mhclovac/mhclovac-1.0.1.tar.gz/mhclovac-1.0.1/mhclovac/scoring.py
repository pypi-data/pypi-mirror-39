import numpy as np


def sigmoid_weight(truth_param, null_param, k=8, x0=0.5, std_weighted=False):
    """
    :param truth_param:
    :param null_param:
    :param k:
    :param x0:
    :param std_weighted:
    :return:
    """
    t = truth_param[0] / truth_param[1] if std_weighted else truth_param[0]
    n = null_param[0] / null_param[1] if std_weighted else null_param[0]
    L = 1
    s = L / (1 + np.exp(-k * (t - n - x0)))
    return s


def relu_weight(truth_param, null_param, std_weighted=False):
    """
    :param truth_param:
    :param null_param:
    :param std_weighted:
    :return:
    """
    t = truth_param[0] / truth_param[1] if std_weighted else truth_param[0]
    n = null_param[0] / null_param[1] if std_weighted else null_param[0]
    s = max(0, t-n)
    return s


def linear_weight(truth_param, null_param, std_weighted=False):
    """
    :param truth_param:
    :param null_param:
    :param std_weighted:
    :return:
    """
    t = truth_param[0] / truth_param[1] if std_weighted else truth_param[0]
    n = null_param[0] / null_param[1] if std_weighted else null_param[0]
    return t-n


def get_profile_score(profile, hla_profile, weight=1):
    """
    Score peptide profile vector using reference hla_profile vector of the
    same length. Weight used to weight final score.
    :param profile: Peptide profile vector
    :param hla_profile: Reference HLA profile
    :param weight: float Weight
    :return: float Score
    """
    coef = np.corrcoef(profile, hla_profile)
    return np.round(weight*coef[0][1], 4)
