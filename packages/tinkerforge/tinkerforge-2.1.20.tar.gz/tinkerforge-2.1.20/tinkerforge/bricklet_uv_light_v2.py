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

GetUVACallbackConfiguration = namedtuple('UVACallbackConfiguration', ['period', 'value_has_to_change', 'option', 'min', 'max'])
GetUVBCallbackConfiguration = namedtuple('UVBCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'min', 'max'])
GetUVICallbackConfiguration = namedtuple('UVICallbackConfiguration', ['period', 'value_has_to_change', 'option', 'min', 'max'])
GetSPITFPErrorCount = namedtuple('SPITFPErrorCount', ['error_count_ack_checksum', 'error_count_message_checksum', 'error_count_frame', 'error_count_overflow'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletUVLightV2(Device):
    """
    Measures UV-A, UV-B and UV index
    """

    DEVICE_IDENTIFIER = 2118
    DEVICE_DISPLAY_NAME = 'UV Light Bricklet 2.0'
    DEVICE_URL_PART = 'uv_light_v2' # internal

    CALLBACK_UVA = 4
    CALLBACK_UVB = 8
    CALLBACK_UVI = 12


    FUNCTION_GET_UVA = 1
    FUNCTION_SET_UVA_CALLBACK_CONFIGURATION = 2
    FUNCTION_GET_UVA_CALLBACK_CONFIGURATION = 3
    FUNCTION_GET_UVB = 5
    FUNCTION_SET_UVB_CALLBACK_CONFIGURATION = 6
    FUNCTION_GET_UVB_CALLBACK_CONFIGURATION = 7
    FUNCTION_GET_UVI = 9
    FUNCTION_SET_UVI_CALLBACK_CONFIGURATION = 10
    FUNCTION_GET_UVI_CALLBACK_CONFIGURATION = 11
    FUNCTION_SET_CONFIGURATION = 13
    FUNCTION_GET_CONFIGURATION = 14
    FUNCTION_GET_SPITFP_ERROR_COUNT = 234
    FUNCTION_SET_BOOTLOADER_MODE = 235
    FUNCTION_GET_BOOTLOADER_MODE = 236
    FUNCTION_SET_WRITE_FIRMWARE_POINTER = 237
    FUNCTION_WRITE_FIRMWARE = 238
    FUNCTION_SET_STATUS_LED_CONFIG = 239
    FUNCTION_GET_STATUS_LED_CONFIG = 240
    FUNCTION_GET_CHIP_TEMPERATURE = 242
    FUNCTION_RESET = 243
    FUNCTION_WRITE_UID = 248
    FUNCTION_READ_UID = 249
    FUNCTION_GET_IDENTITY = 255

    THRESHOLD_OPTION_OFF = 'x'
    THRESHOLD_OPTION_OUTSIDE = 'o'
    THRESHOLD_OPTION_INSIDE = 'i'
    THRESHOLD_OPTION_SMALLER = '<'
    THRESHOLD_OPTION_GREATER = '>'
    INTEGRATION_TIME_50MS = 0
    INTEGRATION_TIME_100MS = 1
    INTEGRATION_TIME_200MS = 2
    INTEGRATION_TIME_400MS = 3
    INTEGRATION_TIME_800MS = 4
    BOOTLOADER_MODE_BOOTLOADER = 0
    BOOTLOADER_MODE_FIRMWARE = 1
    BOOTLOADER_MODE_BOOTLOADER_WAIT_FOR_REBOOT = 2
    BOOTLOADER_MODE_FIRMWARE_WAIT_FOR_REBOOT = 3
    BOOTLOADER_MODE_FIRMWARE_WAIT_FOR_ERASE_AND_REBOOT = 4
    BOOTLOADER_STATUS_OK = 0
    BOOTLOADER_STATUS_INVALID_MODE = 1
    BOOTLOADER_STATUS_NO_CHANGE = 2
    BOOTLOADER_STATUS_ENTRY_FUNCTION_NOT_PRESENT = 3
    BOOTLOADER_STATUS_DEVICE_IDENTIFIER_INCORRECT = 4
    BOOTLOADER_STATUS_CRC_MISMATCH = 5
    STATUS_LED_CONFIG_OFF = 0
    STATUS_LED_CONFIG_ON = 1
    STATUS_LED_CONFIG_SHOW_HEARTBEAT = 2
    STATUS_LED_CONFIG_SHOW_STATUS = 3

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

        self.response_expected[BrickletUVLightV2.FUNCTION_GET_UVA] = BrickletUVLightV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletUVLightV2.FUNCTION_SET_UVA_CALLBACK_CONFIGURATION] = BrickletUVLightV2.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletUVLightV2.FUNCTION_GET_UVA_CALLBACK_CONFIGURATION] = BrickletUVLightV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletUVLightV2.FUNCTION_GET_UVB] = BrickletUVLightV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletUVLightV2.FUNCTION_SET_UVB_CALLBACK_CONFIGURATION] = BrickletUVLightV2.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletUVLightV2.FUNCTION_GET_UVB_CALLBACK_CONFIGURATION] = BrickletUVLightV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletUVLightV2.FUNCTION_GET_UVI] = BrickletUVLightV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletUVLightV2.FUNCTION_SET_UVI_CALLBACK_CONFIGURATION] = BrickletUVLightV2.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletUVLightV2.FUNCTION_GET_UVI_CALLBACK_CONFIGURATION] = BrickletUVLightV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletUVLightV2.FUNCTION_SET_CONFIGURATION] = BrickletUVLightV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletUVLightV2.FUNCTION_GET_CONFIGURATION] = BrickletUVLightV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletUVLightV2.FUNCTION_GET_SPITFP_ERROR_COUNT] = BrickletUVLightV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletUVLightV2.FUNCTION_SET_BOOTLOADER_MODE] = BrickletUVLightV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletUVLightV2.FUNCTION_GET_BOOTLOADER_MODE] = BrickletUVLightV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletUVLightV2.FUNCTION_SET_WRITE_FIRMWARE_POINTER] = BrickletUVLightV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletUVLightV2.FUNCTION_WRITE_FIRMWARE] = BrickletUVLightV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletUVLightV2.FUNCTION_SET_STATUS_LED_CONFIG] = BrickletUVLightV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletUVLightV2.FUNCTION_GET_STATUS_LED_CONFIG] = BrickletUVLightV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletUVLightV2.FUNCTION_GET_CHIP_TEMPERATURE] = BrickletUVLightV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletUVLightV2.FUNCTION_RESET] = BrickletUVLightV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletUVLightV2.FUNCTION_WRITE_UID] = BrickletUVLightV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletUVLightV2.FUNCTION_READ_UID] = BrickletUVLightV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletUVLightV2.FUNCTION_GET_IDENTITY] = BrickletUVLightV2.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletUVLightV2.CALLBACK_UVA] = 'i'
        self.callback_formats[BrickletUVLightV2.CALLBACK_UVB] = 'i'
        self.callback_formats[BrickletUVLightV2.CALLBACK_UVI] = 'i'


    def get_uva(self):
        """
        Returns the UVA intensity of the sensor, the intensity is given
        in 1/10 mW/m². The sensor has not weighted the intensity with the erythemal
        action spectrum to get the skin-affecting irradiation. Therefore, you cannot
        just divide the value by 250 to get the UVA index. To get the UV index use
        :func:`Get UVI`.

        If the sensor is saturated, then -1 is returned, see :func:`Set Configuration`.

        If you want to get the intensity periodically, it is recommended to use the
        :cb:`UVA` callback and set the period with
        :func:`Set UVA Callback Configuration`.


        If you want to get the value periodically, it is recommended to use the
        :cb:`UVA` callback. You can set the callback configuration
        with :func:`Set UVA Callback Configuration`.
        """
        return self.ipcon.send_request(self, BrickletUVLightV2.FUNCTION_GET_UVA, (), '', 'i')

    def set_uva_callback_configuration(self, period, value_has_to_change, option, min, max):
        """
        The period in ms is the period with which the :cb:`UVA` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`UVA` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Threshold is turned off"
         "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
         "'i'",    "Threshold is triggered when the value is *inside* or equal to the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"

        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.

        The default value is (0, false, 'x', 0, 0).
        """
        period = int(period)
        value_has_to_change = bool(value_has_to_change)
        option = create_char(option)
        min = int(min)
        max = int(max)

        self.ipcon.send_request(self, BrickletUVLightV2.FUNCTION_SET_UVA_CALLBACK_CONFIGURATION, (period, value_has_to_change, option, min, max), 'I ! c i i', '')

    def get_uva_callback_configuration(self):
        """
        Returns the callback configuration as set by :func:`Set UVA Callback Configuration`.
        """
        return GetUVACallbackConfiguration(*self.ipcon.send_request(self, BrickletUVLightV2.FUNCTION_GET_UVA_CALLBACK_CONFIGURATION, (), '', 'I ! c i i'))

    def get_uvb(self):
        """
        Returns the UVB intensity of the sensor, the intensity is given
        in 1/10 mW/m². The sensor has not weighted the intensity with the erythemal
        action spectrum to get the skin-affecting irradiation. Therefore, you cannot
        just divide the value by 250 to get the UVB index. To get the UV index use
        :func:`Get UVI`.

        If the sensor is saturated, then -1 is returned, see :func:`Set Configuration`.

        If you want to get the intensity periodically, it is recommended to use the
        :cb:`UVB` callback and set the period with
        :func:`Set UVB Callback Configuration`.


        If you want to get the value periodically, it is recommended to use the
        :cb:`UVB` callback. You can set the callback configuration
        with :func:`Set UVB Callback Configuration`.
        """
        return self.ipcon.send_request(self, BrickletUVLightV2.FUNCTION_GET_UVB, (), '', 'i')

    def set_uvb_callback_configuration(self, period, value_has_to_change, option, min, max):
        """
        The period in ms is the period with which the :cb:`UVB` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`UVB` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Threshold is turned off"
         "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
         "'i'",    "Threshold is triggered when the value is *inside* or equal to the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"

        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.

        The default value is (0, false, 'x', 0, 0).
        """
        period = int(period)
        value_has_to_change = bool(value_has_to_change)
        option = create_char(option)
        min = int(min)
        max = int(max)

        self.ipcon.send_request(self, BrickletUVLightV2.FUNCTION_SET_UVB_CALLBACK_CONFIGURATION, (period, value_has_to_change, option, min, max), 'I ! c i i', '')

    def get_uvb_callback_configuration(self):
        """
        Returns the callback configuration as set by :func:`Set UVB Callback Configuration`.
        """
        return GetUVBCallbackConfiguration(*self.ipcon.send_request(self, BrickletUVLightV2.FUNCTION_GET_UVB_CALLBACK_CONFIGURATION, (), '', 'I ! c i i'))

    def get_uvi(self):
        """
        Returns the UV index of the sensor, the index is given in 1/10.

        If the sensor is saturated, then -1 is returned, see :func:`Set Configuration`.

        If you want to get the intensity periodically, it is recommended to use the
        :cb:`UVI` callback and set the period with
        :func:`Set UVI Callback Configuration`.


        If you want to get the value periodically, it is recommended to use the
        :cb:`UVI` callback. You can set the callback configuration
        with :func:`Set UVI Callback Configuration`.
        """
        return self.ipcon.send_request(self, BrickletUVLightV2.FUNCTION_GET_UVI, (), '', 'i')

    def set_uvi_callback_configuration(self, period, value_has_to_change, option, min, max):
        """
        The period in ms is the period with which the :cb:`UVI` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`UVI` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Threshold is turned off"
         "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
         "'i'",    "Threshold is triggered when the value is *inside* or equal to the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"

        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.

        The default value is (0, false, 'x', 0, 0).
        """
        period = int(period)
        value_has_to_change = bool(value_has_to_change)
        option = create_char(option)
        min = int(min)
        max = int(max)

        self.ipcon.send_request(self, BrickletUVLightV2.FUNCTION_SET_UVI_CALLBACK_CONFIGURATION, (period, value_has_to_change, option, min, max), 'I ! c i i', '')

    def get_uvi_callback_configuration(self):
        """
        Returns the callback configuration as set by :func:`Set UVI Callback Configuration`.
        """
        return GetUVICallbackConfiguration(*self.ipcon.send_request(self, BrickletUVLightV2.FUNCTION_GET_UVI_CALLBACK_CONFIGURATION, (), '', 'I ! c i i'))

    def set_configuration(self, integration_time):
        """
        Sets the configuration of the sensor. The integration time can be configured
        between 50 and 800 ms. With a shorter integration time the sensor reading updates
        more often but contains more noise. With a longer integration the sensor reading
        contains less noise but updates less often.

        With a longer integration time (especially 800 ms) and a higher UV intensity the
        sensor can be saturated. If this happens the UVA/UVB/UVI readings are all -1.
        In this case you need to choose a shorter integration time.

        Default value: 400 ms.
        """
        integration_time = int(integration_time)

        self.ipcon.send_request(self, BrickletUVLightV2.FUNCTION_SET_CONFIGURATION, (integration_time,), 'B', '')

    def get_configuration(self):
        """
        Returns the configuration as set by :func:`Set Configuration`.
        """
        return self.ipcon.send_request(self, BrickletUVLightV2.FUNCTION_GET_CONFIGURATION, (), '', 'B')

    def get_spitfp_error_count(self):
        """
        Returns the error count for the communication between Brick and Bricklet.

        The errors are divided into

        * ACK checksum errors,
        * message checksum errors,
        * framing errors and
        * overflow errors.

        The errors counts are for errors that occur on the Bricklet side. All
        Bricks have a similar function that returns the errors on the Brick side.
        """
        return GetSPITFPErrorCount(*self.ipcon.send_request(self, BrickletUVLightV2.FUNCTION_GET_SPITFP_ERROR_COUNT, (), '', 'I I I I'))

    def set_bootloader_mode(self, mode):
        """
        Sets the bootloader mode and returns the status after the requested
        mode change was instigated.

        You can change from bootloader mode to firmware mode and vice versa. A change
        from bootloader mode to firmware mode will only take place if the entry function,
        device identifier and CRC are present and correct.

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        mode = int(mode)

        return self.ipcon.send_request(self, BrickletUVLightV2.FUNCTION_SET_BOOTLOADER_MODE, (mode,), 'B', 'B')

    def get_bootloader_mode(self):
        """
        Returns the current bootloader mode, see :func:`Set Bootloader Mode`.
        """
        return self.ipcon.send_request(self, BrickletUVLightV2.FUNCTION_GET_BOOTLOADER_MODE, (), '', 'B')

    def set_write_firmware_pointer(self, pointer):
        """
        Sets the firmware pointer for :func:`Write Firmware`. The pointer has
        to be increased by chunks of size 64. The data is written to flash
        every 4 chunks (which equals to one page of size 256).

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        pointer = int(pointer)

        self.ipcon.send_request(self, BrickletUVLightV2.FUNCTION_SET_WRITE_FIRMWARE_POINTER, (pointer,), 'I', '')

    def write_firmware(self, data):
        """
        Writes 64 Bytes of firmware at the position as written by
        :func:`Set Write Firmware Pointer` before. The firmware is written
        to flash every 4 chunks.

        You can only write firmware in bootloader mode.

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        data = list(map(int, data))

        return self.ipcon.send_request(self, BrickletUVLightV2.FUNCTION_WRITE_FIRMWARE, (data,), '64B', 'B')

    def set_status_led_config(self, config):
        """
        Sets the status LED configuration. By default the LED shows
        communication traffic between Brick and Bricklet, it flickers once
        for every 10 received data packets.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is will show heartbeat by default.
        """
        config = int(config)

        self.ipcon.send_request(self, BrickletUVLightV2.FUNCTION_SET_STATUS_LED_CONFIG, (config,), 'B', '')

    def get_status_led_config(self):
        """
        Returns the configuration as set by :func:`Set Status LED Config`
        """
        return self.ipcon.send_request(self, BrickletUVLightV2.FUNCTION_GET_STATUS_LED_CONFIG, (), '', 'B')

    def get_chip_temperature(self):
        """
        Returns the temperature in °C as measured inside the microcontroller. The
        value returned is not the ambient temperature!

        The temperature is only proportional to the real temperature and it has bad
        accuracy. Practically it is only useful as an indicator for
        temperature changes.
        """
        return self.ipcon.send_request(self, BrickletUVLightV2.FUNCTION_GET_CHIP_TEMPERATURE, (), '', 'h')

    def reset(self):
        """
        Calling this function will reset the Bricklet. All configurations
        will be lost.

        After a reset you have to create new device objects,
        calling functions on the existing ones will result in
        undefined behavior!
        """
        self.ipcon.send_request(self, BrickletUVLightV2.FUNCTION_RESET, (), '', '')

    def write_uid(self, uid):
        """
        Writes a new UID into flash. If you want to set a new UID
        you have to decode the Base58 encoded UID string into an
        integer first.

        We recommend that you use Brick Viewer to change the UID.
        """
        uid = int(uid)

        self.ipcon.send_request(self, BrickletUVLightV2.FUNCTION_WRITE_UID, (uid,), 'I', '')

    def read_uid(self):
        """
        Returns the current UID as an integer. Encode as
        Base58 to get the usual string version.
        """
        return self.ipcon.send_request(self, BrickletUVLightV2.FUNCTION_READ_UID, (), '', 'I')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be 'a', 'b', 'c' or 'd'.

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletUVLightV2.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, callback_id, function):
        """
        Registers the given *function* with the given *callback_id*.
        """
        if function is None:
            self.registered_callbacks.pop(callback_id, None)
        else:
            self.registered_callbacks[callback_id] = function

UVLightV2 = BrickletUVLightV2 # for backward compatibility
