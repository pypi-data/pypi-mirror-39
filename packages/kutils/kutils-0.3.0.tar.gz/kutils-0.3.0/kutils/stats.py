# -*- coding: utf-8 -*-
"""
stats contains basic statistics utilities for use in the Udacity
probstats class and quick statistics calculations.
"""

import math
import pdb
import random
import statistics


class DataSet:
    """
    DataSet contains a list of data which may have statistics
    computed on it. It stores both the original data passed
    into it, as well as a working data set. The working data
    set will be sorted on calls to update(), and a call to
    quartile will trim the dataset.
    """

    __slots__ = ["data", "orig_data", "mu", "stdev", "alpha", "size", "sum_x", "sum_x2"]

    def __init__(self, data, alpha=1.96):
        """
        Creating a DataSet requires initialising itself with some
        data.
        """
        self.orig_data = data
        self.data = None
        self.alpha = alpha
        self.mu = 0
        self.stdev = 0
        self.sum_x = 0
        self.sum_x2 = 0

        self.update()

    def update(self, data=None, no_reset=False):
        """
        Compute μ and σ for the dataset. This will reset all computations
        on the data, including calls to quartiles, replacing the working
        data set with a new working data set from the original data. If
        the data parameter is not None, it must be a list or set that will
        be used to extend the original data. If no_reset is True, the working
        data set will not be replaced. If no_reset is True and data is not
        None, the working data set will be replaced anyways.
        """
        if data is not None:
            self.orig_data.extend(data)
            no_reset = False

        if not no_reset:
            self.data = sorted(self.orig_data)

        self.mu = sum(self.data) / len(self.data)
        self.stdev = statistics.pstdev(self.data, self.mu)
        self.size = len(self.data)

        self.sum_x = 0
        self.sum_x2 = 0
        for x in self.data:
            self.sum_x += x
            self.sum_x2 += x ** 2

    def confidence(self):
        """Compute the confidence interval for the dataset."""
        return self.alpha * math.sqrt(self.stdev ** 2 / self.size)

    def confidence_mu(self):
        """
        Compute the low and high mean based on the confidence.
        """
        ci = self.confidence()
        return (self.mu - ci, self.mu + ci)

    def confident(self, mu):
        """
        Given the dataset, are we confident that mu falls in the confidence
        interval for the mean?
        """
        return abs(mu - self.mu) < self.confidence()

    def quartiles_indices(self):
        """Return indices for the lower quartile and upper quartile."""
        lqi = math.floor(self.size / 4)
        uqi = math.ceil(self.size * 3 / 4)
        return lqi, uqi

    def quartiles(self, low=None, high=None):
        """
        Set the working data set to the quartiles of the working
        data set. This is not idempotent; successive calls will
        return further trimmed data.
        """
        lqi, uqi = self.quartiles_indices()
        if low is None:
            low = lqi
        if high is None:
            high = uqi
        self.data = self.data[low:high]
        self.update(no_reset=True)

    def score(self, x):
        """Compute the standard score of x."""
        return (x - self.mu) / self.stdev


def ncomb(n, k):
    """Return the combinatorics of n objects with k choices."""
    return math.factorial(n) / ((math.factorial(n - k) * math.factorial(k)))


def confidence(p, n, a=1.96):
    """Return the confidence of a two-state system with n samples and probability p."""
    var = p * (1 - p)
    ci = math.sqrt(var / n)
    return a * ci


def binomial(n, k, p):
    """Return the binomial distribution of n objects with k choices and probability p."""
    return ncomb(n, k) * (p ** k) * ((1.0 - p) ** (n - k))


def variance(data, mu=None):
    """Compute variance over a list."""
    if mu is None:
        mu = statistics.mean(data)
    return sum([(x - mu) ** 2 for x in data]) / len(data)


def meanvar3(n, sum_x, sum_x2, alpha=1.96):
    """Compute the mean and variance from the three variables."""
    mu = sum_x / n
    var = (sum_x2 / n) - ((sum_x ** 2) / (n ** 2))
    ci = alpha * math.sqrt(var / n)
    return mu, var, ci


def stddev(data, mu=None):
    """Compute standard deviation over a list."""
    return math.sqrt(variance(data, mu))


def bayes(prior, sensitivity, specitivity):
    """Compute Bayes rule over the prior, sensitivity, and specitivity."""
    joint1 = prior * sensitivity
    joint2 = (1.0 - prior) * (1.0 - specitivity)
    normalizer = joint1 + joint2
    return joint1 / normalizer


def coin_flip(p=0.5):
    """Simulate a coin flip."""
    return True if random.random() > p else False


def dice(sides=6):
    """Simulate a dice roll."""
    return math.floor(random.random() * sides) + 1


def sample_builder(samples):
    """
    Given a dictionary with value: count pairs, build a list.
    """
    data = []
    for key in samples:
        data.extend([key] * samples[key])
    data.sort()
    return data


# TODO: make this not iterate over the dataset so many times
def linear_regression_2d(data):
    """Compute a and b for a two-dimensional dataset."""
    mu_y = 0
    mu_x = 0

    for (x, y) in data:
        mu_y += y
        mu_x += x

    mu_x = mu_x / len(data)
    mu_y = mu_y / len(data)

    top = sum([(x - mu_x) * (y - mu_y) for (x, y) in data])
    x_vars = [(x - mu_x) ** 2 for (x, _) in data]
    y_vars = [(y - mu_y) ** 2 for (_, y) in data]

    b = top / sum(x_vars)
    a = mu_y - (b * mu_x)
    r = top / math.sqrt(sum(x_vars) * sum(y_vars))
    return b, a, r


def monty_hall(verbose=False):
    """
    Run a Monty Hall simulation modeled on the choices available to
    both us and Monty. Returns True if we picked the right door and
    False otherwise. Set verbose to True to print messages about
    what's happening.
    """
    pick_one = lambda l: l[random.randint(0, len(l) - 1)]
    # we have three choices for a door
    choices = [1, 2, 3]
    # monty has three choices for a door
    mchoices = [1, 2, 3]
    s = u""

    # first: where is it? remove this from the choices, because monty won't
    # pick it.
    car = pick_one(mchoices)
    mchoices.remove(car)
    s += u"car←{}, ".format(car)

    # second: I pick a door, and remove it from the choices, because monty
    # won't pick it. remove it from my choices, because I won't pick it.
    door = pick_one(choices)
    choices.remove(door)
    if door in mchoices:
        mchoices.remove(door)
    s += u"guess1←{}, ".format(door)

    # now monty has to pick a door to show us. we have to remove this choice from
    # our list.
    shown = pick_one(mchoices)
    s += u"shown←{}, ".format(shown)
    choices.remove(shown)

    door = pick_one(choices)
    s += u"guess2←{}, ".format(door)

    if door == car:
        s += u"(Y)"
        if verbose:
            print(s)
        return True
    else:
        s += u"(N)"
        if verbose:
            print(s)
        return False
