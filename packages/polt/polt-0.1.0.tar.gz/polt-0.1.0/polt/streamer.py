# system modules
import sys
import threading
import inspect
import collections
import functools
import logging
import time

# internal modules

# external modules


logger = logging.getLogger(__name__)


class Streamer(threading.Thread):
    """
    Class to asynchronously stream and buffer data from a
    :class:`polt.parser.Parser` in a :class:`threading.Thread`.

    Args:
        parser (polt.parser.)
        buffer (list-like, optional): A buffer for the data. Defaults To a
            :class:`collections.deque`.
    """

    def __init__(self, parser=None, buffer=None):
        threading.Thread.__init__(
            self, daemon=True, name="{}Thread".format(type(self).__name__)
        )
        frame = inspect.currentframe()
        args = inspect.getargvalues(frame)[0]
        for arg in args[1:]:
            val = locals().get(arg)
            if val is not None:
                setattr(self, arg, val)

    @property
    def stopevent(self):
        """
        Event to stop the thread gracefully

        :type: :class:`threading.Event`
        """
        try:
            self._stopevent
        except AttributeError:  # pragma: no cover
            self._stopevent = threading.Event()
        return self._stopevent

    @property
    def parser(self):
        """
        The parser to buffer data from

        :type: :class:`polt.parser.Parser`
        """
        try:
            self._parser
        except AttributeError:  # pragma: no cover
            self._parser = None
        return self._parser

    @parser.setter
    def parser(self, new_parser):
        try:
            iter(new_parser.dataset)
        except AttributeError:  # pragma: no cover
            raise ValueError(
                "{} object does not have a 'dataset' property".format(
                    type(new_parser).__name__
                )
            )
        except TypeError:  # pragma: no cover
            raise ValueError(
                "dataset property {} object is not iterable".format(
                    type(new_parser.dataset).__name__
                )
            )
        self._parser = new_parser

    @property
    def buffer(self):
        """
        Buffer for received data

        :type: list-like, i.e. something with a :meth:`list.append`-like method
        :getter: Initializes an empty :class:`collections.deque`
            buffer if none is yet available
        """
        try:
            self._buffer
        except AttributeError:
            self._buffer = collections.deque()
        return self._buffer

    @buffer.setter
    def buffer(self, new_buffer):
        assert hasattr(
            new_buffer, "append"
        ), "{} object does not have an append() method".format(
            type(new_buffer).__name__
        )
        self._buffer = new_buffer

    def run(self):
        """
        Continuously read data from :attr:`Streamer.parser` into
        :attr:`Streamer.buffer` by iterating over :attr:`Parser.dataset`.
        """
        logger.debug(
            "Starting {} on {}".format(
                type(self.parser).__name__,
                self.parser.f.name
                if hasattr(self.parser.f, "name")
                else self.parser.f,
            )
        )
        while True:
            if self.stopevent.is_set():
                logger.debug("stopevent is set, stop reading data")
                break
            try:
                d = next(self.parser.dataset)
                logger.debug(
                    "Received dataset {} from {} on {}".format(
                        d,
                        type(self.parser).__name__,
                        self.parser.f.name
                        if hasattr(self.parser.f, "name")
                        else self.parser.f,
                    )
                )
                self.buffer.append(d)
            except StopIteration:
                logger.info(
                    "No more {} data on {}".format(
                        type(self.parser).__name__,
                        self.parser.f.name
                        if hasattr(self.parser.f, "name")
                        else self.parser.f,
                    )
                )
                break

    def stop(self):
        """
        Stop this thread gracefully, finishing just reading the current dataset
        """
        logger.debug("Will stop buffering soon")
        self.stopevent.set()

    def __del__(self):
        """
        Deconstructor
        """
        logger.debug("deconstructor")
