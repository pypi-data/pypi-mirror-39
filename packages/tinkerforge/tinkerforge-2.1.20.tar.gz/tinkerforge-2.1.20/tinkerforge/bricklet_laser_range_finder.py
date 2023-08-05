# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2018-11-28.      #
#                                                           #
# Python Bindings Version 2.1.20                            #
#                                                           #
# If you have a bugfix for this file and want to commit it, #
# please fix the bug in the generator. You can find a link  #
# to the generators git repository on tinkerforge.com       #
#############################################################

from collections import namedtuple

try:
    from .ip_connection import Device, IPConnection, Error, create_char, create_char_list, create_string, create_chunk_data
except ValueError:
    from ip_connection import Device, IPConnection, Error, create_char, create_char_list, create_string, create_chunk_data

GetDistanceCallbackThreshold = namedtuple('DistanceCallbackThreshold', ['option', 'min', 'max'])
GetVelocityCallbackThreshold = namedtuple('VelocityCallbackThreshold', ['option', 'min', 'max'])
GetMovingAverage = namedtuple('MovingAverage', ['distance_average_length', 'velocity_average_length'])
GetConfiguration = namedtuple('Configuration', ['acquisition_count', 'enable_quick_termination', 'threshold_value', 'measurement_frequency'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletLaserRangeFinder(Device):
    """
    Measures distance up to 40m with laser light
    """

    DEVICE_IDENTIFIER = 255
    DEVICE_DISPLAY_NAME = 'Laser Range Finder Bricklet'
    DEVICE_URL_PART = 'laser_range_finder' # internal

    CALLBACK_DISTANCE = 20
    CALLBACK_VELOCITY = 21
    CALLBACK_DISTANCE_REACHED = 22
    CALLBACK_VELOCITY_REACHED = 23


    FUNCTION_GET_DISTANCE = 1
    FUNCTION_GET_VELOCITY = 2
    FUNCTION_SET_DISTANCE_CALLBACK_PERIOD = 3
    FUNCTION_GET_DISTANCE_CALLBACK_PERIOD = 4
    FUNCTION_SET_VELOCITY_CALLBACK_PERIOD = 5
    FUNCTION_GET_VELOCITY_CALLBACK_PERIOD = 6
    FUNCTION_SET_DISTANCE_CALLBACK_THRESHOLD = 7
    FUNCTION_GET_DISTANCE_CALLBACK_THRESHOLD = 8
    FUNCTION_SET_VELOCITY_CALLBACK_THRESHOLD = 9
    FUNCTION_GET_VELOCITY_CALLBACK_THRESHOLD = 10
    FUNCTION_SET_DEBOUNCE_PERIOD = 11
    FUNCTION_GET_DEBOUNCE_PERIOD = 12
    FUNCTION_SET_MOVING_AVERAGE = 13
    FUNCTION_GET_MOVING_AVERAGE = 14
    FUNCTION_SET_MODE = 15
    FUNCTION_GET_MODE = 16
    FUNCTION_ENABLE_LASER = 17
    FUNCTION_DISABLE_LASER = 18
    FUNCTION_IS_LASER_ENABLED = 19
    FUNCTION_GET_SENSOR_HARDWARE_VERSION = 24
    FUNCTION_SET_CONFIGURATION = 25
    FUNCTION_GET_CONFIGURATION = 26
    FUNCTION_GET_IDENTITY = 255

    THRESHOLD_OPTION_OFF = 'x'
    THRESHOLD_OPTION_OUTSIDE = 'o'
    THRESHOLD_OPTION_INSIDE = 'i'
    THRESHOLD_OPTION_SMALLER = '<'
    THRESHOLD_OPTION_GREATER = '>'
    MODE_DISTANCE = 0
    MODE_VELOCITY_MAX_13MS = 1
    MODE_VELOCITY_MAX_32MS = 2
    MODE_VELOCITY_MAX_64MS = 3
    MODE_VELOCITY_MAX_127MS = 4
    VERSION_1 = 1
    VERSION_3 = 3

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 1)

        self.response_expected[BrickletLaserRangeFinder.FUNCTION_GET_DISTANCE] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_GET_VELOCITY] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_SET_DISTANCE_CALLBACK_PERIOD] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_GET_DISTANCE_CALLBACK_PERIOD] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_SET_VELOCITY_CALLBACK_PERIOD] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_GET_VELOCITY_CALLBACK_PERIOD] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_SET_DISTANCE_CALLBACK_THRESHOLD] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_GET_DISTANCE_CALLBACK_THRESHOLD] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_SET_VELOCITY_CALLBACK_THRESHOLD] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_GET_VELOCITY_CALLBACK_THRESHOLD] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_SET_DEBOUNCE_PERIOD] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_GET_DEBOUNCE_PERIOD] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_SET_MOVING_AVERAGE] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_GET_MOVING_AVERAGE] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_SET_MODE] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_GET_MODE] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_ENABLE_LASER] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_DISABLE_LASER] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_IS_LASER_ENABLED] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_GET_SENSOR_HARDWARE_VERSION] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_SET_CONFIGURATION] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_GET_CONFIGURATION] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_GET_IDENTITY] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletLaserRangeFinder.CALLBACK_DISTANCE] = 'H'
        self.callback_formats[BrickletLaserRangeFinder.CALLBACK_VELOCITY] = 'h'
        self.callback_formats[BrickletLaserRangeFinder.CALLBACK_DISTANCE_REACHED] = 'H'
        self.callback_formats[BrickletLaserRangeFinder.CALLBACK_VELOCITY_REACHED] = 'h'


    def get_distance(self):
        """
        Returns the measured distance. The value has a range of 0 to 4000
        and is given in cm.

        Sensor hardware version 1 (see :func:`Get Sensor Hardware Version`) cannot
        measure distance and velocity at the same time. Therefore, the distance mode
        has to be enabled using :func:`Set Mode`.
        Sensor hardware version 3 can measure distance and velocity at the same
        time. Also the laser has to be enabled, see :func:`Enable Laser`.

        If you want to get the distance periodically, it is recommended to
        use the :cb:`Distance` callback and set the period with
        :func:`Set Distance Callback Period`.
        """
        return self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_GET_DISTANCE, (), '', 'H')

    def get_velocity(self):
        """
        Returns the measured velocity. The value has a range of -12800 to 12700
        and is given in 1/100 m/s.

        Sensor hardware version 1 (see :func:`Get Sensor Hardware Version`) cannot
        measure distance and velocity at the same time. Therefore, the velocity mode
        has to be enabled using :func:`Set Mode`.
        Sensor hardware version 3 can measure distance and velocity at the same
        time, but the velocity measurement only produces stables results if a fixed
        measurement rate (see :func:`Set Configuration`) is configured. Also the laser
        has to be enabled, see :func:`Enable Laser`.

        If you want to get the velocity periodically, it is recommended to
        use the :cb:`Velocity` callback and set the period with
        :func:`Set Velocity Callback Period`.
        """
        return self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_GET_VELOCITY, (), '', 'h')

    def set_distance_callback_period(self, period):
        """
        Sets the period in ms with which the :cb:`Distance` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :cb:`Distance` callback is only triggered if the distance value has
        changed since the last triggering.

        The default value is 0.
        """
        period = int(period)

        self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_SET_DISTANCE_CALLBACK_PERIOD, (period,), 'I', '')

    def get_distance_callback_period(self):
        """
        Returns the period as set by :func:`Set Distance Callback Period`.
        """
        return self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_GET_DISTANCE_CALLBACK_PERIOD, (), '', 'I')

    def set_velocity_callback_period(self, period):
        """
        Sets the period in ms with which the :cb:`Velocity` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :cb:`Velocity` callback is only triggered if the velocity value has
        changed since the last triggering.

        The default value is 0.
        """
        period = int(period)

        self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_SET_VELOCITY_CALLBACK_PERIOD, (period,), 'I', '')

    def get_velocity_callback_period(self):
        """
        Returns the period as set by :func:`Set Velocity Callback Period`.
        """
        return self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_GET_VELOCITY_CALLBACK_PERIOD, (), '', 'I')

    def set_distance_callback_threshold(self, option, min, max):
        """
        Sets the thresholds for the :cb:`Distance Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the distance value is *outside* the min and max values"
         "'i'",    "Callback is triggered when the distance value is *inside* the min and max values"
         "'<'",    "Callback is triggered when the distance value is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the distance value is greater than the min value (max is ignored)"

        The default value is ('x', 0, 0).
        """
        option = create_char(option)
        min = int(min)
        max = int(max)

        self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_SET_DISTANCE_CALLBACK_THRESHOLD, (option, min, max), 'c H H', '')

    def get_distance_callback_threshold(self):
        """
        Returns the threshold as set by :func:`Set Distance Callback Threshold`.
        """
        return GetDistanceCallbackThreshold(*self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_GET_DISTANCE_CALLBACK_THRESHOLD, (), '', 'c H H'))

    def set_velocity_callback_threshold(self, option, min, max):
        """
        Sets the thresholds for the :cb:`Velocity Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the velocity is *outside* the min and max values"
         "'i'",    "Callback is triggered when the velocity is *inside* the min and max values"
         "'<'",    "Callback is triggered when the velocity is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the velocity is greater than the min value (max is ignored)"

        The default value is ('x', 0, 0).
        """
        option = create_char(option)
        min = int(min)
        max = int(max)

        self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_SET_VELOCITY_CALLBACK_THRESHOLD, (option, min, max), 'c h h', '')

    def get_velocity_callback_threshold(self):
        """
        Returns the threshold as set by :func:`Set Velocity Callback Threshold`.
        """
        return GetVelocityCallbackThreshold(*self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_GET_VELOCITY_CALLBACK_THRESHOLD, (), '', 'c h h'))

    def set_debounce_period(self, debounce):
        """
        Sets the period in ms with which the threshold callbacks

        * :cb:`Distance Reached`,
        * :cb:`Velocity Reached`,

        are triggered, if the thresholds

        * :func:`Set Distance Callback Threshold`,
        * :func:`Set Velocity Callback Threshold`,

        keep being reached.

        The default value is 100.
        """
        debounce = int(debounce)

        self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_SET_DEBOUNCE_PERIOD, (debounce,), 'I', '')

    def get_debounce_period(self):
        """
        Returns the debounce period as set by :func:`Set Debounce Period`.
        """
        return self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_GET_DEBOUNCE_PERIOD, (), '', 'I')

    def set_moving_average(self, distance_average_length, velocity_average_length):
        """
        Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
        for the distance and velocity.

        Setting the length to 0 will turn the averaging completely off. With less
        averaging, there is more noise on the data.

        The range for the averaging is 0-30.

        The default value is 10.
        """
        distance_average_length = int(distance_average_length)
        velocity_average_length = int(velocity_average_length)

        self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_SET_MOVING_AVERAGE, (distance_average_length, velocity_average_length), 'B B', '')

    def get_moving_average(self):
        """
        Returns the length moving average as set by :func:`Set Moving Average`.
        """
        return GetMovingAverage(*self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_GET_MOVING_AVERAGE, (), '', 'B B'))

    def set_mode(self, mode):
        """
        .. note::
         This function is only available if you have a LIDAR-Lite sensor with hardware
         version 1. Use :func:`Set Configuration` for hardware version 3. You can check
         the sensor hardware version using :func:`Get Sensor Hardware Version`.

        The LIDAR-Lite sensor (hardware version 1) has five different modes. One mode is
        for distance measurements and four modes are for velocity measurements with
        different ranges.

        The following modes are available:

        * 0: Distance is measured with resolution 1.0 cm and range 0-400 cm
        * 1: Velocity is measured with resolution 0.1 m/s and range is 0-12.7 m/s
        * 2: Velocity is measured with resolution 0.25 m/s and range is 0-31.75 m/s
        * 3: Velocity is measured with resolution 0.5 m/s and range is 0-63.5 m/s
        * 4: Velocity is measured with resolution 1.0 m/s and range is 0-127 m/s

        The default mode is 0 (distance is measured).
        """
        mode = int(mode)

        self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_SET_MODE, (mode,), 'B', '')

    def get_mode(self):
        """
        Returns the mode as set by :func:`Set Mode`.
        """
        return self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_GET_MODE, (), '', 'B')

    def enable_laser(self):
        """
        Activates the laser of the LIDAR.

        We recommend that you wait 250ms after enabling the laser before
        the first call of :func:`Get Distance` to ensure stable measurements.
        """
        self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_ENABLE_LASER, (), '', '')

    def disable_laser(self):
        """
        Deactivates the laser of the LIDAR.
        """
        self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_DISABLE_LASER, (), '', '')

    def is_laser_enabled(self):
        """
        Returns *true* if the laser is enabled, *false* otherwise.
        """
        return self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_IS_LASER_ENABLED, (), '', '!')

    def get_sensor_hardware_version(self):
        """
        Returns the LIDAR-Lite hardware version.

        .. versionadded:: 2.0.3$nbsp;(Plugin)
        """
        return self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_GET_SENSOR_HARDWARE_VERSION, (), '', 'B')

    def set_configuration(self, acquisition_count, enable_quick_termination, threshold_value, measurement_frequency):
        """
        .. note::
         This function is only available if you have a LIDAR-Lite sensor with hardware
         version 3. Use :func:`Set Mode` for hardware version 1. You can check
         the sensor hardware version using :func:`Get Sensor Hardware Version`.

        The **Aquisition Count** defines the number of times the Laser Range Finder Bricklet
        will integrate acquisitions to find a correlation record peak. With a higher count,
        the Bricklet can measure longer distances. With a lower count, the rate increases. The
        allowed values are 1-255.

        If you set **Enable Quick Termination** to true, the distance measurement will be terminated
        early if a high peak was already detected. This means that a higher measurement rate can be achieved
        and long distances can be measured at the same time. However, the chance of false-positive
        distance measurements increases.

        Normally the distance is calculated with a detection algorithm that uses peak value,
        signal strength and noise. You can however also define a fixed **Threshold Value**.
        Set this to a low value if you want to measure the distance to something that has
        very little reflection (e.g. glass) and set it to a high value if you want to measure
        the distance to something with a very high reflection (e.g. mirror). Set this to 0 to
        use the default algorithm. The other allowed values are 1-255.

        Set the **Measurement Frequency** in Hz to force a fixed measurement rate. If set to 0,
        the Laser Range Finder Bricklet will use the optimal frequency according to the other
        configurations and the actual measured distance. Since the rate is not fixed in this case,
        the velocity measurement is not stable. For a stable velocity measurement you should
        set a fixed measurement frequency. The lower the frequency, the higher is the resolution
        of the calculated velocity. The allowed values are 10Hz-500Hz (and 0 to turn the fixed
        frequency off).

        The default values for Acquisition Count, Enable Quick Termination, Threshold Value and
        Measurement Frequency are 128, false, 0 and 0.

        .. versionadded:: 2.0.3$nbsp;(Plugin)
        """
        acquisition_count = int(acquisition_count)
        enable_quick_termination = bool(enable_quick_termination)
        threshold_value = int(threshold_value)
        measurement_frequency = int(measurement_frequency)

        self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_SET_CONFIGURATION, (acquisition_count, enable_quick_termination, threshold_value, measurement_frequency), 'B ! B H', '')

    def get_configuration(self):
        """
        Returns the configuration as set by :func:`Set Configuration`.

        .. versionadded:: 2.0.3$nbsp;(Plugin)
        """
        return GetConfiguration(*self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_GET_CONFIGURATION, (), '', 'B ! B H'))

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be 'a', 'b', 'c' or 'd'.

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, callback_id, function):
        """
        Registers the given *function* with the given *callback_id*.
        """
        if function is None:
            self.registered_callbacks.pop(callback_id, None)
        else:
            self.registered_callbacks[callback_id] = function

LaserRangeFinder = BrickletLaserRangeFinder # for backward compatibility
