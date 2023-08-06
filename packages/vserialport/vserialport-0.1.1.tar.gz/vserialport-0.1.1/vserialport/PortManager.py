from typing import NamedTuple, List, Union, Callable, Optional, Tuple, cast, Any
from SerialPort.ListConcreteSerialPorts import serial_ports
from SerialPort.ConcreteSerial import BaudRate
from SerialPort.SerialPort_ import SerialPort
from Common.Byte import Byte, Bytes

from enum import Enum
from time import sleep


Milliseconds = int

UUID = int   # Universal Unique Identifier / A ticket number (hash_code) that client will use to request response to server
Hash = int

# ============
# data model
# ============

class PortConfiguration(NamedTuple):
    baudRate: BaudRate
    readtTimerIn: Milliseconds = 1200  # don't wait response after this time
    inferiorWaitTime: Milliseconds = 100  # dont' read before this time

PortName = str

class SerialPortId(NamedTuple):
    name: PortName
    config: PortConfiguration


class PortManagerInfo(NamedTuple):
    listOfPorts: List[PortName]


# ============
# functions
# ============

Size = int


# Port Manager Owns this object
# Clients request him this obj to make his sync communication, when he finish they call close:
# the spefic protocol to this class is not defined yet.
class PortHandler:

    def __init__(self, s: SerialPortId, m: 'PortsManager'):
        self._portId: SerialPortId = s
        self._serialPort: SerialPort = m

    def read(self, s: Size) -> Bytes:
        return self._serialPort.read(s)

    def write(self, b: Bytes) -> Size:
        return self._serialPort.write(b)


Error = Optional[str]

# Basicly receive serial messages, and direct these messages to de respective ports, while wait for async_j response.
class PortsManager:

    def __init__(self):
        self._listOfPortsInUse: List[SerialPortId] = []

    def requestPortHandler(self, s: SerialPortId) -> (PortHandler, Error):
        error: Optional[str] = None
        handler: PortHandler = None
        if s.name not in serial_ports():
            error = "This port is not available by the operational system."
        elif s in self._listOfPortsInUse:
            error = "Port already in use by other routine. Wait until it become available again"
        else:
            self._listOfPortsInUse.append(s)
            ser = SerialPort(s.name, s.config.baudRate)
            handler = PortHandler(s, ser)
        return handler, error


    def update(self):
        pass

    def info(self) -> PortManagerInfo:
        info = PortManagerInfo(
            listOfPorts=serial_ports() )
        return info



if __name__=="__main__":

    portId1 = SerialPortId('COM5', PortConfiguration(BaudRate.Bps_9600))
    portId2 = SerialPortId('COM4', PortConfiguration(BaudRate.Bps_9600))

    manager = PortsManager()
    p1, error1 = manager.requestPortHandler(portId1)
    p2, error2 = manager.requestPortHandler(portId2)

    print(error1)
    print(error2)

    data = [Byte(65),Byte(67),Byte(68)]
    p1.write(data)
    print(p2.read(3))
    p2.write(data)
    print(p1.read(2))
    print(p1.read(1))
    print(p1.read(1))