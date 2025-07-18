import platform
import os
import serial  # include pySerial 
import serial.tools.list_ports  # tool to find list_ports
import time

def decode_NE1000_responses(self, response: str)->str:
    start_char="\x02"
    end_char="\x03"
    resp=response.decode("utf-8", "ignore")
    """ The following character adjustments make the responses easier to read and
    clue the user into any errors. They should be in a dictionary or list to make code cleaner,
    but here they are.
    I is infused/infusing
    W is withdrew/withdrawing
    P is paused
    S is just a good command recieved"""
    resp=resp.replace(end_char,")")
    resp=resp.replace(start_char,"(")
    resp=resp.replace('S',f" pump: ")
    resp=resp.replace('I'," I ")
    resp=resp.replace('W'," W ")
    resp=resp.replace('P', " P ")
    resp=resp.replace('NA', " warning! Command not applicable ")
    resp=resp.replace('?', " Error in Command ")
    resp=resp.replace('COM', "Invalid packet")
    resp=resp.replace('OOR', "Command data is out of range")
    resp=resp.replace('IGN', "Command ignored due to a simultaneous new Phase start")
    return resp
## create a test instance to brute force try ports until a connection is sucessfull
def pump_instance_test():
    port_list=serial.tools.list_ports.comports()
    correct_port="port not found"
    for name in sorted(port_list):
        port_name=name[0]
        print("Trying port: ", port_name)
        try:
            print("Trying port: ", port_name)
            ser=serial.Serial(port=str(port_name), baudrate=19200, timeout=5, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE )
            ser.open()
            if ser.is_open:
                #try all possible addresses
                for n in range(10):
                    ser.reset_input_buffer()
                    pumpAddress = f"{n:02}"
                    test_message = f"{pumpAddress} VER \r"
                    ser.write(test_message.encode('utf-8'))
                    time.sleep(0.1)
                    raw_response=ser.read(ser.in_waiting)
                    response=decode_NE1000_responses(raw_response)
                    if "NE" in response:
                        correct_port=port_name
                ser.close()
        except Exception as err:
            print("tested: ", port_name)
            print(err)
            continue
        else:
            print("tested: ", port_name)
            continue
    print(correct_port)
    return correct_port
# def auto_detect_syringe_pump(port_value):
#     ports = serial.tools.list_ports.grep("Prolific")
#     for port, description, hardware in sorted(ports):
#         port_value = port
#     return str(port_value)
def main():
    # iter_list=serial.tools.list_ports.comports()
    # for i in sorted(iter_list):
    # print(iter_list[0][0])
    pump_instance_test()

if __name__ == "__main__":
    main()
