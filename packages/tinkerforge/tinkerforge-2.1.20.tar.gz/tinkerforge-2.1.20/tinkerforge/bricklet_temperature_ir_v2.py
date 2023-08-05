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

GetAmbientTemperatureCallbackConfiguration = namedtuple('AmbientTemperatureCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'min', 'max'])
GetObjectTemperatureCallbackConfiguration = namedtuple('ObjectTemperatureCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'min', 'max'])
GetSPITFPErrorCount = namedtuple('SPITFPErrorCount', ['error_count_ack_checksum', 'error_count_message_checksum', 'error_count_frame', 'error_count_overflow'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletTemperatureIRV2(Device):
    """
    Measures contactless object temperature between -70°C and +380°C
    """

    DEVICE_IDENTIFIER = 291
    DEVICE_DISPLAY_NAME = 'Temperature IR Bricklet 2.0'
    DEVICE_URL_PART = 'temperature_ir_v2' # internal

    CALLBACK_AMBIENT_TEMPERATURE = 4
    CALLBACK_OBJECT_TEMPERATURE = 8


    FUNCTION_GET_AMBIENT_TEMPERATURE = 1
    FUNCTION_SET_AMBIENT_TEMPERATURE_CALLBACK_CONFIGURATION = 2
    FUNCTION_GET_AMBIENT_TEMPERATURE_CALLBACK_CONFIGURATION = 3
    FUNCTION_GET_OBJECT_TEMPERATURE = 5
    FUNCTION_SET_OBJECT_TEMPERATURE_CALLBACK_CONFIGURATION = 6
    FUNCTION_GET_OBJECT_TEMPERATURE_CALLBACK_CONFIGURATION = 7
    FUNCTION_SET_EMISSIVITY = 9
    FUNCTION_GET_EMISSIVITY = 10
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

        self.api_version = (2, 0, 1)

        self.response_expected[BrickletTemperatureIRV2.FUNCTION_GET_AMBIENT_TEMPERATURE] = BrickletTemperatureIRV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletTemperatureIRV2.FUNCTION_SET_AMBIENT_TEMPERATURE_CALLBACK_CONFIGURATION] = BrickletTemperatureIRV2.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletTemperatureIRV2.FUNCTION_GET_AMBIENT_TEMPERATURE_CALLBACK_CONFIGURATION] = BrickletTemperatureIRV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletTemperatureIRV2.FUNCTION_GET_OBJECT_TEMPERATURE] = BrickletTemperatureIRV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletTemperatureIRV2.FUNCTION_SET_OBJECT_TEMPERATURE_CALLBACK_CONFIGURATION] = BrickletTemperatureIRV2.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletTemperatureIRV2.FUNCTION_GET_OBJECT_TEMPERATURE_CALLBACK_CONFIGURATION] = BrickletTemperatureIRV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletTemperatureIRV2.FUNCTION_SET_EMISSIVITY] = BrickletTemperatureIRV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletTemperatureIRV2.FUNCTION_GET_EMISSIVITY] = BrickletTemperatureIRV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletTemperatureIRV2.FUNCTION_GET_SPITFP_ERROR_COUNT] = BrickletTemperatureIRV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletTemperatureIRV2.FUNCTION_SET_BOOTLOADER_MODE] = BrickletTemperatureIRV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletTemperatureIRV2.FUNCTION_GET_BOOTLOADER_MODE] = BrickletTemperatureIRV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletTemperatureIRV2.FUNCTION_SET_WRITE_FIRMWARE_POINTER] = BrickletTemperatureIRV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletTemperatureIRV2.FUNCTION_WRITE_FIRMWARE] = BrickletTemperatureIRV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletTemperatureIRV2.FUNCTION_SET_STATUS_LED_CONFIG] = BrickletTemperatureIRV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletTemperatureIRV2.FUNCTION_GET_STATUS_LED_CONFIG] = BrickletTemperatureIRV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletTemperatureIRV2.FUNCTION_GET_CHIP_TEMPERATURE] = BrickletTemperatureIRV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletTemperatureIRV2.FUNCTION_RESET] = BrickletTemperatureIRV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletTemperatureIRV2.FUNCTION_WRITE_UID] = BrickletTemperatureIRV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletTemperatureIRV2.FUNCTION_READ_UID] = BrickletTemperatureIRV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletTemperatureIRV2.FUNCTION_GET_IDENTITY] = BrickletTemperatureIRV2.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletTemperatureIRV2.CALLBACK_AMBIENT_TEMPERATURE] = 'h'
        self.callback_formats[BrickletTemperatureIRV2.CALLBACK_OBJECT_TEMPERATURE] = 'h'


    def get_ambient_temperature(self):
        """
        Returns the ambient temperature of the sensor. The value
        has a range of -400 to 1250 and is given in °C/10,
        e.g. a value of 423 means that an ambient temperature of 42.3 °C is
        measured.

        If you want to get the ambient temperature periodically, it is recommended
        to use the :cb:`Ambient Temperature` callback and set the period with
        :func:`Set Ambient Temperature Callback Configuration`.


        If you want to get the value periodically, it is recommended to use the
        :cb:`Ambient Temperature` callback. You can set the callback configuration
        with :func:`Set Ambient Temperature Callback Configuration`.
        """
        return self.ipcon.send_request(self, BrickletTemperatureIRV2.FUNCTION_GET_AMBIENT_TEMPERATURE, (), '', 'h')

    def set_ambient_temperature_callback_configuration(self, period, value_has_to_change, option, min, max):
        """
        The period in ms is the period with which the :cb:`Ambient Temperature` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Ambient Temperature` callback.

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

        self.ipcon.send_request(self, BrickletTemperatureIRV2.FUNCTION_SET_AMBIENT_TEMPERATURE_CALLBACK_CONFIGURATION, (period, value_has_to_change, option, min, max), 'I ! c h h', '')

    def get_ambient_temperature_callback_configuration(self):
        """
        Returns the callback configuration as set by :func:`Set Ambient Temperature Callback Configuration`.
        """
        return GetAmbientTemperatureCallbackConfiguration(*self.ipcon.send_request(self, BrickletTemperatureIRV2.FUNCTION_GET_AMBIENT_TEMPERATURE_CALLBACK_CONFIGURATION, (), '', 'I ! c h h'))

    def get_object_temperature(self):
        """
        Returns the object temperature of the sensor, i.e. the temperature
        of the surface of the object the sensor is aimed at. The value
        has a range of -700 to 3800 and is given in °C/10,
        e.g. a value of 3001 means that a temperature of 300.1 °C is measured
        on the surface of the object.

        The temperature of different materials is dependent on their `emissivity
        <https://en.wikipedia.org/wiki/Emissivity>`__. The emissivity of the material
        can be set with :func:`Set Emissivity`.

        If you want to get the object temperature periodically, it is recommended
        to use the :cb:`Object Temperature` callback and set the period with
        :func:`Set Object Temperature Callback Configuration`.


        If you want to get the value periodically, it is recommended to use the
        :cb:`Object Temperature` callback. You can set the callback configuration
        with :func:`Set Object Temperature Callback Configuration`.
        """
        return self.ipcon.send_request(self, BrickletTemperatureIRV2.FUNCTION_GET_OBJECT_TEMPERATURE, (), '', 'h')

    def set_object_temperature_callback_configuration(self, period, value_has_to_change, option, min, max):
        """
        The period in ms is the period with which the :cb:`Object Temperature` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Object Temperature` callback.

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

        self.ipcon.send_request(self, BrickletTemperatureIRV2.FUNCTION_SET_OBJECT_TEMPERATURE_CALLBACK_CONFIGURATION, (period, value_has_to_change, option, min, max), 'I ! c h h', '')

    def get_object_temperature_callback_configuration(self):
        """
        Returns the callback configuration as set by :func:`Set Object Temperature Callback Configuration`.
        """
        return GetObjectTemperatureCallbackConfiguration(*self.ipcon.send_request(self, BrickletTemperatureIRV2.FUNCTION_GET_OBJECT_TEMPERATURE_CALLBACK_CONFIGURATION, (), '', 'I ! c h h'))

    def set_emissivity(self, emissivity):
        """
        Sets the `emissivity <https://en.wikipedia.org/wiki/Emissivity>`__ that is
        used to calculate the surface temperature as returned by
        :func:`Get Object Temperature`.

        The emissivity is usually given as a value between 0.0 and 1.0. A list of
        emissivities of different materials can be found
        `here <http://www.infrared-thermography.com/material.htm>`__.

        The parameter of :func:`Set Emissivity` has to be given with a factor of
        65535 (16-bit). For example: An emissivity of 0.1 can be set with the
        value 6553, an emissivity of 0.5 with the value 32767 and so on.

        .. note::
         If you need a precise measurement for the object temperature, it is
         absolutely crucial that you also provide a precise emissivity.

        The default emissivity is 1.0 (value of 65535) and the minimum emissivity the
        sensor can handle is 0.1 (value of 6553).
        """
        emissivity = int(emissivity)

        self.ipcon.send_request(self, BrickletTemperatureIRV2.FUNCTION_SET_EMISSIVITY, (emissivity,), 'H', '')

    def get_emissivity(self):
        """
        Returns the emissivity as set by :func:`Set Emissivity`.
        """
        return self.ipcon.send_request(self, BrickletTemperatureIRV2.FUNCTION_GET_EMISSIVITY, (), '', 'H')

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
        return GetSPITFPErrorCount(*self.ipcon.send_request(self, BrickletTemperatureIRV2.FUNCTION_GET_SPITFP_ERROR_COUNT, (), '', 'I I I I'))

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

        return self.ipcon.send_request(self, BrickletTemperatureIRV2.FUNCTION_SET_BOOTLOADER_MODE, (mode,), 'B', 'B')

    def get_bootloader_mode(self):
        """
        Returns the current bootloader mode, see :func:`Set Bootloader Mode`.
        """
        return self.ipcon.send_request(self, BrickletTemperatureIRV2.FUNCTION_GET_BOOTLOADER_MODE, (), '', 'B')

    def set_write_firmware_pointer(self, pointer):
        """
        Sets the firmware pointer for :func:`Write Firmware`. The pointer has
        to be increased by chunks of size 64. The data is written to flash
        every 4 chunks (which equals to one page of size 256).

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        pointer = int(pointer)

        self.ipcon.send_request(self, BrickletTemperatureIRV2.FUNCTION_SET_WRITE_FIRMWARE_POINTER, (pointer,), 'I', '')

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

        return self.ipcon.send_request(self, BrickletTemperatureIRV2.FUNCTION_WRITE_FIRMWARE, (data,), '64B', 'B')

    def set_status_led_config(self, config):
        """
        Sets the status LED configuration. By default the LED shows
        communication traffic between Brick and Bricklet, it flickers once
        for every 10 received data packets.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is will show heartbeat by default.
        """
        config = int(config)

        self.ipcon.send_request(self, BrickletTemperatureIRV2.FUNCTION_SET_STATUS_LED_CONFIG, (config,), 'B', '')

    def get_status_led_config(self):
        """
        Returns the configuration as set by :func:`Set Status LED Config`
        """
        return self.ipcon.send_request(self, BrickletTemperatureIRV2.FUNCTION_GET_STATUS_LED_CONFIG, (), '', 'B')

    def get_chip_temperature(self):
        """
        Returns the temperature in °C as measured inside the microcontroller. The
        value returned is not the ambient temperature!

        The temperature is only proportional to the real temperature and it has bad
        accuracy. Practically it is only useful as an indicator for
        temperature changes.
        """
        return self.ipcon.send_request(self, BrickletTemperatureIRV2.FUNCTION_GET_CHIP_TEMPERATURE, (), '', 'h')

    def reset(self):
        """
        Calling this function will reset the Bricklet. All configurations
        will be lost.

        After a reset you have to create new device objects,
        calling functions on the existing ones will result in
        undefined behavior!
        """
        self.ipcon.send_request(self, BrickletTemperatureIRV2.FUNCTION_RESET, (), '', '')

    def write_uid(self, uid):
        """
        Writes a new UID into flash. If you want to set a new UID
        you have to decode the Base58 encoded UID string into an
        integer first.

        We recommend that you use Brick Viewer to change the UID.
        """
        uid = int(uid)

        self.ipcon.send_request(self, BrickletTemperatureIRV2.FUNCTION_WRITE_UID, (uid,), 'I', '')

    def read_uid(self):
        """
        Returns the current UID as an integer. Encode as
        Base58 to get the usual string version.
        """
        return self.ipcon.send_request(self, BrickletTemperatureIRV2.FUNCTION_READ_UID, (), '', 'I')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be 'a', 'b', 'c' or 'd'.

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletTemperatureIRV2.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, callback_id, function):
        """
        Registers the given *function* with the given *callback_id*.
        """
        if function is None:
            self.registered_callbacks.pop(callback_id, None)
        else:
            self.registered_callbacks[callback_id] = function

TemperatureIRV2 = BrickletTemperatureIRV2 # for backward compatibility
