import pdb
import time
import datetime
import struct
import logging
from .. import GMC, gmc_connection
import pytest

# pytest -xs --pdb -log_cli=true

"""
caplog global setting

"""

config = {'DEFAULT_BAUDRATE': 57600}

@gmc_connection(config)
def test_init():
    pass


def test_device(caplog):
    caplog.set_level(logging.INFO, logger='gmc.gmc')
    version = gmc.version()
    device = gmc.config.device
    assert device


def test_settings( caplog):
    caplog.set_level(logging.INFO, logger='gmc.gmc')
    print(gmc.config.device)
    print(gmc.get_settings())
    print(gmc.device_fields)


def test_gyro(caplog):
    caplog.set_level(logging.INFO, logger='gmc.gmc')
    position = gmc.gyro()
    assert len(position) == 3


def test_temp(caplog):
    caplog.set_level(logging.INFO, logger='gmc.gmc')
    temp = gmc.temp()
    assert temp


def test_settings(caplog):
    caplog.set_level(logging.INFO, logger='gmc.gmc')
    cpm = gmc.cpm()
    assert cpm >= 0


def test_config_fields(caplog):
    """ test changing config values
    """
    caplog.set_level(logging.INFO, logger='gmc.gmc')

    gmc.device_fields.speakerOnOff = 0
    assert gmc.device_fields.speakerOnOff == 0

    gmc.device_fields.calibrationCPM_0.value = 65
    assert gmc.device_fields.calibrationCPM_0.value == 65


def test_date():
    new_time = datetime.datetime.now().replace(microsecond=0)
    gmc.set_date_time(new_time)
    after = gmc.get_date_time()
    print(new_time, after)
    assert new_time == after


def test_reboot(caplog):
    caplog.set_level(logging.INFO, logger='gmc.gmc')
    version = gmc.version()
    gmc.reboot()
    assert gmc.version() == version


def test_power(caplog):
    caplog.set_level(logging.INFO, logger='gmc.gmc')
    gmc.power_off()
    time.sleep(2)
    gmc.config_load()
    assert gmc.device_fields.powerOnOff == 255

    gmc.power_on()
    time.sleep(2)
    gmc.config_load()
    assert gmc.device_fields.powerOnOff == 0


def test_heart(caplog):
    caplog.set_level(logging.INFO, logger='gmc.gmc')
    timeout = 10
    gmc.heartbeatOn()

    print('sleep')
    time.sleep(5)

    print('watch queue')
    start = time.time()
    for i in gmc.heart():
        print(i)
        if time.time() - start > timeout:
            break

    print('sleep')
    time.sleep(5)

    gmc.heartbeatOff()

    start = time.time()
    for i in gmc.heart():
        print(i)
        if time.time() - start > timeout:
            break


def test_history(caplog):
    caplog.set_level(logging.INFO, logger='gmc.gmc')
    gmc.history()
    path = gmc.history_all()
    print(path)
    assert path

@pytest.mark.skip(reason="prepare to factory reset device")
def test_config_write(caplog):
    """ test writing config values
    """
    caplog.set_level(logging.INFO, logger='gmc.gmc')

    gmc.power_off()
    # refresh config from device
    gmc.config_load()

    speakerOnOff = gmc.device_fields.speakerOnOff
    calibrationCPM_0 = gmc.device_fields.calibrationCPM_0.value

    # modulate the speaker setting
    if speakerOnOff == 1:
        gmc.device_fields.speakerOnOff = 0
    else:
        gmc.device_fields.speakerOnOff = 1

    gmc.device_fields.calibrationCPM_0.value = calibrationCPM_0 + 1

    print('speakerOnOff:{} calibrationCPM_0:{}'.format(
        gmc.device_fields.speakerOnOff,
        gmc.device_fields.calibrationCPM_0.value)
    )

    assert gmc.device_fields.speakerOnOff != speakerOnOff

    assert gmc.device_fields.calibrationCPM_0.value == calibrationCPM_0 + 1

    gmc.config_write()
    gmc.reboot()
    gmc.config_load()

    # set to original values
    gmc.device_fields.speakerOnOff =  speakerOnOff
    gmc.device_fields.calibrationCPM_0.value = calibrationCPM_0

    print('speakerOnOff:{} calibrationCPM_0:{}'.format(
        gmc.device_fields.speakerOnOff,
        gmc.device_fields.calibrationCPM_0.value)
    )

    gmc.config_write()
    gmc.reboot()
    gmc.config_load()

    print('speakerOnOff:{} calibrationCPM_0:{}'.format(
        gmc.device_fields.speakerOnOff,
        gmc.device_fields.calibrationCPM_0.value)
    )

    assert gmc.device_fields.speakerOnOff == speakerOnOff
    assert gmc.device_fields.calibrationCPM_0.value == calibrationCPM_0


@pytest.mark.skip(reason="only when you need to.")
def test_reset():
    gmc.factory_reset()
    while gmc.version() == '':
        print('waiting..')

