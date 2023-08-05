"""Generic pwm driver."""
from __future__ import division
import time
import math
import threading

from datetime import datetime


class Driver(object):
    """Represents the base class for pwm drivers."""

    IO_TRIES = 10
    TRANSITION_MIN_WAIT = 0.08

    def __init__(self, pins, resolution, freq):
        """
        Initialize the driver.

        :param pins: The pin numbers that should be controlled.
        :param resolution: The resolution of the pwm channel.
        :param freq: The pwm frequency.
        """
        if not isinstance(pins, list):
            pins = [pins]

        self._pins = pins
        self._resolution = resolution
        self._freq = freq
        self._state = [0] * len(self._pins)
        self._max_raw_value = math.pow(2, self._resolution) - 1

    @property
    def pins(self):
        """
        Color property.

        :return: The pins numbers that are controlled.
        """
        return self._pins

    def set_pwm(self, values):
        """
        Set pwm values on the controlled pins.

        :param values: Values to set (0.0-1.0).
        :return:
        """
        if len(values) != len(self._pins):
            raise ValueError('Number of values has to be identical with '
                             'the number of pins.')
        if not all(0 <= v <= 1 for v in values):
            raise ValueError('Values must be between 0 and 1.')

        for tries in range(self.IO_TRIES):
            try:
                self._set_pwm(self._to_raw_pwm(values))
                break
            except IOError as error:
                if tries == self.IO_TRIES - 1:
                    raise error
        self._state = values

    def _set_pwm(self, values):
        """
        Method stub for setting the pwm values.

        Has to be implemented by inheriting classes.
        :param values: Values to set (0.0-1.0).
        """
        raise NotImplementedError

    def _to_raw_pwm(self, values):
        """
        Convert uniform pwm values to raw, driver-specific values.

        :param values: The uniform pwm values (0.0-1.0).
        :return: Converted, driver-specific pwm values.
        """
        return [self._to_single_raw_pwm(values[i])
                for i in range(len(self._pins))]

    def _to_single_raw_pwm(self, value):
        """
        Convert a single uiform pwm value to raw, driver-specific value.

        :param value: The uniform pwm value (0.0-1.0).
        :return: Converted, driver-specific pwm value.
        """
        return int(round(value * self._max_raw_value))

    def _to_uniform_pwm(self, values):
        """
        Convert raw pwm values to uniform values.

        :param values: The raw pwm values.
        :return: Converted, uniform pwm values (0.0-1.0).
        """
        return [self._to_single_uniform_pwm(values[i])
                for i in range(len(self._pins))]

    def _to_single_uniform_pwm(self, value):
        """
        Convert a single raw pwm value to uniform value.

        :param value: The raw pwm value.
        :return: Converted, uniform pwm value (0.0-1.0).
        """
        return value / self._max_raw_value

    def transition(self, *args, callback=None, blocking=False):
        """
        Transition through given stages in specified duration.

        :param duration: The duration of the transition.
        :param stages: The stages to be executed during the transition.
        :param cancellation_token: Token used for cancelling the transition.
        :param blocking: Determines if the transition should block the thread.
        :param callback: Callback that is called when transition has finished.
        """
        if blocking:
            self._transition(*args, callback=callback)
        else:
            thread = threading.Thread(target=self._transition,
                                      args=args,
                                      kwargs={'callback': callback})
            thread.setDaemon(True)
            thread.start()

    def _transition(self, duration, stages, cancellation_token, callback=None):
        """
        Transition through given stages in specified duration.

        :param duration: The duration of the transition.
        :param stages: The stages to be executed during the transition.
        :param cancellation_token: Token used for cancelling the transition.
        :param callback: Callback that is called when transition has finished.
        """
        # Execute last stage immediately if duration is 0
        if duration == 0:
            self.set_pwm(stages[-1])
            self._call_if_present(callback, len(stages) - 1)
            return

        # If no stages were passed, nothing has to be done
        if not stages:
            self._call_if_present(callback, 0)
            return

        # Calculate steps to take
        steps = len(stages)
        wait = duration / steps
        if wait < self.TRANSITION_MIN_WAIT:
            steps = int(math.floor(duration / self.TRANSITION_MIN_WAIT))
            wait = self.TRANSITION_MIN_WAIT

        # Execute steps
        stage_index = 0
        for step in range(steps):
            # Abort transition, if cancellation was requested
            if cancellation_token.is_cancellation_requested:
                self._call_if_present(callback, stage_index)
                return

            # Apply stage
            start_time = datetime.now()
            progress = step / (steps - 1)
            stage_index = int(math.ceil(progress * (len(stages) - 1)))
            stage = stages[stage_index]
            self.set_pwm(stage)

            # Wait calculated interval minus time needed for applying the stage
            time_delta = datetime.now() - start_time
            time.sleep(max(0, wait - time_delta.total_seconds()))

        self._call_if_present(callback, stage_index)

    @staticmethod
    def _call_if_present(callback, *args, **kwargs):
        if callback:
            callback(*args, **kwargs)

    def steps(self, start, end):
        """
        Get the maximum number of steps the driver needs for a transition.

        :param start: The start value as uniform pwm value (0.0-1.0).
        :param end: The end value as uniform pwm value (0.0-1.0).
        :return: The maximum number of steps.
        """
        if not 0 <= start <= 1:
            raise ValueError('Values must be between 0 and 1.')
        if not 0 <= end <= 1:
            raise ValueError('Values must be between 0 and 1.')

        raw_start = self._to_single_raw_pwm(start)
        raw_end = self._to_single_raw_pwm(end)
        return abs(raw_start - raw_end)

    def stop(self):
        """Stop the driver and release resources."""
        self._stop()

    def _stop(self):
        """
        Method stub for stopping the driver.

        Has to be implemented by inheriting classes.
        """
        pass
