# Concrete Serial port representation
# author: Flavio Vilante
from typing import NamedTuple, Any, Dict
from enum import Enum
import serial

from Common.Byte import Byte, Bytes, convertToBytes, fromBytesTobytes
from SerialPort.ListConcreteSerialPorts import serial_ports



class BaudRate(Enum):
    # for complete list see: https://pythonhosted.org/pyserial/pyserial_api.html
    Bps_2400 = 2400
    Bps_9600 = 9600
    Bps_19200 = 19200

class Parity(Enum):
    EVEN = serial.PARITY_EVEN
    NONE = serial.PARITY_NONE
    ODD = serial.PARITY_ODD
    DEFAULT = serial.PARITY_NONE

class XonXoff(Enum):
    DEFAULT = 0 # todo: don't use 'default' keyword, it's error prone

class RtsCts(Enum):
    HARDWARE = 1
    DEFAULT = 0

PortName = str

TimeOut = int  #in seconds
ByteSize = int #ie: 8
StopBits = int #ie: 1
class PortParameters(NamedTuple):
    port: PortName
    baudRate: BaudRate
    timeout: TimeOut
    parity: Parity
    byteSize: ByteSize
    stopBits: StopBits
    xonxoff: XonXoff
    rtscts: RtsCts




Size = int

# for more see: https://pyserial.readthedocs.io/en/latest/shortintro.html#opening-serial-ports
# todo: insert a exception handler where is necessary
# todo: there is a bug, can't make (read)timeout=0 [no blocking], if I do, test hang on serial read.
#       I'll delay solution, in hope reveal new information on use.
class ConcreteSerialPort_Impl1:
    def __init__(self, parameters: PortParameters ) -> None:
        self._parameters: PortParameters = parameters

    def initialize(self) -> serial.Serial:
        ser = self._init()
        self._configure(ser)
        self._open(ser)
        return ser


    def _getConfiguration(self) -> Dict[str, Any]:
        params = {
            'url' : self._parameters.port,
            'baudrate' : self._parameters.baudRate.value,
            'timeout' : self._parameters.timeout,
            'parity' : self._parameters.parity.value,
            'bytesize' : self._parameters.byteSize,
            'stopbits' : self._parameters.stopBits,
            'xonxoff' : self._parameters.xonxoff.value,
            'rtscts' : self._parameters.rtscts.value,
            'write_timeout': 1 # todo: eventually make this parameter available for clients of this class
        }
        return params


    def _read(self, s: Size) -> bytes:
        config = self._getConfiguration()
        res: bytes = bytes([])
        with serial.serial_for_url(**config) as ser:
            res = ser.read(s)
        return res

    def _write(self, b: bytes) -> Size:
        config = self._getConfiguration()
        with serial.serial_for_url(**config) as ser:
            res = ser.write(b)
        return res


    def read(self, s: Size) -> Bytes:
        r = self._read(s)
        return convertToBytes(r)

    def write(self, b: Bytes) -> Size:
        d = fromBytesTobytes(b)
        return self._write(d)


def createConcretePort(portName: PortName, baudRate: BaudRate) -> ConcreteSerialPort_Impl1:
    params = PortParameters(
        port= portName,
        baudRate= baudRate,
        timeout= 0.5,  # timeout = 0: non-blocking mode, return immediately in any case, returning zero or more, up to the requested number of bytes
        parity= Parity.NONE,
        byteSize= 8,
        stopBits= 1,
        xonxoff= XonXoff.DEFAULT,
        rtscts= RtsCts.DEFAULT
    )
    return ConcreteSerialPort_Impl1(params)

if __name__ == "__main__":

    print(serial_ports())




    #com5 = createConcretePort('COM5', BaudRate.B_2400_Bps)

    #com4.write(Byte(65))
    #print(com5.read(1))

    a = "junior".encode()
    for i in range(10):

        #print("ooo")
        #ser = serial.serial_for_url('COM4', baudrate=9600, timeout=0.5)
        #print("->",ser.is_open())

        #with serial.Serial('COM4', baudrate=9600, timeout=0.5) as ser:
        #    print("gravei")
        #    ser.write(bytes(a))

        com4 = createConcretePort('COM5', BaudRate.Bps_19200)
        size = com4.write(convertToBytes(bytes(a)))

        com5 = createConcretePort('COM4', BaudRate.Bps_19200)
        data = com5.read(len(a))
        print("li")
        print(data)


        #print(data)



        #with serial.Serial('COM5', baudrate=9600, timeout=0.5) as ser:
        #    s = ser.read(len(a))
        #    print("li")
        #    print(s)




    pass