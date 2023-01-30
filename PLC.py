# create an instance of a Modbus-TCP class (Server IP-Address and Port) and connect
# modbusclient = MBus.ModbusClient('10.0.0.41', 502)
# modbusclient.connect()

# DEGER OKUMA
# MetreBilgisi = modbusclient.read_inputregisters(10, 1)
# print(MetreBilgisi)


# DEGER SET ETME. - 1/0
# modbusclient.write_single_coil(7,False)
# ProgramOnOf = modbusclient.read_discreteinputs(7,1)
# print(ProgramOnOf)

# DEGER SET ETME DECIMAL
# holding_register_value = 41
# ADDR = 154
# modbusclient.write_single_register(ADDR, holding_register_value)
# PLC_PASTALOFSET = modbusclient.read_inputregisters(ADDR, 1)
# print(PLC_PASTALOFSET)

# Close the Port
# modbusclient.close()

# The first argument is the starting address, the second argument is the quantity.
# coils = modbus_client.read_coils(0, 2)	#Read coils 1 and 2 from server
# discrete_inputs = modbus_client.read_discreteinputs(10, 10)	#Read discrete inputs 11 to 20 from server
# input_registers = modbus_client.read_inputregisters(0, 10)	#Read input registers 1 to 10 from server
# holding_registers = modbus_client.read_holdingregisters(0, 5)	#Read holding registers 1 to 5 from server

# holding_register_value = 115
# coil_value = True
# The first argument is the address, the second argument is the value.
# modbus_client.write_single_register(0, holding_register_value)	#Write value "115" to Holding Register 1
# modbus_client.write_single_coil(10, coil_value)	#Set Coil 11 to True
import time

import easymodbus.modbusClient as MBus

class modbusPLC:
    def __init__(self, args):
        self.args = args
        self.plcIP = args.plcIP
        self.plcPort = args.plcPort
        self.addr_METRE_BILGISI = args.addr_METRE_BILGISI
        self.addr_STOP_PLC = args.addr_STOP_PLC

    def setPLC(self):

        # create an instance of a Modbus-TCP class (Server IP-Address and Port) and connect
        modbusclient = MBus.ModbusClient(self.plcIP, self.plcPort)
        modbusclient.connect()

        MetreBilgisi = modbusclient.read_inputregisters(self.addr_METRE_BILGISI, 1)
        print('Stop signal send to PLC on: ' + str(MetreBilgisi) + " -- " + time.ctime(time.time()))

        # DEGER SET ETME. - 1/0
        degerStop = True
        modbusclient.write_single_coil(self.addr_STOP_PLC, degerStop)
        myStop = modbusclient.read_discreteinputs(self.addr_STOP_PLC, 1)
        print(myStop)
        degerStop = False
        modbusclient.write_single_coil(self.addr_STOP_PLC, degerStop)

        # Close the Port
        modbusclient.close()