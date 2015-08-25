__author__ = 'fgh'

import locale

class Data:
    """ Light curve data point """

    def __init__(self, date, magnitude, error):
        self._date = locale.atof(date)
        self._magnitude = locale.atof(magnitude)
        self._error = locale.atof(error)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = locale.atof(date)

    @property
    def magnitude(self):
        return self._magnitude

    @magnitude.setter
    def magnitude(self, magnitude):
        self._magnitude = locale.atof(magnitude)

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, error):
        self._error = locale.atof(error)