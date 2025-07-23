import platform
import os
import serial  # include pySerial 
import serial.tools.list_ports  # tool to find list_ports
import time
import stat

def write_to_NE_and_get_response( ser: serial, *messages: str):
    message_to_network = ""
    for message in messages:
        if message and isinstance(message, str):
            message_to_network += message
    ser.write(message_to_network.encode('utf-8'))
    time.sleep(0.05)  # Slight delay for pump processing
    response = ser.read(ser.in_waiting).decode('utf-8', 'ignore')
    return response.strip()

def pump_instance_test():
    port_list=serial.tools.list_ports.comports()
    correct_port=None
    lock_count=0
    for name in sorted(port_list):
        port_name=name[0]
        # print("Trying port: ", port_name)
        try:
            print("Trying port: ", port_name)
            os.chmod(port_name,stat.S_IRGRP )
            # os.chmod(port_name,stat.S_IXGRP )
            os.chmod(port_name,stat.S_IWGRP )
            ser=serial.Serial(port=str(port_name), baudrate=19200, timeout=5, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE )
            if ser.is_open:
                print("Connected to PORT ON: ", port_name, "Checking for NE pump firmware...")
                #try all possible addresses
                for n in range(10):
                    ser.reset_input_buffer()
                    pumpAddress = f"{n:02}"
                    test_message = f"{pumpAddress} VER\r"
                    # print(test_message.encode('utf-8'))
                    raw_response=write_to_NE_and_get_response(ser,test_message)
                    # print(raw_response)
                    if "NE" in response:
                        correct_port=port_name
                ser.close()
        except PermissionError as err:
            lock_count=lock_count+1
            # print(err)
        except Exception as err:
            # print("tested: ", port_name, " it was not correct.")
            # print(err)
            continue
        else:
            # print("tested: ", port_name, " it was not correct.")
            continue
    if correct_port:
        print("Correct port is: ", correct_port)
    else:
        print("Correct port not found, check connection and permissions!")
        if lock_count== len(port_list):
            print("Port is likely lacking read-write access, either set permissions for the port or run as Administrator!")
    return correct_port
def main():
    pump_instance_test()

if __name__ == "__main__":
    main()
