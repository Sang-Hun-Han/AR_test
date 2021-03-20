from pybleno import *
import time
import math


class PiBleCharacteristic(Characteristic):

    def __init__(self, uuid):
        Characteristic.__init__(self, {
            'uuid': uuid,
            'properties': ['read', 'write', 'notify'],
            'value': None
        })
        self._updateValueCallback = None

    def onSubscribe(self, maxValueSize, updateValueCallback):
        print('EchoCharacteristic - onSubscribe')
        self._updateValueCallback = updateValueCallback

    def onUnsubscribe(self):
        print('EchoCharacteristic - onUnsubscribe')

        self._updateValueCallback = None


def onStateChange(state):
    print('on -> stateChange: ' + state)

    if (state == 'poweredOn'):
        bleno.startAdvertising('PiBle', ['0000ec00-0000-1000-8000-00805f9b34fb'])
    else:
        bleno.stopAdvertising()


def onAdvertisingStart(error):
    print('on -> advertisingStart: ' + ('error ' + error if error else 'success'))

    if not error:
        bleno.setServices([
            BlenoPrimaryService({
                'uuid': 'ec00',
                # 'uuid': '0000ec00-0000-1000-8000-00805f9b34fb', これにするとPCとの接続がNG
                'characteristics': [
                    tomosoftCharacteristic_read
                ]
            })
        ])


def generatedata():
    x = 0.12
    y = 0.13
    z = 0.14
    for degx in range(-40, 40, 10):
        x = math.sin(math.radians(degx))
        for degy in range(-30, 30, 5):
            y = math.sin(math.radians(degy))
            formatted_msg = '%f,%f,%f' % (x, y, z)
            print(formatted_msg)
            tomosoftCharacteristic_read._updateValueCallback(str(formatted_msg).encode())
            time.sleep(1)
    return


if __name__ == '__main__':
    bleno = Bleno()
    bleno.on('stateChange', onStateChange)
    bleno.on('advertisingStart', onAdvertisingStart)
    tomosoftCharacteristic_read = PiBleCharacteristic('0000ec0f-0000-1000-8000-00805f9b34fb')
    bleno.start()

    while True:
        time.sleep(1)
        if tomosoftCharacteristic_read._updateValueCallback:
            print('Sending notification with value-cmd : ')
            # notificationBytes = str("0.45,0.56").encode()
            # tomosoftCharacteristic_read._updateValueCallback(generatedata())
            generatedata()
