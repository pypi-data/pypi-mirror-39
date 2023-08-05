#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2015 Chintalagiri Shashank
# Copyright (C) 2015 Anurag Kar
#
# This file is part of tendril.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Docstring for measurements
"""

import time
import arrow

from colorama import Fore
from tendril.utils.types.electromagnetic import Voltage, Current
from tendril.utils.types.time import Frequency

from tendril.utils import log
logger = log.get_logger(__name__, log.INFO)


class TestMeasurementBase(object):
    """ Object representing a single measurement for a Test """
    def __init__(self):
        self._parent = None
        self._ts = None

    def do_measurement(self):
        """
        This is the measurement function. This should be overridden
        by the actual Test classes to perform the actual measurement.
        """
        raise NotImplementedError

    def render(self):
        """
        This is an example render function. This should be overridden by the
        actual Test classes to render the actual result.

        Rendering means encoding the test result into a JSON representation,
        which can later be dumped into a postgres database.
        """
        raise NotImplementedError

    def render_dox(self):
        if self._ts is None:
            logger.warning("render_dox can't find _ts for Measurement Class"
                           + str(self.__class__))
            meas_dict = {}
        else:
            meas_dict = {'ts': self._ts.format()}
        return meas_dict

    def load_result_from_obj(self, result_db_obj):
        raise NotImplementedError

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def yesorno(self):
        raise NotImplementedError


class TestSimpleMeasurement(TestMeasurementBase):
    def __init__(self):
        super(TestSimpleMeasurement, self).__init__()
        self._outputchannel = None
        self._output = None
        self._stime = None
        self._inputchannel = None
        self._input = None
        self._inputtype = None
        self._instrument = None

    def do_measurement(self):
        """
        This is an example measurement function. This should be overridden
        by the actual Test classes to perform the actual measurement, and
        this code can be used as a starting point.

        The result of the measurement would typically be some composition of
        instances of :class:`tendril.utils.type.signalbase.SignalBase`.
        """
        logger.debug("Making measurement : " + repr(self))
        if self._output is not None:
            if self._outputchannel is None:
                raise IOError("Output channel is not defined")
            self._outputchannel.set(self._output)

        if self.stime is not None:
            time.sleep(self.stime)

        if self._inputtype is not None:
            if self._inputchannel is None:
                raise IOError("Input channel is not defined")
            self._input = self._inputchannel.get()
            if self._input.unitclass is not None and \
                    not self._input.unitclass == self._inputtype:
                raise TypeError(
                    "Expected " + self._inputtype.unitclass +
                    ", got " + type(self._input)
                )

        self._ts = arrow.utcnow()

    @property
    def stime(self):
        return self._stime

    @property
    def yesorno(self):
        raise NotImplementedError

    def render(self):
        return {'instrument':
                (self._instrument.ident if self._instrument is not None
                 else None),
                'output': self._output,
                'input': self._input}

    def load_result_from_obj(self, result_db_obj):
        raise NotImplementedError


class DCVoltageMeasurement(TestSimpleMeasurement):
    def __init__(self):
        super(DCVoltageMeasurement, self).__init__()
        self._outputchannel = None
        self._inputtype = None
        self._inputchannel = None

    def do_measurement(self):
        """
        This function is present only because the instrument return value is
        not of a SignalPoint Type. Instrument classes should be changed to
        use Signal Point type instead and this class should fall back to the
        parent's implementation.
        """
        logger.debug("Making measurement : " + repr(self))
        if self._output is not None:
            if self._outputchannel is None:
                raise IOError("Output channel is not defined")
            self._outputchannel.set(self._output)

        if self.stime is not None:
            time.sleep(self.stime)

        if self._inputtype is not None:
            if self._inputchannel is None:
                raise IOError("Input channel is not defined")
            self._input = self._inputchannel.get()
            # if self._input.unitclass and \
            #         not self._input.unitclass == self._inputtype:
            #     raise TypeError(
            #         "Expected " + self._inputtype.unitclass +
            #         ", got " + type(self._input)
            #     )
        logger.info("Measured Voltage: " + repr(self._input))
        self._ts = arrow.utcnow()

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value
        self._inputtype = Voltage
        if self._parent._offline is not True:
            self._inputchannel = self._parent.instrument.voltage_input

    @property
    def input_voltage(self):
        return self._input

    def yesorno(self):
        pass

    def render(self):
        return {
            'input': {'v': repr(self._input)},
            'timestamp': self._ts.isoformat()
            }

    def load_result_from_obj(self, result_db_obj):
        self._input = Voltage(result_db_obj['input']['v'])
        self._ts = arrow.get(result_db_obj['timestamp'])


class ACVoltageMeasurement(TestSimpleMeasurement):
    def __init__(self):
        super(ACVoltageMeasurement, self).__init__()
        self._outputchannel = None
        self._inputtype = None
        self._inputchannel = None

    def do_measurement(self):
        """
        This function is present only because the instrument return value is
        not of a SignalPoint Type. Instrument classes should be changed to
        use Signal Point type instead and this class should fall back to the
        parent's implementation.
        """
        logger.debug("Making measurement : " + repr(self))
        if self._output is not None:
            if self._outputchannel is None:
                raise IOError("Output channel is not defined")
            self._outputchannel.set(self._output)

        if self.stime is not None:
            time.sleep(self.stime)

        if self._inputtype is not None:
            if self._inputchannel is None:
                raise IOError("Input channel is not defined")
            self._input = self._inputchannel.get()
            # if self._input.unitclass and \
            #         not self._input.unitclass == self._inputtype:
            #     raise TypeError(
            #         "Expected " + self._inputtype.unitclass +
            #         ", got " + type(self._input)
            #     )
        logger.info("Measured Voltage: " + repr(self._input))
        self._ts = arrow.utcnow()

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value
        self._inputtype = Voltage
        if self._parent._offline is not True:
            self._inputchannel = self._parent.instrument.ac_voltage_input

    @property
    def input_voltage(self):
        return self._input

    def yesorno(self):
        pass

    def render(self):
        return {
            'input': {'v': repr(self._input)},
            'timestamp': self._ts.isoformat()
            }

    def load_result_from_obj(self, result_db_obj):
        self._input = Voltage(result_db_obj['input']['v'])
        self._ts = arrow.get(result_db_obj['timestamp'])


class FrequencyMeasurement(TestSimpleMeasurement):
    def __init__(self):
        super(FrequencyMeasurement, self).__init__()
        self._outputchannel = None
        self._inputtype = None
        self._inputchannel = None

    def do_measurement(self):
        """
        This function is present only because the instrument return value is
        not of a SignalPoint Type. Instrument classes should be changed to
        use Signal Point type instead and this class should fall back to the
        parent's implementation.
        """
        logger.debug("Making measurement : " + repr(self))
        if self._output is not None:
            if self._outputchannel is None:
                raise IOError("Output channel is not defined")
            self._outputchannel.set(self._output)

        if self.stime is not None:
            time.sleep(self.stime)

        if self._inputtype is not None:
            if self._inputchannel is None:
                raise IOError("Input channel is not defined")
            self._input = self._inputchannel.get()
            # if self._input.unitclass and \
            #         not self._input.unitclass == self._inputtype:
            #     raise TypeError(
            #         "Expected " + self._inputtype.unitclass +
            #         ", got " + type(self._input)
            #     )
        logger.info("Measured Frequency: " + repr(self._input))
        self._ts = arrow.utcnow()

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value
        self._inputtype = Frequency
        if self._parent._offline is not True:
            self._inputchannel = self._parent.instrument.frequency_input

    @property
    def input_frequency(self):
        return self._input

    def yesorno(self):
        pass

    def render(self):
        return {
            'input': {'hz': repr(self._input)},
            'timestamp': self._ts.isoformat()
            }

    def load_result_from_obj(self, result_db_obj):
        self._input = Frequency(result_db_obj['input']['hz'])
        self._ts = arrow.get(result_db_obj['timestamp'])


class DCCurrentMeasurement(TestSimpleMeasurement):
    def __init__(self):
        super(DCCurrentMeasurement, self).__init__()
        self._outputchannel = None
        self._inputtype = None
        self._inputchannel = None

    def do_measurement(self):
        """
        This function is present only because the instrument return value is
        not of a SignalPoint Type. Instrument classes should be changed to
        use Signal Point type instead and this class should fall back to the
        parent's implementation.
        """
        logger.debug("Making measurement : " + repr(self))
        if self._output is not None:
            if self._outputchannel is None:
                raise IOError("Output channel is not defined")
            self._outputchannel.set(self._output)

        if self.stime is not None:
            time.sleep(self.stime)

        if self._inputtype is not None:
            if self._inputchannel is None:
                raise IOError("Input channel is not defined")
            self._input = self._inputchannel.get()
            # if self._input.unitclass and \
            #         not self._input.unitclass == self._inputtype:
            #     raise TypeError(
            #         "Expected " + self._inputtype.unitclass +
            #         ", got " + type(self._input)
            #     )
        logger.info("Measured Current: " + repr(self._input))
        self._ts = arrow.utcnow()

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value
        self._inputtype = Current
        if self._parent._offline is not True:
            self._inputchannel = self._parent.instrument.current_input

    @property
    def input_current(self):
        return self._input

    def yesorno(self):
        pass

    def render(self):
        return {
            'input': {'i': repr(self._input)},
            'timestamp': self._ts.isoformat()
            }

    def load_result_from_obj(self, result_db_obj):
        self._input = Current(result_db_obj['input']['i'])
        self._ts = arrow.get(result_db_obj['timestamp'])


class TestUserMeasurement(TestMeasurementBase):
    def __init__(self, string):
        super(TestUserMeasurement, self).__init__()
        self._string = string
        self._user_input = None

    def do_measurement(self):
        while self.input_valid is False:
            self._user_input = raw_input(
                Fore.CYAN + self._string + ' [y/n] : ' + Fore.RESET
            ).strip()
        self._ts = arrow.utcnow()

    @property
    def input_valid(self):
        if self._user_input is None:
            return False
        if self._user_input.lower() in ['y', 'yes', 'ok', 'pass', 'n',
                                        'no', 'fail', 'true', 'false']:
            return True
        else:
            return False

    @property
    def yesorno(self):
        if self._user_input.lower() in ['y', 'yes', 'ok', 'pass', 'true']:
            return True
        else:
            return False

    def render(self):
        return {'question': self._string + ' [y/n] : ' + str(self.yesorno),
                'timestamp': self._ts.isoformat()}

    def load_result_from_obj(self, result_db_obj):
        self._ts = arrow.get(result_db_obj['timestamp'])
        self._user_input = result_db_obj['question'].split(' ')[-1]
