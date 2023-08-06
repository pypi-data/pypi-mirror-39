#A serial port object
from typing import NamedTuple, List, Callable
from time import sleep
from Common.Byte import Byte, Bytes
from SerialPort.ConcreteSerial import createConcretePort, BaudRate


# =====================================


class SerialPortInfo(NamedTuple):
    #initialization time
    #first transmission type
    #number of bytes sent
    #number of bytes read
    #reconfigurations history...
    #etc...
    pass



Size = int
SerialWriteFunction = Callable[[Bytes], Size]
SerialReadFunction = Callable[[Size], Bytes]
SerialPortOSName = str #Operational System port Name

# Mid-level port representation
# Responsible to send and receive Bytes to the concrete serial driver
class SerialPort:

    def __init__(self, p: SerialPortOSName,  b: BaudRate):
        self.osName = p
        self.baudRate = b
        self._info = SerialPortInfo()

    def reconfigure(self, p: SerialPortOSName,  b: BaudRate):
        self.osName = p
        self.baudRate = b

    def read(self, s: Size) -> Bytes:
        port = createConcretePort(self.osName, self.baudRate)
        return port.read(s)

    def write(self, b: Bytes) -> Size:
        port = createConcretePort(self.osName, self.baudRate)
        return port.write(b)

    def info(self) -> SerialPortInfo:
        return self._info



if __name__ == "__main__":


    for i in range(5):

        port1 = SerialPort("COM5", BaudRate.Bps_9600)
        port1.write([Byte(65),Byte(67)])

        sleep(0.1)

        port2 = SerialPort("COM4", BaudRate.Bps_2400)
        data = port2.read(2)
        print(data)

