# system modules
import sys
import inspect
import re
import functools
import csv
import logging
from abc import ABC, abstractproperty

# internal modules
from polt.streamer import Streamer

# external modules


logger = logging.getLogger(__name__)


class Parser(ABC):
    """
    Abstract base class for parsers.

    Args:
        f (file-like object, optional): the connection to read from
    """

    def __init__(self, f=None):
        frame = inspect.currentframe()
        args = inspect.getargvalues(frame)[0]
        for arg in args[1:]:
            val = locals().get(arg)
            if val is not None:
                setattr(self, arg, val)

    @property
    def f(self):
        """
        The connection to read from
        """
        try:
            self._f
        except AttributeError:  # pragma: no cover
            self._f = None
        return self._f

    @f.setter
    def f(self, new):
        self._f = new

    @abstractproperty
    def dataset(self):
        """
        Generator yielding the next dataset
        """
        pass


class NumberParser(Parser):
    """
    Simple parser extracting numbers line-wise
    """

    NUMBER_REGEX = re.compile(r"-?\d+(?:\.\d+)?")
    """
    Regular expression to detect numbers
    """

    @property
    def dataset(self):
        logger.debug(
            "Reading from {}...".format(
                self.f.name if hasattr(self.f, "name") else self.f
            )
        )
        for line in self.f:
            if not line.strip():
                continue
            logger.debug(
                "Received {} from {}".format(
                    repr(line),
                    self.f.name if hasattr(self.f, "name") else self.f,
                )
            )
            numbers = (
                float(m.group())
                for m in self.NUMBER_REGEX.finditer(
                    line.decode(errors="ignore")
                    if hasattr(line, "decode")
                    else line
                )
            )
            numbers_list = list(numbers)
            logger.debug("Numbers extracted: {}".format(numbers_list))
            yield numbers_list


class CsvParser(Parser):
    """
    Parser for CSV input
    """

    def __init__(self, f=None, **dictreader_kwargs):
        Parser.__init__(self, f)
        self.dictreader_kwargs = dictreader_kwargs

    def modifies_csvreader(decorated_function):
        """
        Decorator for methods that require a reset of the :attr:`csvreader`
        """

        @functools.wraps(decorated_function)
        def wrapper(self, *args, **kwargs):
            if hasattr(self, "_csvreader"):
                logger.debug(
                    "Resetting csvreader before {}".format(decorated_function)
                )
                del self._csvreader  # pragma: no cover
            return decorated_function(self, *args, **kwargs)

        return wrapper

    @property
    def csvreader(self):
        """
        The underlying csv parser

        :type: :class:`csv.DictReader`
        """
        try:
            self._csvreader
        except AttributeError:
            self._csvreader = csv.DictReader(self.f, **self.dictreader_kwargs)
        return self._csvreader

    @property
    def dictreader_kwargs(self):
        """
        Further keyword arguments for the underlying :attr:`csvreader`

        :type: :class:`dict`
        :setter: resets the :attr:`csvreader`
        """
        try:
            self._dictreader_kwargs
        except AttributeError:  # pragma: no cover
            self._dictreader_kwargs = {}
        return self._dictreader_kwargs

    @dictreader_kwargs.setter
    @modifies_csvreader
    def dictreader_kwargs(self, new):
        self._dictreader_kwargs = new

    @Parser.f.setter
    @modifies_csvreader
    def f(self, new):
        self._f = new

    @property
    def dataset(self):
        for d in self.csvreader:
            yield d
