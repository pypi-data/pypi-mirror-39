import ctypes


class AbstractStructure():

    def send(self):
        return bytes(self)[:]

    def receive(self, buffer):
        """
        this also works to import bytes into the Structure
        #Structure.from_buffer_copy(data)
        """
        fit = min(len(buffer), ctypes.sizeof(self))
        ctypes.memmove(ctypes.addressof(self), buffer, fit)

    def __repr__(self):
        '''Print the fields'''
        res = []
        for field in self._fields_:
            res.append('%s=%s \n' % (field[0], repr(getattr(self, field[0]))))
        return self.__class__.__name__ + '(' + ','.join(res) + ')'

    def enumerate(self):
        data = bytes(self)
        for i in range(len(data)):
            yield (i, data[i].to_bytes(1, 'big'))


class Short(AbstractStructure, ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('value', ctypes.c_ushort),
    ]


class Float(AbstractStructure, ctypes.Structure):
    _pack_ = 1
    _fields_ = [
           ('value', ctypes.c_float),
    ]


class DeviceFields(AbstractStructure, ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('powerOnOff', ctypes.c_uint8),             # // byte 0
        ('alarmOnOff', ctypes.c_uint8),
        ('speakerOnOff', ctypes.c_uint8),
        ('graphicModeOnOff', ctypes.c_uint8),
        ('backlightTimeoutSeconds', ctypes.c_uint8),# // byte 4
        ('idleTitleDisplayMode', ctypes.c_uint8),
        ('alarmCPMValueHiByte', ctypes.c_uint8),
        ('alarmCPMValueLoByte', ctypes.c_uint8),
        ('calibrationCPM_0', Short),
        ('calibrationSvUc_0', Float),
        ('calibrationCPM_1', Short),
        ('calibrationSvUc_1', Float),
        ('calibrationCPM_2', Short),
        ('calibrationSvUc_2', Float),
        ('idleDisplayMode', ctypes.c_uint8),
        ('alarmValueuSvUc', Float),
        ('alarmType', ctypes.c_uint8),
       # saveDataType specifies both the interval of data logging where
       # 0 = data logging is off, 1 = once per second, 2 = once per minute,
       # 3 = once per hour and the type of data saved where 0 = don't care,
       # 1 = counts/second, 2 = counts/minute, 3 = CPM averaged over hour.
       # Whenever this is changed, the GQ GMC inserts a date/timestamp
       # into the history data buffer.
        ('saveDataType', ctypes.c_uint8),               # // byte 32
        ('swivelDisplay', ctypes.c_uint8),
        ('zoom', Float),
        # dataSaveAddress represents the address of the first sample following
        # the insertion of a date/timestamp or label tag into the data buffer.
        # Periodically, a label or date/timestamp will be put into the buffer
        # without a change made to dataSaveAddress. So you always have to be
        # on the lookout for 55AA sequence when parsing data buffer. But you
        # have to do that anyway because you might encounter double byte data.
        ('dataSaveAddress2', ctypes.c_uint8),
        ('dataSaveAddress1', ctypes.c_uint8),
        ('dataSaveAddress0', ctypes.c_uint8),               #  // byte 40
       # dataReadAddress semantics is unknown. As far as I have seen,
       # its value is always zero.
        ('dataReadAddress2', ctypes.c_uint8),
        ('dataReadAddress1', ctypes.c_uint8),
        ('dataReadAddress0', ctypes.c_uint8),
        ('nPowerSavingMode', ctypes.c_uint8),      # // byte 44
        ('nSensitivityMode', ctypes.c_uint8),
        ('nCounterDelayHiByte', ctypes.c_uint8),
        ('nCounterDelayLoByte', ctypes.c_uint8),
        ('nVoltageOffset', ctypes.c_uint8),        # // byte 48
        ('maxCPMHiByte', ctypes.c_uint8),
        ('maxCPMLoByte', ctypes.c_uint8),
        ('nSensitivityAutoModeThreshold', ctypes.c_uint8),
       # saveDateTimeStamp is the date/timestamp of the logging run,
       # all data following up to the next date/timestamp are marked
       # in time by this date/timestamp, where
        ('saveDateTimeStampByte5', ctypes.c_uint8), # // = year (last two digits) // byte 52
        ('saveDateTimeStampByte4', ctypes.c_uint8), # // = month
        ('saveDateTimeStampByte3', ctypes.c_uint8), # // = day
        ('saveDateTimeStampByte2', ctypes.c_uint8), # // = hour
        ('saveDateTimeStampByte1', ctypes.c_uint8), # // = minute // byte 56
        ('saveDateTimeStampByte0', ctypes.c_uint8), # // = second
       # // maxBytes is always 0xff
        ('maxBytes', ctypes.c_uint8),

   ]

#if __name__ == '__main__':
#    filename = '/tmp/tmpdx43b6eb.bin'
#    with open(filename, mode='rb') as file:
#        data = file.read()
#        
#
#        fields = DeviceFields.from_buffer_copy(data)
#
#        print(fields.calibrationCPM_0, bytes(fields.calibrationCPM_0))
#        print(fields.calibrationSvUc_0, bytes(fields.calibrationSvUc_0))
#        pdb.set_trace()
