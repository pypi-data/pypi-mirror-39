# Transact a unique object through serial.
# Algorithm: Send the object, wait, and take the returned object

from SerialPort.PortManager import PortsManager, SerialPortId, PortConfiguration
from SerialPort.ConcreteSerial import BaudRate
from Common.Byte import Byte, Bytes, convertToBytes, fromBytesTobytes
from time import sleep

# portId helper factory
def createPortId(portName:str, baud_rate:str) -> SerialPortId:
    #todo: check if portName is valid

    # set baud rate
    if baud_rate == 9600 :
        rate = PortConfiguration(BaudRate.Bps_9600)
    elif baud_rate == 2400:
        rate = PortConfiguration(BaudRate.Bps_2600)
    else:
        raise("PortId esta send criado com baud_rate nao implementado")

    return SerialPortId(portName, rate)


def transactObjectThroughSerial(portId: SerialPortId, dataObj: bytes) -> bytes:
    # openPhisicalPort
    manager = PortsManager()
    port, error1 = manager.requestPortHandler(portId)
    print(port, error1)
    if (error1 == None):
        # Send
        d = convertToBytes(dataObj)
        print("Enviando: ", d)
        s = port.write(d)
        # Wait
        sleep(0.150)
        # read
        # Create Port Spec
        portId2 = createPortId('COM4', 9600)
        port2, error2 = manager.requestPortHandler(portId2)
        d = port2.read(s)
        print(d)
        data = fromBytesTobytes(d)
        return data
    else:
        raise ("Erro na transferencia do pacote pela porta fisica")


