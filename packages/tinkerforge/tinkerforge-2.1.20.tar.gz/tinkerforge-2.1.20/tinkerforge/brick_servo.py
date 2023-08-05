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

GetPulseWidth = namedtuple('PulseWidth', ['min', 'max'])
GetDegree = namedtuple('Degree', ['min', 'max'])
GetSPITFPBaudrateConfig = namedtuple('SPITFPBaudrateConfig', ['enable_dynamic_baudrate', 'minimum_dynamic_baudrate'])
GetSPITFPErrorCount = namedtuple('SPITFPErrorCount', ['error_count_ack_checksum', 'error_count_message_checksum', 'error_count_frame', 'error_count_overflow'])
GetProtocol1BrickletName = namedtuple('Protocol1BrickletName', ['protocol_version', 'firmware_version', 'name'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickServo(Device):
    """
    Drives up to 7 RC Servos with up to 3A
    """

    DEVICE_IDENTIFIER = 14
    DEVICE_DISPLAY_NAME = 'Servo Brick'
    DEVICE_URL_PART = 'servo' # internal

    CALLBACK_UNDER_VOLTAGE = 26
    CALLBACK_POSITION_REACHED = 27
    CALLBACK_VELOCITY_REACHED = 28


    FUNCTION_ENABLE = 1
    FUNCTION_DISABLE = 2
    FUNCTION_IS_ENABLED = 3
    FUNCTION_SET_POSITION = 4
    FUNCTION_GET_POSITION = 5
    FUNCTION_GET_CURRENT_POSITION = 6
    FUNCTION_SET_VELOCITY = 7
    FUNCTION_GET_VELOCITY = 8
    FUNCTION_GET_CURRENT_VELOCITY = 9
    FUNCTION_SET_ACCELERATION = 10
    FUNCTION_GET_ACCELERATION = 11
    FUNCTION_SET_OUTPUT_VOLTAGE = 12
    FUNCTION_GET_OUTPUT_VOLTAGE = 13
    FUNCTION_SET_PULSE_WIDTH = 14
    FUNCTION_GET_PULSE_WIDTH = 15
    FUNCTION_SET_DEGREE = 16
    FUNCTION_GET_DEGREE = 17
    FUNCTION_SET_PERIOD = 18
    FUNCTION_GET_PERIOD = 19
    FUNCTION_GET_SERVO_CURRENT = 20
    FUNCTION_GET_OVERALL_CURRENT = 21
    FUNCTION_GET_STACK_INPUT_VOLTAGE = 22
    FUNCTION_GET_EXTERNAL_INPUT_VOLTAGE = 23
    FUNCTION_SET_MINIMUM_VOLTAGE = 24
    FUNCTION_GET_MINIMUM_VOLTAGE = 25
    FUNCTION_ENABLE_POSITION_REACHED_CALLBACK = 29
    FUNCTION_DISABLE_POSITION_REACHED_CALLBACK = 30
    FUNCTION_IS_POSITION_REACHED_CALLBACK_ENABLED = 31
    FUNCTION_ENABLE_VELOCITY_REACHED_CALLBACK = 32
    FUNCTION_DISABLE_VELOCITY_REACHED_CALLBACK = 33
    FUNCTION_IS_VELOCITY_REACHED_CALLBACK_ENABLED = 34
    FUNCTION_SET_SPITFP_BAUDRATE_CONFIG = 231
    FUNCTION_GET_SPITFP_BAUDRATE_CONFIG = 232
    FUNCTION_GET_SEND_TIMEOUT_COUNT = 233
    FUNCTION_SET_SPITFP_BAUDRATE = 234
    FUNCTION_GET_SPITFP_BAUDRATE = 235
    FUNCTION_GET_SPITFP_ERROR_COUNT = 237
    FUNCTION_ENABLE_STATUS_LED = 238
    FUNCTION_DISABLE_STATUS_LED = 239
    FUNCTION_IS_STATUS_LED_ENABLED = 240
    FUNCTION_GET_PROTOCOL1_BRICKLET_NAME = 241
    FUNCTION_GET_CHIP_TEMPERATURE = 242
    FUNCTION_RESET = 243
    FUNCTION_GET_IDENTITY = 255

    COMMUNICATION_METHOD_NONE = 0
    COMMUNICATION_METHOD_USB = 1
    COMMUNICATION_METHOD_SPI_STACK = 2
    COMMUNICATION_METHOD_CHIBI = 3
    COMMUNICATION_METHOD_RS485 = 4
    COMMUNICATION_METHOD_WIFI = 5
    COMMUNICATION_METHOD_ETHERNET = 6
    COMMUNICATION_METHOD_WIFI_V2 = 7

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 4)

        self.response_expected[BrickServo.FUNCTION_ENABLE] = BrickServo.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickServo.FUNCTION_DISABLE] = BrickServo.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickServo.FUNCTION_IS_ENABLED] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_SET_POSITION] = BrickServo.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickServo.FUNCTION_GET_POSITION] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_GET_CURRENT_POSITION] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_SET_VELOCITY] = BrickServo.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickServo.FUNCTION_GET_VELOCITY] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_GET_CURRENT_VELOCITY] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_SET_ACCELERATION] = BrickServo.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickServo.FUNCTION_GET_ACCELERATION] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_SET_OUTPUT_VOLTAGE] = BrickServo.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickServo.FUNCTION_GET_OUTPUT_VOLTAGE] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_SET_PULSE_WIDTH] = BrickServo.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickServo.FUNCTION_GET_PULSE_WIDTH] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_SET_DEGREE] = BrickServo.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickServo.FUNCTION_GET_DEGREE] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_SET_PERIOD] = BrickServo.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickServo.FUNCTION_GET_PERIOD] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_GET_SERVO_CURRENT] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_GET_OVERALL_CURRENT] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_GET_STACK_INPUT_VOLTAGE] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_GET_EXTERNAL_INPUT_VOLTAGE] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_SET_MINIMUM_VOLTAGE] = BrickServo.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickServo.FUNCTION_GET_MINIMUM_VOLTAGE] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_ENABLE_POSITION_REACHED_CALLBACK] = BrickServo.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickServo.FUNCTION_DISABLE_POSITION_REACHED_CALLBACK] = BrickServo.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickServo.FUNCTION_IS_POSITION_REACHED_CALLBACK_ENABLED] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_ENABLE_VELOCITY_REACHED_CALLBACK] = BrickServo.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickServo.FUNCTION_DISABLE_VELOCITY_REACHED_CALLBACK] = BrickServo.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickServo.FUNCTION_IS_VELOCITY_REACHED_CALLBACK_ENABLED] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_SET_SPITFP_BAUDRATE_CONFIG] = BrickServo.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickServo.FUNCTION_GET_SPITFP_BAUDRATE_CONFIG] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_GET_SEND_TIMEOUT_COUNT] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_SET_SPITFP_BAUDRATE] = BrickServo.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickServo.FUNCTION_GET_SPITFP_BAUDRATE] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_GET_SPITFP_ERROR_COUNT] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_ENABLE_STATUS_LED] = BrickServo.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickServo.FUNCTION_DISABLE_STATUS_LED] = BrickServo.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickServo.FUNCTION_IS_STATUS_LED_ENABLED] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_GET_PROTOCOL1_BRICKLET_NAME] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_GET_CHIP_TEMPERATURE] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickServo.FUNCTION_RESET] = BrickServo.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickServo.FUNCTION_GET_IDENTITY] = BrickServo.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickServo.CALLBACK_UNDER_VOLTAGE] = 'H'
        self.callback_formats[BrickServo.CALLBACK_POSITION_REACHED] = 'B h'
        self.callback_formats[BrickServo.CALLBACK_VELOCITY_REACHED] = 'B h'


    def enable(self, servo_num):
        """
        Enables a servo (0 to 6). If a servo is enabled, the configured position,
        velocity, acceleration, etc. are applied immediately.
        """
        servo_num = int(servo_num)

        self.ipcon.send_request(self, BrickServo.FUNCTION_ENABLE, (servo_num,), 'B', '')

    def disable(self, servo_num):
        """
        Disables a servo (0 to 6). Disabled servos are not driven at all, i.e. a
        disabled servo will not hold its position if a load is applied.
        """
        servo_num = int(servo_num)

        self.ipcon.send_request(self, BrickServo.FUNCTION_DISABLE, (servo_num,), 'B', '')

    def is_enabled(self, servo_num):
        """
        Returns *true* if the specified servo is enabled, *false* otherwise.
        """
        servo_num = int(servo_num)

        return self.ipcon.send_request(self, BrickServo.FUNCTION_IS_ENABLED, (servo_num,), 'B', '!')

    def set_position(self, servo_num, position):
        """
        Sets the position in °/100 for the specified servo.

        The default range of the position is -9000 to 9000, but it can be specified
        according to your servo with :func:`Set Degree`.

        If you want to control a linear servo or RC brushless motor controller or
        similar with the Servo Brick, you can also define lengths or speeds with
        :func:`Set Degree`.
        """
        servo_num = int(servo_num)
        position = int(position)

        self.ipcon.send_request(self, BrickServo.FUNCTION_SET_POSITION, (servo_num, position), 'B h', '')

    def get_position(self, servo_num):
        """
        Returns the position of the specified servo as set by :func:`Set Position`.
        """
        servo_num = int(servo_num)

        return self.ipcon.send_request(self, BrickServo.FUNCTION_GET_POSITION, (servo_num,), 'B', 'h')

    def get_current_position(self, servo_num):
        """
        Returns the *current* position of the specified servo. This may not be the
        value of :func:`Set Position` if the servo is currently approaching a
        position goal.
        """
        servo_num = int(servo_num)

        return self.ipcon.send_request(self, BrickServo.FUNCTION_GET_CURRENT_POSITION, (servo_num,), 'B', 'h')

    def set_velocity(self, servo_num, velocity):
        """
        Sets the maximum velocity of the specified servo in °/100s. The velocity
        is accelerated according to the value set by :func:`Set Acceleration`.

        The minimum velocity is 0 (no movement) and the maximum velocity is 65535.
        With a value of 65535 the position will be set immediately (no velocity).

        The default value is 65535.
        """
        servo_num = int(servo_num)
        velocity = int(velocity)

        self.ipcon.send_request(self, BrickServo.FUNCTION_SET_VELOCITY, (servo_num, velocity), 'B H', '')

    def get_velocity(self, servo_num):
        """
        Returns the velocity of the specified servo as set by :func:`Set Velocity`.
        """
        servo_num = int(servo_num)

        return self.ipcon.send_request(self, BrickServo.FUNCTION_GET_VELOCITY, (servo_num,), 'B', 'H')

    def get_current_velocity(self, servo_num):
        """
        Returns the *current* velocity of the specified servo. This may not be the
        value of :func:`Set Velocity` if the servo is currently approaching a
        velocity goal.
        """
        servo_num = int(servo_num)

        return self.ipcon.send_request(self, BrickServo.FUNCTION_GET_CURRENT_VELOCITY, (servo_num,), 'B', 'H')

    def set_acceleration(self, servo_num, acceleration):
        """
        Sets the acceleration of the specified servo in °/100s².

        The minimum acceleration is 1 and the maximum acceleration is 65535.
        With a value of 65535 the velocity will be set immediately (no acceleration).

        The default value is 65535.
        """
        servo_num = int(servo_num)
        acceleration = int(acceleration)

        self.ipcon.send_request(self, BrickServo.FUNCTION_SET_ACCELERATION, (servo_num, acceleration), 'B H', '')

    def get_acceleration(self, servo_num):
        """
        Returns the acceleration for the specified servo as set by
        :func:`Set Acceleration`.
        """
        servo_num = int(servo_num)

        return self.ipcon.send_request(self, BrickServo.FUNCTION_GET_ACCELERATION, (servo_num,), 'B', 'H')

    def set_output_voltage(self, voltage):
        """
        Sets the output voltages with which the servos are driven in mV.
        The minimum output voltage is 2000mV and the maximum output voltage is
        9000mV.

        .. note::
         We recommend that you set this value to the maximum voltage that is
         specified for your servo, most servos achieve their maximum force only
         with high voltages.

        The default value is 5000.
        """
        voltage = int(voltage)

        self.ipcon.send_request(self, BrickServo.FUNCTION_SET_OUTPUT_VOLTAGE, (voltage,), 'H', '')

    def get_output_voltage(self):
        """
        Returns the output voltage as specified by :func:`Set Output Voltage`.
        """
        return self.ipcon.send_request(self, BrickServo.FUNCTION_GET_OUTPUT_VOLTAGE, (), '', 'H')

    def set_pulse_width(self, servo_num, min, max):
        """
        Sets the minimum and maximum pulse width of the specified servo in µs.

        Usually, servos are controlled with a
        `PWM <https://en.wikipedia.org/wiki/Pulse-width_modulation>`__, whereby the
        length of the pulse controls the position of the servo. Every servo has
        different minimum and maximum pulse widths, these can be specified with
        this function.

        If you have a datasheet for your servo that specifies the minimum and
        maximum pulse width, you should set the values accordingly. If your servo
        comes without any datasheet you have to find the values via trial and error.

        Both values have a range from 1 to 65535 (unsigned 16-bit integer). The
        minimum must be smaller than the maximum.

        The default values are 1000µs (1ms) and 2000µs (2ms) for minimum and
        maximum pulse width.
        """
        servo_num = int(servo_num)
        min = int(min)
        max = int(max)

        self.ipcon.send_request(self, BrickServo.FUNCTION_SET_PULSE_WIDTH, (servo_num, min, max), 'B H H', '')

    def get_pulse_width(self, servo_num):
        """
        Returns the minimum and maximum pulse width for the specified servo as set by
        :func:`Set Pulse Width`.
        """
        servo_num = int(servo_num)

        return GetPulseWidth(*self.ipcon.send_request(self, BrickServo.FUNCTION_GET_PULSE_WIDTH, (servo_num,), 'B', 'H H'))

    def set_degree(self, servo_num, min, max):
        """
        Sets the minimum and maximum degree for the specified servo (by default
        given as °/100).

        This only specifies the abstract values between which the minimum and maximum
        pulse width is scaled. For example: If you specify a pulse width of 1000µs
        to 2000µs and a degree range of -90° to 90°, a call of :func:`Set Position`
        with 0 will result in a pulse width of 1500µs
        (-90° = 1000µs, 90° = 2000µs, etc.).

        Possible usage:

        * The datasheet of your servo specifies a range of 200° with the middle position
          at 110°. In this case you can set the minimum to -9000 and the maximum to 11000.
        * You measure a range of 220° on your servo and you don't have or need a middle
          position. In this case you can set the minimum to 0 and the maximum to 22000.
        * You have a linear servo with a drive length of 20cm, In this case you could
          set the minimum to 0 and the maximum to 20000. Now you can set the Position
          with :func:`Set Position` with a resolution of cm/100. Also the velocity will
          have a resolution of cm/100s and the acceleration will have a resolution of
          cm/100s².
        * You don't care about units and just want the highest possible resolution. In
          this case you should set the minimum to -32767 and the maximum to 32767.
        * You have a brushless motor with a maximum speed of 10000 rpm and want to
          control it with a RC brushless motor controller. In this case you can set the
          minimum to 0 and the maximum to 10000. :func:`Set Position` now controls the rpm.

        Both values have a possible range from -32767 to 32767
        (signed 16-bit integer). The minimum must be smaller than the maximum.

        The default values are -9000 and 9000 for the minimum and maximum degree.
        """
        servo_num = int(servo_num)
        min = int(min)
        max = int(max)

        self.ipcon.send_request(self, BrickServo.FUNCTION_SET_DEGREE, (servo_num, min, max), 'B h h', '')

    def get_degree(self, servo_num):
        """
        Returns the minimum and maximum degree for the specified servo as set by
        :func:`Set Degree`.
        """
        servo_num = int(servo_num)

        return GetDegree(*self.ipcon.send_request(self, BrickServo.FUNCTION_GET_DEGREE, (servo_num,), 'B', 'h h'))

    def set_period(self, servo_num, period):
        """
        Sets the period of the specified servo in µs.

        Usually, servos are controlled with a
        `PWM <https://en.wikipedia.org/wiki/Pulse-width_modulation>`__. Different
        servos expect PWMs with different periods. Most servos run well with a
        period of about 20ms.

        If your servo comes with a datasheet that specifies a period, you should
        set it accordingly. If you don't have a datasheet and you have no idea
        what the correct period is, the default value (19.5ms) will most likely
        work fine.

        The minimum possible period is 1µs and the maximum is 65535µs.

        The default value is 19.5ms (19500µs).
        """
        servo_num = int(servo_num)
        period = int(period)

        self.ipcon.send_request(self, BrickServo.FUNCTION_SET_PERIOD, (servo_num, period), 'B H', '')

    def get_period(self, servo_num):
        """
        Returns the period for the specified servo as set by :func:`Set Period`.
        """
        servo_num = int(servo_num)

        return self.ipcon.send_request(self, BrickServo.FUNCTION_GET_PERIOD, (servo_num,), 'B', 'H')

    def get_servo_current(self, servo_num):
        """
        Returns the current consumption of the specified servo in mA.
        """
        servo_num = int(servo_num)

        return self.ipcon.send_request(self, BrickServo.FUNCTION_GET_SERVO_CURRENT, (servo_num,), 'B', 'H')

    def get_overall_current(self):
        """
        Returns the current consumption of all servos together in mA.
        """
        return self.ipcon.send_request(self, BrickServo.FUNCTION_GET_OVERALL_CURRENT, (), '', 'H')

    def get_stack_input_voltage(self):
        """
        Returns the stack input voltage in mV. The stack input voltage is the
        voltage that is supplied via the stack, i.e. it is given by a
        Step-Down or Step-Up Power Supply.
        """
        return self.ipcon.send_request(self, BrickServo.FUNCTION_GET_STACK_INPUT_VOLTAGE, (), '', 'H')

    def get_external_input_voltage(self):
        """
        Returns the external input voltage in mV. The external input voltage is
        given via the black power input connector on the Servo Brick.

        If there is an external input voltage and a stack input voltage, the motors
        will be driven by the external input voltage. If there is only a stack
        voltage present, the motors will be driven by this voltage.

        .. warning::
         This means, if you have a high stack voltage and a low external voltage,
         the motors will be driven with the low external voltage. If you then remove
         the external connection, it will immediately be driven by the high
         stack voltage
        """
        return self.ipcon.send_request(self, BrickServo.FUNCTION_GET_EXTERNAL_INPUT_VOLTAGE, (), '', 'H')

    def set_minimum_voltage(self, voltage):
        """
        Sets the minimum voltage in mV, below which the :cb:`Under Voltage` callback
        is triggered. The minimum possible value that works with the Servo Brick is 5V.
        You can use this function to detect the discharge of a battery that is used
        to drive the stepper motor. If you have a fixed power supply, you likely do
        not need this functionality.

        The default value is 5V (5000mV).
        """
        voltage = int(voltage)

        self.ipcon.send_request(self, BrickServo.FUNCTION_SET_MINIMUM_VOLTAGE, (voltage,), 'H', '')

    def get_minimum_voltage(self):
        """
        Returns the minimum voltage as set by :func:`Set Minimum Voltage`
        """
        return self.ipcon.send_request(self, BrickServo.FUNCTION_GET_MINIMUM_VOLTAGE, (), '', 'H')

    def enable_position_reached_callback(self):
        """
        Enables the :cb:`Position Reached` callback.

        Default is disabled.

        .. versionadded:: 2.0.1$nbsp;(Firmware)
        """
        self.ipcon.send_request(self, BrickServo.FUNCTION_ENABLE_POSITION_REACHED_CALLBACK, (), '', '')

    def disable_position_reached_callback(self):
        """
        Disables the :cb:`Position Reached` callback.

        Default is disabled.

        .. versionadded:: 2.0.1$nbsp;(Firmware)
        """
        self.ipcon.send_request(self, BrickServo.FUNCTION_DISABLE_POSITION_REACHED_CALLBACK, (), '', '')

    def is_position_reached_callback_enabled(self):
        """
        Returns *true* if :cb:`Position Reached` callback is enabled, *false* otherwise.

        .. versionadded:: 2.0.1$nbsp;(Firmware)
        """
        return self.ipcon.send_request(self, BrickServo.FUNCTION_IS_POSITION_REACHED_CALLBACK_ENABLED, (), '', '!')

    def enable_velocity_reached_callback(self):
        """
        Enables the :cb:`Velocity Reached` callback.

        Default is disabled.

        .. versionadded:: 2.0.1$nbsp;(Firmware)
        """
        self.ipcon.send_request(self, BrickServo.FUNCTION_ENABLE_VELOCITY_REACHED_CALLBACK, (), '', '')

    def disable_velocity_reached_callback(self):
        """
        Disables the :cb:`Velocity Reached` callback.

        Default is disabled.

        .. versionadded:: 2.0.1$nbsp;(Firmware)
        """
        self.ipcon.send_request(self, BrickServo.FUNCTION_DISABLE_VELOCITY_REACHED_CALLBACK, (), '', '')

    def is_velocity_reached_callback_enabled(self):
        """
        Returns *true* if :cb:`Velocity Reached` callback is enabled, *false* otherwise.

        .. versionadded:: 2.0.1$nbsp;(Firmware)
        """
        return self.ipcon.send_request(self, BrickServo.FUNCTION_IS_VELOCITY_REACHED_CALLBACK_ENABLED, (), '', '!')

    def set_spitfp_baudrate_config(self, enable_dynamic_baudrate, minimum_dynamic_baudrate):
        """
        The SPITF protocol can be used with a dynamic baudrate. If the dynamic baudrate is
        enabled, the Brick will try to adapt the baudrate for the communication
        between Bricks and Bricklets according to the amount of data that is transferred.

        The baudrate will be increased exponentially if lots of data is send/received and
        decreased linearly if little data is send/received.

        This lowers the baudrate in applications where little data is transferred (e.g.
        a weather station) and increases the robustness. If there is lots of data to transfer
        (e.g. Thermal Imaging Bricklet) it automatically increases the baudrate as needed.

        In cases where some data has to transferred as fast as possible every few seconds
        (e.g. RS485 Bricklet with a high baudrate but small payload) you may want to turn
        the dynamic baudrate off to get the highest possible performance.

        The maximum value of the baudrate can be set per port with the function
        :func:`Set SPITFP Baudrate`. If the dynamic baudrate is disabled, the baudrate
        as set by :func:`Set SPITFP Baudrate` will be used statically.

        The minimum dynamic baudrate has a value range of 400000 to 2000000 baud.

        By default dynamic baudrate is enabled and the minimum dynamic baudrate is 400000.

        .. versionadded:: 2.3.4$nbsp;(Firmware)
        """
        enable_dynamic_baudrate = bool(enable_dynamic_baudrate)
        minimum_dynamic_baudrate = int(minimum_dynamic_baudrate)

        self.ipcon.send_request(self, BrickServo.FUNCTION_SET_SPITFP_BAUDRATE_CONFIG, (enable_dynamic_baudrate, minimum_dynamic_baudrate), '! I', '')

    def get_spitfp_baudrate_config(self):
        """
        Returns the baudrate config, see :func:`Set SPITFP Baudrate Config`.

        .. versionadded:: 2.3.4$nbsp;(Firmware)
        """
        return GetSPITFPBaudrateConfig(*self.ipcon.send_request(self, BrickServo.FUNCTION_GET_SPITFP_BAUDRATE_CONFIG, (), '', '! I'))

    def get_send_timeout_count(self, communication_method):
        """
        Returns the timeout count for the different communication methods.

        The methods 0-2 are available for all Bricks, 3-7 only for Master Bricks.

        This function is mostly used for debugging during development, in normal operation
        the counters should nearly always stay at 0.

        .. versionadded:: 2.3.2$nbsp;(Firmware)
        """
        communication_method = int(communication_method)

        return self.ipcon.send_request(self, BrickServo.FUNCTION_GET_SEND_TIMEOUT_COUNT, (communication_method,), 'B', 'I')

    def set_spitfp_baudrate(self, bricklet_port, baudrate):
        """
        Sets the baudrate for a specific Bricklet port ('a' - 'd'). The
        baudrate can be in the range 400000 to 2000000.

        If you want to increase the throughput of Bricklets you can increase
        the baudrate. If you get a high error count because of high
        interference (see :func:`Get SPITFP Error Count`) you can decrease the
        baudrate.

        If the dynamic baudrate feature is enabled, the baudrate set by this
        function corresponds to the maximum baudrate (see :func:`Set SPITFP Baudrate Config`).

        Regulatory testing is done with the default baudrate. If CE compatibility
        or similar is necessary in you applications we recommend to not change
        the baudrate.

        The default baudrate for all ports is 1400000.

        .. versionadded:: 2.3.2$nbsp;(Firmware)
        """
        bricklet_port = create_char(bricklet_port)
        baudrate = int(baudrate)

        self.ipcon.send_request(self, BrickServo.FUNCTION_SET_SPITFP_BAUDRATE, (bricklet_port, baudrate), 'c I', '')

    def get_spitfp_baudrate(self, bricklet_port):
        """
        Returns the baudrate for a given Bricklet port, see :func:`Set SPITFP Baudrate`.

        .. versionadded:: 2.3.2$nbsp;(Firmware)
        """
        bricklet_port = create_char(bricklet_port)

        return self.ipcon.send_request(self, BrickServo.FUNCTION_GET_SPITFP_BAUDRATE, (bricklet_port,), 'c', 'I')

    def get_spitfp_error_count(self, bricklet_port):
        """
        Returns the error count for the communication between Brick and Bricklet.

        The errors are divided into

        * ACK checksum errors,
        * message checksum errors,
        * framing errors and
        * overflow errors.

        The errors counts are for errors that occur on the Brick side. All
        Bricklets have a similar function that returns the errors on the Bricklet side.

        .. versionadded:: 2.3.2$nbsp;(Firmware)
        """
        bricklet_port = create_char(bricklet_port)

        return GetSPITFPErrorCount(*self.ipcon.send_request(self, BrickServo.FUNCTION_GET_SPITFP_ERROR_COUNT, (bricklet_port,), 'c', 'I I I I'))

    def enable_status_led(self):
        """
        Enables the status LED.

        The status LED is the blue LED next to the USB connector. If enabled is is
        on and it flickers if data is transfered. If disabled it is always off.

        The default state is enabled.

        .. versionadded:: 2.3.1$nbsp;(Firmware)
        """
        self.ipcon.send_request(self, BrickServo.FUNCTION_ENABLE_STATUS_LED, (), '', '')

    def disable_status_led(self):
        """
        Disables the status LED.

        The status LED is the blue LED next to the USB connector. If enabled is is
        on and it flickers if data is transfered. If disabled it is always off.

        The default state is enabled.

        .. versionadded:: 2.3.1$nbsp;(Firmware)
        """
        self.ipcon.send_request(self, BrickServo.FUNCTION_DISABLE_STATUS_LED, (), '', '')

    def is_status_led_enabled(self):
        """
        Returns *true* if the status LED is enabled, *false* otherwise.

        .. versionadded:: 2.3.1$nbsp;(Firmware)
        """
        return self.ipcon.send_request(self, BrickServo.FUNCTION_IS_STATUS_LED_ENABLED, (), '', '!')

    def get_protocol1_bricklet_name(self, port):
        """
        Returns the firmware and protocol version and the name of the Bricklet for a
        given port.

        This functions sole purpose is to allow automatic flashing of v1.x.y Bricklet
        plugins.
        """
        port = create_char(port)

        return GetProtocol1BrickletName(*self.ipcon.send_request(self, BrickServo.FUNCTION_GET_PROTOCOL1_BRICKLET_NAME, (port,), 'c', 'B 3B 40s'))

    def get_chip_temperature(self):
        """
        Returns the temperature in °C/10 as measured inside the microcontroller. The
        value returned is not the ambient temperature!

        The temperature is only proportional to the real temperature and it has an
        accuracy of +-15%. Practically it is only useful as an indicator for
        temperature changes.
        """
        return self.ipcon.send_request(self, BrickServo.FUNCTION_GET_CHIP_TEMPERATURE, (), '', 'h')

    def reset(self):
        """
        Calling this function will reset the Brick. Calling this function
        on a Brick inside of a stack will reset the whole stack.

        After a reset you have to create new device objects,
        calling functions on the existing ones will result in
        undefined behavior!
        """
        self.ipcon.send_request(self, BrickServo.FUNCTION_RESET, (), '', '')

    def get_identity(self):
        """
        Returns the UID, the UID where the Brick is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be '0'-'8' (stack position).

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickServo.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, callback_id, function):
        """
        Registers the given *function* with the given *callback_id*.
        """
        if function is None:
            self.registered_callbacks.pop(callback_id, None)
        else:
            self.registered_callbacks[callback_id] = function

Servo = BrickServo # for backward compatibility
