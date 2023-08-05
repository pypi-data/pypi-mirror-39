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

GetUVLightCallbackThreshold = namedtuple('UVLightCallbackThreshold', ['option', 'min', 'max'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletUVLight(Device):
    """
    Measures UV light
    """

    DEVICE_IDENTIFIER = 265
    DEVICE_DISPLAY_NAME = 'UV Light Bricklet'
    DEVICE_URL_PART = 'uv_light' # internal

    CALLBACK_UV_LIGHT = 8
    CALLBACK_UV_LIGHT_REACHED = 9


    FUNCTION_GET_UV_LIGHT = 1
    FUNCTION_SET_UV_LIGHT_CALLBACK_PERIOD = 2
    FUNCTION_GET_UV_LIGHT_CALLBACK_PERIOD = 3
    FUNCTION_SET_UV_LIGHT_CALLBACK_THRESHOLD = 4
    FUNCTION_GET_UV_LIGHT_CALLBACK_THRESHOLD = 5
    FUNCTION_SET_DEBOUNCE_PERIOD = 6
    FUNCTION_GET_DEBOUNCE_PERIOD = 7
    FUNCTION_GET_IDENTITY = 255

    THRESHOLD_OPTION_OFF = 'x'
    THRESHOLD_OPTION_OUTSIDE = 'o'
    THRESHOLD_OPTION_INSIDE = 'i'
    THRESHOLD_OPTION_SMALLER = '<'
    THRESHOLD_OPTION_GREATER = '>'

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

        self.response_expected[BrickletUVLight.FUNCTION_GET_UV_LIGHT] = BrickletUVLight.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletUVLight.FUNCTION_SET_UV_LIGHT_CALLBACK_PERIOD] = BrickletUVLight.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletUVLight.FUNCTION_GET_UV_LIGHT_CALLBACK_PERIOD] = BrickletUVLight.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletUVLight.FUNCTION_SET_UV_LIGHT_CALLBACK_THRESHOLD] = BrickletUVLight.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletUVLight.FUNCTION_GET_UV_LIGHT_CALLBACK_THRESHOLD] = BrickletUVLight.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletUVLight.FUNCTION_SET_DEBOUNCE_PERIOD] = BrickletUVLight.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletUVLight.FUNCTION_GET_DEBOUNCE_PERIOD] = BrickletUVLight.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletUVLight.FUNCTION_GET_IDENTITY] = BrickletUVLight.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletUVLight.CALLBACK_UV_LIGHT] = 'I'
        self.callback_formats[BrickletUVLight.CALLBACK_UV_LIGHT_REACHED] = 'I'


    def get_uv_light(self):
        """
        Returns the UV light intensity of the sensor, the intensity is given
        in 1/10 mW/m². The sensor has already weighted the intensity with the erythemal
        action spectrum to get the skin-affecting irradiation.

        To get UV index you just have to divide the value by 250. For example, a UV
        light intensity of 500 is equivalent to an UV index of 2.

        If you want to get the intensity periodically, it is recommended to use the
        :cb:`UV Light` callback and set the period with
        :func:`Set UV Light Callback Period`.
        """
        return self.ipcon.send_request(self, BrickletUVLight.FUNCTION_GET_UV_LIGHT, (), '', 'I')

    def set_uv_light_callback_period(self, period):
        """
        Sets the period in ms with which the :cb:`UV Light` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :cb:`UV Light` callback is only triggered if the intensity has changed since
        the last triggering.

        The default value is 0.
        """
        period = int(period)

        self.ipcon.send_request(self, BrickletUVLight.FUNCTION_SET_UV_LIGHT_CALLBACK_PERIOD, (period,), 'I', '')

    def get_uv_light_callback_period(self):
        """
        Returns the period as set by :func:`Set UV Light Callback Period`.
        """
        return self.ipcon.send_request(self, BrickletUVLight.FUNCTION_GET_UV_LIGHT_CALLBACK_PERIOD, (), '', 'I')

    def set_uv_light_callback_threshold(self, option, min, max):
        """
        Sets the thresholds for the :cb:`UV Light Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the intensity is *outside* the min and max values"
         "'i'",    "Callback is triggered when the intensity is *inside* the min and max values"
         "'<'",    "Callback is triggered when the intensity is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the intensity is greater than the min value (max is ignored)"

        The default value is ('x', 0, 0).
        """
        option = create_char(option)
        min = int(min)
        max = int(max)

        self.ipcon.send_request(self, BrickletUVLight.FUNCTION_SET_UV_LIGHT_CALLBACK_THRESHOLD, (option, min, max), 'c I I', '')

    def get_uv_light_callback_threshold(self):
        """
        Returns the threshold as set by :func:`Set UV Light Callback Threshold`.
        """
        return GetUVLightCallbackThreshold(*self.ipcon.send_request(self, BrickletUVLight.FUNCTION_GET_UV_LIGHT_CALLBACK_THRESHOLD, (), '', 'c I I'))

    def set_debounce_period(self, debounce):
        """
        Sets the period in ms with which the threshold callbacks

        * :cb:`UV Light Reached`,

        are triggered, if the thresholds

        * :func:`Set UV Light Callback Threshold`,

        keep being reached.

        The default value is 100.
        """
        debounce = int(debounce)

        self.ipcon.send_request(self, BrickletUVLight.FUNCTION_SET_DEBOUNCE_PERIOD, (debounce,), 'I', '')

    def get_debounce_period(self):
        """
        Returns the debounce period as set by :func:`Set Debounce Period`.
        """
        return self.ipcon.send_request(self, BrickletUVLight.FUNCTION_GET_DEBOUNCE_PERIOD, (), '', 'I')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be 'a', 'b', 'c' or 'd'.

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletUVLight.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, callback_id, function):
        """
        Registers the given *function* with the given *callback_id*.
        """
        if function is None:
            self.registered_callbacks.pop(callback_id, None)
        else:
            self.registered_callbacks[callback_id] = function

UVLight = BrickletUVLight # for backward compatibility
