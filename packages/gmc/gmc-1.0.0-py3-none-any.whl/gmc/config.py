#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import platform


def port():
    if platform.system() == 'Windows':
        return 'COM3'
    else:
         return '/dev/ttyUSB0'

class Config:
    DEFAULT_WRITE_TIMEOUT = 0.3
    DEFAULT_READ_TIMEOUT = 3
    DEFAULT_PORT = port()
    DEFAULT_BAUDRATE = 115200
    baudrates = [115200, 57600, 38400, 28800, 19200, 14400, 9600, 4800, 2400, 1200]

    def update(self, config_update):
        """update properties of config
        from a dictionary of values
        """
        if type(config_update) is not dict:
            return
        for key, value in config_update.items():
            setattr(self, key, value)

    def set_device(self, version):
        """
        find the device configuration from the version
        """
        model, number = version.split()
        self.model_name = model[:7]
        self.model_type = model[7:]
        self.number_major = number[:1]
        self.number_minor = number[2:]

        device = '{}_{}_{}'.format(
            self.model_name.replace('-', '_'),
            self.model_type.replace('+', 'plus'),
            self.number_major
        )
        if hasattr(sys.modules[__name__], device):
            self.device = getattr(sys.modules[__name__], device)
        else:
            self.device = getattr(sys.modules[__name__], device+number_minor)

"""
GETVER            Model               Firmware  nominal (observed)
GMC-300Re 3.xx,   GMC-300             Firmware: 3.xx    (3.20)
                  GMC-300E            existing?
GMC-300Re 4.xx,   GMC-300E+           Firmware: 4.xx    (4.20, 4.22)
                  GMC-320             existing?
GMC-320Re 4.xx,   GMC-320+            Firmware: 4.xx    (4.19)
GMC-320Re 5.xx,   GMC-320+V5 (WiFi)   Firmware: 5.xx
GMC-500Re 1.xx,   GMC-500 and 500+    Firmware: 1.xx    (1.00, 1.08)
GMC-500+Re 1.xx,  GMC-500+            Firmware: 1.??    (1.18(bug), 1.21)
GMC-600Re 1.xx,   GMC-600 and 600+    Firmware: 1.xx

see: http://www.gqelectronicsllc.com/forum/topic.asp?TOPIC_ID=4948 Reply #30
Quote EmfDev:
"On the 500 and 600 series, the GETVER return can be any length.
So far its only 14 bytes or 15 bytes. But it should return any given
model name completely so the length is variable.
And the '+' sign is included in the model name. e.g. GMC500+Re 1.10
But I don't think the 300 or 320 has been updated so maybe you can ask
support for the fix."

discovered for the 300 series:
    baudrate = 1200         # config setting:  64
    baudrate = 2400         # config setting: 160
    baudrate = 4800         # config setting: 208
    baudrate = 9600         # config setting: 232
    baudrate = 14400        # config setting: 240
    baudrate = 19200        # config setting: 244
    baudrate = 28800        # config setting: 248
    baudrate = 38400        # config setting: 250
    baudrate = 57600        # config setting: 252
    baudrate = 115200       # config setting: 254
    #baudrate = 921600      # config setting: not available

for the GMC-500 and 600 series
by EmfDev from GQ from here:
http://www.gqelectronicsllc.com/forum/topic.asp?TOPIC_ID=4948 Reply #14
- The baudrate config is now
    baudrate = 115200       # config setting: 0
    baudrate = 1200         # config setting: 1
    baudrate = 2400         # config setting: 2
    baudrate = 4800         # config setting: 3
    baudrate = 9600         # config setting: 4
    baudrate = 14400        # config setting: 5
    baudrate = 19200        # config setting: 6
    baudrate = 28800        # config setting: 7
    baudrate = 38400        # config setting: 8
    baudrate = 57600        # config setting: 9
"""


class GMC_Device(object):
    name = "default"
    memory               = 2**20
    SPIRpage             = 2048
    SPIRbugfix           = False
    configsize           = 512
    calibration          = 0.0065
    calibration2nd       = 0.194
    voltagebytes         = 5
    endianness           = 'big'
    GMCvariables         = "CPM, CPS"
    nbytes               = 2
    # wcfg_addres is a param of struct.pack
    # B gives one byte address H gives two.
    wcfg_address         = 'B'


class GMC_300_Re_3(GMC_Device):
    name = "GMC-300Re 3."
    #######################################################################
    # the "GMC-300" delivers the requested page after ANDing with 0fff
    # hence when you request 4k (=1000hex) you get zero
    # therefore use pagesize 2k only
    #######################################################################
    memory               = 2**16
    configsize           = 256
    voltagebytes         = 1
    endianness           = 'little'


class GMC_300_Re_4(GMC_Device):
    name = "GMC-300Re 4."
    #######################################################################
    # when using a page of 4k, you need the datalength workaround in
    # gcommand, i.e. asking for 1 byte less
    #######################################################################
    memory               = 2**16
    SPIRpage             = 4096
    SPIRbugfix           = True
    configsize           = 256
    voltagebytes         = 1
    endianness           = 'little'


class GMC_320_Re_4(GMC_Device):
    name = "GMC-320Re 4."
    #######################################################################
    #
    #######################################################################
    SPIRpage             = 4096
    SPIRbugfix           = True
    configsize           = 256
    voltagebytes         = 1
    endianness           = 'little'


class GMC_320_Re_5(GMC_Device):
    name = "GMC-320Re 5."
    #######################################################################
    #
    #######################################################################
    SPIRpage             = 4096
    SPIRbugfix           = True
    configsize           = 256
    voltagebytes         = 1
    endianness           = 'little'


class GMC_500_Re_1(GMC_Device):
    name = "GMC-500Re 1."
    #######################################################################
    #
    #######################################################################
    #SPIRpage            = 4096  # ist bug jetzt behoben oder auf altem Stand???
    SPIRpage             = 2048   # Workaround erstmal auf 2048 bytes
    wcfg_address         = 'H'


class GMC_500_plusRe_118(GMC_Device):
    name = "GMC-500+Re 1.18"
    #######################################################################
    # Yields 4 bytes on all CPx calls!
    # Has a firmware bug: on first call to GETVER gets nothing returned.
    # WORK AROUND: must cycle connection ON->OFF->ON. then ok
    #######################################################################
    # calib based on: http://www.gqelectronicsllc.com/forum/topic.asp?TOPIC_ID=5120 Reply #3
    # calib 2nd tube: 0.194, see Reply #21 in:
    # http://www.gqelectronicsllc.com/forum/topic.asp?TOPIC_ID=5148
    # "The GMC-500+ low sensitivity tube conversion rate is 0.194 uSv/h per
    # CPM. It is about 30 times less than M4011."
    calibration2nd       = 0.194
    GMCvariables         = "CPM, CPS, CPM1st, CPM2nd, CPS1st, CPS2nd"
    nbytes               = 4
    wcfg_address         = 'H'


class GMC_500_plusRe_121(GMC_Device):
    name = "GMC-500+Re 1.21"
    #######################################################################
    # Yields 4 bytes oj all CPx calls!
    # Firmware bug from 'GMC-500+Re 1.18' is corrected
    #######################################################################
    SPIRpage            = 4096  # ist bug jetzt behoben oder auf altem Stand???
    # calib based on: http://www.gqelectronicsllc.com/forum/topic.asp?TOPIC_ID=5120 Reply #3
    # calib 2nd tube: 0.194, see Reply #21 in:
    # http://www.gqelectronicsllc.com/forum/topic.asp?TOPIC_ID=5148
    # "The GMC-500+ low sensitivity tube conversion rate is 0.194 uSv/h per
    # CPM. It is about 30 times less than M4011."
    GMCvariables         = "CPM, CPS, CPM1st, CPM2nd, CPS1st, CPS2nd"
    nbytes               = 4
    wcfg_address         = 'H'


class GMC_500_plusRe_1(GMC_Device):
    name = "GMC-500+Re 1."
    #######################################################################
    #
    #######################################################################
    # calib based on: http://www.gqelectronicsllc.com/forum/topic.asp?TOPIC_ID=5120 Reply #3
    # calib 2nd tube: 0.194, see Reply #21 in:
    # http://www.gqelectronicsllc.com/forum/topic.asp?TOPIC_ID=5148
    # "The GMC-500+ low sensitivity tube conversion rate is 0.194 uSv/h per
    # CPM. It is about 30 times less than M4011."
    GMCvariables         = "CPM, CPS, CPM1st, CPM2nd"
    nbytes               = 2
    wcfg_address         = 'H'



class GMC_600_Re_1(GMC_Device):
    name = "GMC-600Re 1."
    #######################################################################
    #
    #######################################################################
    wcfg_address         = 'H'


class GMC_600_plus_Re_1(GMC_Device):
    name = "GMC-600+Re 1."
    #######################################################################
    #
    # Amazon:   https://www.amazon.de/gmc-600-Plus-Geiger-Counter-Detektor-Dosimeter/dp/B077V7QSHP
    #           Hohe Empfindlichkeit Pancake Geiger Röhre LND 7317 installiert
    # LND 7317: https://shop.kithub.cc/products/pancake-geiger-mueller-tube-lnd-7317
    #           Gamma sensitivity Co60 (cps/mr/hr) 58
    # SBM20 :   http://www.gstube.com/data/2398/
    #           Gamma Sensitivity Ra226 (cps/mR/hr) : 29
    #           Gamma Sensitivity Co60 (cps/mR/hr) : 22
    #######################################################################
    # re calib: see user Kaban here: http://www.gqelectronicsllc.com/forum/topic.asp?TOPIC_ID=4948
    calibration          = 0.002637
    wcfg_address         = 'H'
