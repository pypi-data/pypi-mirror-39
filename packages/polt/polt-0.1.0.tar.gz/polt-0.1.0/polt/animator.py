# system modules
import threading
import functools
import collections
import logging
import inspect
import datetime

# internal modules

# external modules
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

logger = logging.getLogger(__name__)


class Animator:
    """
    Animator class

    Args:
        figure (matplotlib.figure.Figure, optional): the figure to animate on
        buffer (list-like, optional): the buffer to retrieve
            data from.
        interval (int, optional): the frame update interval in milliseconds.
            Default is 200.
    """

    def __init__(self, figure=None, buffer=None, interval=None):
        frame = inspect.currentframe()
        args = inspect.getargvalues(frame)[0]
        for arg in args[1:]:
            val = locals().get(arg)
            if val is not None:
                setattr(self, arg, val)

    def modifies_animation(decorated_function):
        """
        Decorator for methods that require resetting the animation
        """

        @functools.wraps(decorated_function)
        def wrapper(self, *args, **kwargs):
            if hasattr(self, "_animation"):
                logger.debug(
                    "Clearing animation before {}".format(decorated_function)
                )
                del self._animation
            return decorated_function(self, *args, **kwargs)

        return wrapper

    @property
    def buffer(self):
        """
        The buffer to retrieve data from

        :type: list-like
        """
        try:
            self._buffer
        except AttributeError:  # pragma: no cover
            self._buffer = None
        return self._buffer

    @buffer.setter
    def buffer(self, new):
        self._buffer = new

    @property
    def interval(self):
        """
        The frame update interval

        :type: :any:`int`
        """
        try:
            self._interval
        except AttributeError:
            self._interval = 200
        return self._interval

    @interval.setter
    def interval(self, new_interval):
        self._interval = int(new_interval)

    @property
    def figure(self):
        """
        The figure to animate on

        :type: :class:`matplotlib.figure.Figure`
        """
        try:
            self._figure
        except AttributeError:  # pragma: no cover
            self._figure = None
        return self._figure

    @figure.setter
    @modifies_animation
    def figure(self, new):
        self._figure = new

    @property
    def animation(self):
        """
        The underlying animation

        :type: :class:`matplotlib.animation.FuncAnimation`
        """
        try:
            self._animation
        except AttributeError:
            self._animation = FuncAnimation(
                fig=self.figure,
                func=self.update_figure,
                frames=self.dataset,
                interval=self.interval,
                repeat=False,
            )
        return self._animation

    def update_figure(self, data):
        """
        Update the :attr:`figure`
        """
        if data is None:
            logger.debug("No data waiting")
        else:
            logger.debug("Updating the figure with data {}".format(data))
            ax = plt.gca()
            if isinstance(data, collections.Sequence):
                for d in data:
                    ax.scatter(datetime.datetime.now(), d, c="royalblue")
            else:
                ax.scatter(datetime.datetime.now(), data, c="royalblue")

    @property
    def dataset(self):
        """
        Generator yielding the last element in :attr:`Animator.buffer`
        """
        while True:
            if len(self.buffer):
                yield self.buffer.pop(0)
            else:
                yield None

    def run(self):
        """
        Run the animation by calling :func:`matplotlib.pyplot.show`
        """
        self.animation
        logger.debug("Showing the plot")
        plt.show()
        logger.debug("Plot was closed")
