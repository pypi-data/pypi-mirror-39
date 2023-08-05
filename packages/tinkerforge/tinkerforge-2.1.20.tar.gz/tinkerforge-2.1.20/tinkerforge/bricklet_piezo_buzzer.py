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

GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletPiezoBuzzer(Device):
    """
    Creates 1kHz beep
    """

    DEVICE_IDENTIFIER = 214
    DEVICE_DISPLAY_NAME = 'Piezo Buzzer Bricklet'
    DEVICE_URL_PART = 'piezo_buzzer' # internal

    CALLBACK_BEEP_FINISHED = 3
    CALLBACK_MORSE_CODE_FINISHED = 4


    FUNCTION_BEEP = 1
    FUNCTION_MORSE_CODE = 2
    FUNCTION_GET_IDENTITY = 255


    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

        self.response_expected[BrickletPiezoBuzzer.FUNCTION_BEEP] = BrickletPiezoBuzzer.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletPiezoBuzzer.FUNCTION_MORSE_CODE] = BrickletPiezoBuzzer.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletPiezoBuzzer.FUNCTION_GET_IDENTITY] = BrickletPiezoBuzzer.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletPiezoBuzzer.CALLBACK_BEEP_FINISHED] = ''
        self.callback_formats[BrickletPiezoBuzzer.CALLBACK_MORSE_CODE_FINISHED] = ''


    def beep(self, duration):
        """
        Beeps with the duration in ms. For example: If you set a value of 1000,
        the piezo buzzer will beep for one second.
        """
        duration = int(duration)

        self.ipcon.send_request(self, BrickletPiezoBuzzer.FUNCTION_BEEP, (duration,), 'I', '')

    def morse_code(self, morse):
        """
        Sets morse code that will be played by the piezo buzzer. The morse code
        is given as a string consisting of "." (dot), "-" (minus) and " " (space)
        for *dits*, *dahs* and *pauses*. Every other character is ignored.

        For example: If you set the string "...---...", the piezo buzzer will beep
        nine times with the durations "short short short long long long short
        short short".

        The maximum string size is 60.
        """
        morse = create_string(morse)

        self.ipcon.send_request(self, BrickletPiezoBuzzer.FUNCTION_MORSE_CODE, (morse,), '60s', '')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be 'a', 'b', 'c' or 'd'.

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletPiezoBuzzer.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, callback_id, function):
        """
        Registers the given *function* with the given *callback_id*.
        """
        if function is None:
            self.registered_callbacks.pop(callback_id, None)
        else:
            self.registered_callbacks[callback_id] = function

PiezoBuzzer = BrickletPiezoBuzzer # for backward compatibility
