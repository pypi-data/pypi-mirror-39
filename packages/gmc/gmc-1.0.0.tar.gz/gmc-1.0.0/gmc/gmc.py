import time
import struct
from datetime import datetime, date
import serial
import logging
from multiprocessing import Process, Queue, Value
from .config import Config
from .device import DeviceFields
from .util import save_bin_file, wait_until


class GMC:
    """GMC serial message wrapper class
    extends the pyserial port interface with __getattr__
    """

    def __init__(self, config_update=None):
        self.logger = logging.getLogger(__name__)
        self.logger.info('new {} instance.'.format(__name__))
        self.port = None
        self.config = Config()
        self.config.update(config_update)
        self.device_fields = None
        self._autobaud()
        self.get_device_config()

    def __repr__(self):
        return str(self.get_settings())

    def _autobaud(self):
        """ attempt to find the baudrate of the device
        place the DEFAULT_BAUDRATE first and then try others
        """
        bauds = self.config.baudrates
        bauds.remove(self.config.DEFAULT_BAUDRATE)
        bauds.insert(0, self.config.DEFAULT_BAUDRATE)
        for baudrate in self.config.baudrates:
            self.config.DEFAULT_BAUDRATE = baudrate
            if not self.version():
                self.logger.info('connect failed with baud: {}'.format(baudrate))
                self.close_device()
            else:
                self.logger.info('connect with baud:{}'.format(baudrate))
                break

    def __getattr__(self, attr):
        """
        assumes all the methods of pyserial.port
        instead of self.port.read() you can call self.read()
        """
        if not self.port or not self.port.is_open:
            self._open_device()
        if hasattr(self.port, attr):
            def wrapper(*args, **kw):
                self.logger.info('getattr calling port.{}'.format(attr))
                return getattr(self.port, attr)(*args, **kw)
            return wrapper
        raise AttributeError(attr)

    def _open_device(self):
        """automatically called when the serial port is referenced
        """
        self.logger.info('_open_device on port'.format(self.config.DEFAULT_PORT))
        try:
            self.port = serial.Serial(self.config.DEFAULT_PORT,
                                      baudrate=self.config.DEFAULT_BAUDRATE,
                                      timeout=1.0)
            self.clear_port()
        except serial.serialutil.SerialException as e:
            self._handle_serial_error(e)
        except serial.serialutil.SerialTimeoutException as e:
            self._handle_serial_error(e)
        except Exception as e:
            self._handle_serial_error(e)

    def close_device(self):
        """close the serial device
        """
        if self.port:
            self.close()
            self.port = None

    def _handle_serial_error(self, error=None):
        self.logger.exception(error)
        self.close_device()
        raise error

    def clear_port(self):
        """a method to clean the read and write port buffer of data
        """
        self.reset_input_buffer()
        self.reset_output_buffer()

    def get_device_config(self):
        """there are two types of config local and device
        find the configuration of the device using the device version
        load the device config
        """
        self.config.set_device(self.version())
        self.config_load()

    def write_data(self, data, size=None):
        """helper for the serial port write
        the size parm will determine if the read will have the data ready.
        prepare the port for write message.
        encode the message if string.
        send the message and then wait.
        """
        self.logger.info('write_data: size={} data={}'.format(size, data))
        self.clear_port()
        if type(data) is str:
            data = data.encode('utf-8')
        self.write(data)
        time.sleep(self.config.DEFAULT_WRITE_TIMEOUT)
        if size:
            # wait until port has data to read
            wait_until(self._bytes_ready, size=size, timeout=self.config.DEFAULT_READ_TIMEOUT)

    def _bytes_ready(self, size=None):
        return self.port.in_waiting == size

    def command_ok(self):
        """certain device commands are to return 0xaa
        """
        result = self.read(1)
        if result == b'' or ord(result) != 0xaa:
            return False
        return True

    def send_key(self, key):
        """send key to device
        return None
        """
        key = key.lower()
        keys = ['s1', 's2', 's3', 's4']
        if key not in keys:
            raise ValueError('Invalid key. Expected one of: %s' % keys)
        if key == 's1':
            self.write_data('<KEY0>>')
        elif key == 's2':
            self.write_data('<KEY1>>')
        elif key == 's3':
            self.write_data('<KEY2>>')
        elif key == 's4':
            self.write_data('<KEY3>>')

    def power_off(self):
        self.write_data('<POWEROFF>>')

    def power_on(self):
        self.write_data('<POWERON>>')

    def reboot(self):
        self.write_data('<REBOOT>>')
        self.close_device()

    def factory_reset(self):
        self.write_data('<FACTORYRESET>>', 1)
        if not self.command_ok():
            logging.warning('factory reset failed.')
            return False
        return True

    def config_reset(self):
        """reset device configuration to factory defaults
        """
        self.write_data('<ECFG>>', 1)
        if not self.command_ok():
            logging.warning('config reset failed.')
            return False
        return True

    def config_update(self):
        """after writing config to device
        you will need to call the device update command.
        """
        self.write_data('<CFGUPDATE>>', 1)
        if not self.command_ok():
            logging.warning('config update failed.')
            return False
        return True

    def config_load(self):
        """get the device config and load into device_fields
        """
        self.write_data('<GETCFG>>', self.config.device.configsize)
        data = self.read(self.config.device.configsize)
        #print('config:', self.save_bin_file(data))
        self.device_fields = DeviceFields()
        self.device_fields.receive(data)

    def config_write(self):
        """ write config to device

        writes to device one byte at a time

        make changes to confiuration by updating
        the device_fields ctypes.Structure that
        contains the latest settings.

        see device.py DeviceFields for fields to modify

        example:
        gmc = GMC()
        gmc.device_fields.speakerOnOff = 1
        gmc.config_write()

        address packing for WCFG is different for devices device.wcfg_address
        accounts for the variation

        """
        if not self.device_fields:
            logging.warning('load device config with config_load')
            return

        if not self.config_reset():
            raise Exception("config_write failed to reset device configuation")

        # feed of raw bytes from config ctypes.Structure.
        for i in self.device_fields.enumerate():
            A0 = struct.pack(">" + self.config.device.wcfg_address, i[0])
            D0 = i[1]
            self.write_data(b'<WCFG' + A0 + D0 + b'>>', 1)
            if not self.command_ok():
                raise Exception("config_write failed: {}, {}" .format(i[0], i[1]))

        if not self.config_update():
            raise Exception("config_write failed to update device configuation")

        self.config_load()

    def get_date_time(self):
        self.write_data('<GETDATETIME>>', 7)
        date = self.read(7)
        (year, month, day, hour, minute, second, dummy) = struct.unpack(">BBBBBBB", date)
        return datetime(year+2000, month, day, hour, minute, second)

    def set_date_time(self, date_time):
        if not isinstance(date_time, datetime):
            raise TypeError('date_time must be datetime.date.')
        cmd = struct.pack('>BBBBBB',
                          date_time.year - 2000,
                          date_time.month,
                          date_time.day,
                          date_time.hour,
                          date_time.minute,
                          date_time.second)
        self.write_data(b'<SETDATETIME' + cmd + b'>>', 1)
        return self.command_ok()

    def version(self):
        self.write_data('<GETVER>>', 14)
        return self.read(14).decode('utf-8')

    def serial(self):
        self.write_data('<GETSERIAL>>', 7)
        serial_number = self.read(7)
        return serial_number.hex()

    def voltage(self):
        self.write_data('<GETVOLT>>', 1)
        v = ord(self.read(1))
        return '%s V' % (float(v) / 10.0)

    def temp(self):
        self.write_data('<GETTEMP>>', 4)
        temp = self.read(4)
        sign = ''
        if temp[2] != 0:
            sign = '-'
        temp_str = "{}{}.{} {}{}".format(sign, temp[0], temp[1], chr(0x00B0), chr(0x0043))
        return(temp_str)

    def gyro(self):
        """
        Return: Seven bytes gyroscope data in hexdecimal: BYTE1,BYTE2,BYTE3,BYTE4,BYTE5,BYTE6,BYTE7
        Here: BYTE1,BYTE2 are the X position data in 16 bits value. The first byte is MSB byte data and second byte is LSB byte data.
        BYTE3,BYTE4 are the Y position data in 16 bits value. The first byte is MSB byte data and second byte is LSB byte data.
        BYTE5,BYTE6 are the Z position data in 16 bits value. The first byte is MSB byte data and second byte is LSB byte data.
        BYTE7 always 0xAA
        """
        self.write_data('<GETGYRO>>', 7)
        result = self.read(7)
        (x, y, z, dummy) = struct.unpack(">hhhB", result)
        return x, y, z

    def cpm(self, cpm_to_usievert=None):
        self.write_data('<GETCPM>>', 2)
        cpm = self.read(2)
        value = struct.unpack(">H", cpm)[0]
        unit_value = (value, 'CPM')
        if cpm_to_usievert != None:
            return self.cpmToUSievert(value, 'CPM', cpm_to_usievert)
        if unit_value[1] == 'uSv/h':
            return('%.4f %s' % unit_value)
        else:
            return('%d %s' % unit_value)

    def cpmToUSievert(cpm, unit, cpm_to_usievert):
        if cpm_to_usievert == None:
            return (cpm, unit)
        if unit == 'CPS':
            return (cpm * cpm_to_usievert[1] / cpm_to_usievert[0] * 60, 'uSv/h')
        elif unit == 'CPM':
            return (cpm * cpm_to_usievert[1] / cpm_to_usievert[0], 'uSv/h')
        elif unit == 'CPH':
            return (cpm * cpm_to_usievert[1] / cpm_to_usievert[0] / 60, 'uSv/h')
        else:
            return (cpm, unit)

    def history(self, address = 0, datalength = None):
        """return raw binary history data
        """
        if not datalength:
            datalength = self.config.device.SPIRpage

        # address: pack into 4 bytes, big endian; then clip 1st byte = high byte!
        ad = struct.pack(">I", address)[1:]

        # datalength: pack into 2 bytes, big endian; use all bytes
        # but adjust datalength to fix bug!
        if self.config.device.SPIRbugfix:
            dl = struct.pack(">H", datalength - 1)
        else:
            dl = struct.pack(">H", datalength)

        ad = bytearray(ad)
        dl = bytearray(dl)

        self.logger.info("history: SPIR requested: address: {}, datalength:{} \
                         (hex: address: {}, datalength:{})"
                         .format(address, datalength, ad, dl)
        )

        self.write_data(b'<SPIR' + ad + dl + b'>>', datalength)
        data = self.read(datalength)
        return data

    def history_all(self):
        """return all the history data
        """
        FFpages = 0
        hist = b''
        page = self.config.device.SPIRpage
        for address in range(0, self.config.device.memory, page):
            self.logger.info("Reading page of size:{} @address:{}".format(page, address))
            data = self.history(address, page)
            hist += data
            if data.count(b'\xFF') == page:
                FFpages += 1

            if FFpages * page >= page * 2:
                self.logger.warning("Found {} successive {} B-pages (total {} B), as 'FF' only - ending reading".format(FFpages, page, FFpages * page))
                break

        return save_bin_file(hist, prefix='gmc-',  suffix='.bin')

    def heartbeatOn(self):
        """activate heartbeat and start process
        to capture the results into a queue.
        """
        self.write_data('<HEARTBEAT1>>')
        self.heart_flag = Value('i', 1) # multiprocessing.Value
        self.heartQueue = Queue() # multiprocessing.Queue
        self.heartProcess = Process(
            target=self._heartbeat,
            args=(self.heart_flag, self.heartQueue,))
        self.heartProcess.start()

    def heart(self):
        """function generator to get heartbeats
        example: for beat in gmc.hear(): print(beat)
        """
        try:
            if self.heartProcess and not self.heartProcess.is_alive():
                self.logger.warning('heartbeat is off.')

            if not self.heartQueue or self.heartQueue.empty():
                self.logger.warning('heartbeat queue not ready.')
                return

            for beat in iter(self.heartq, None):
                yield beat
        except Exception as e:
            self.logger.error(e)

    def heartq(self):
        """read the queue without blocking
        """
        return self.heartQueue.get(False, timeout=1)

    def _heartbeat(self, flag, queue):
        """worker process to capture heartbeats
        """
        while True:
            if flag.value == 0:
                self.logger.info('_heartbeat stop')
                return
            try:
                cpm = self.read(2)
                time.sleep(2)
                if cpm == '':
                    continue
                mark = datetime.now().replace(microsecond=0)
                value = struct.unpack(">H", cpm)[0] & 0x3fff
                queue.put((mark, value, cpm))
            except Exception as e:
                self.logger.error(e)
                return

    def heartbeatOff(self):
        """deactivate heartbeat and kill process
        can still read from heart
        """
        self.logger.info('heartbeatOff')
        self.write_data('<HEARTBEAT0>>')
        if self.heartProcess:
            self.heart_flag.value = not self.heart_flag.value
            time.sleep(2)
            self.heartProcess.terminate()
            time.sleep(2)
            if not self.heartProcess.is_alive():
                self.heartProcess.join(timeout=2)
