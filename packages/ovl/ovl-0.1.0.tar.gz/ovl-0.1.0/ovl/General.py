# Copyright 2018 Ori Ben-Moshe - All rights reserved.
from math import pi
from time import sleep, gmtime, strftime
from sys import version_info

if version_info[0] == 3:
    xrange = range


def print_pipe(out, *args):
    if out is None:
        for i in args:
            print(str(i))
        print('')
    if not out:
        pass
    else:
        with open(out, 'a') as f:
            print(args)
            text = strftime("%a, %d %b %Y %H:%M:%S:: ", gmtime()) + str(args)
            f.write(text)
            f.close()


class ToolClass:
    help_text = "The help and documentation text for %s hasn't been defined"

    @property
    def help(self):
        return self.__class__.help_text.replace('%s', self.__class__.__name__)

    def __init__(self):
        print('')
        print_pipe(None, self.help)
        sleep(0.25)
        raise ToolError("Tool classes cannot be instantiated ")


class InvalidCustomError(Exception):
    pass


class Performance:
    def __init__(self):
        self.contours_times = []


class VersionError(Exception):
    pass


class ToolError(Exception):
    pass


def root(base, degree):
    """
    Action: Raises base to the root of degree. [base^(1/degree)]
    :param base: The number to be raised
    :param degree: The root
    :return: the result
    :rtype: Float
    """
    return float(base) ** (1 / float(degree))


def get_calibrated_value(img_mean, vector):
    """
    Action: Solves the calibration equation that finds the optimal low bound value for
            the saturation and value.
    :param img_mean: the mean if the image of which
    :param vector: the dictionary containing the coefficients and group mean.
    :return: the optimal low bound
    """
    data_mean = vector['mean'][0]
    z_mean = data_mean[0] * vector['co1'] + data_mean[1] * vector['co2']
    return (z_mean - (img_mean * vector['co1'])) / vector['co2']


def radians2degrees(radians):
    return radians * 180 / pi


def degrees2radians(degrees):
    return degrees * pi / 180


def numerical_replace(string, *args):
    for i in xrange(len(args)):
        string = string.replace(str(i), str(i) + '!%$#*^&#@^#%')

    for number, replacement in enumerate(args):
        string = string.replace(str(number) + '!%$#*^&#@^#%', str(replacement))
    return string


def enumertype(iterable):
    for obj in iterable:
        yield type(obj), obj
