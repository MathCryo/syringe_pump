import serial  # include pySerial 
import asyncio  # asynchronous python
import serial.tools.list_ports  # tool to find ports
import logging # python package for logging
import os
import stat
import time
from datetime import date # python package for working with date/time
import sys
""" SET THE PORT FOR THE WHOLE FILE HERE"""
PORT ="/dev/ttyUSB0"
""" Global variable for handling crashes during pumping to minimize experiments gone bad."""
CURRENT_PUMP_NETWORK=False
# Create and configure a logger
todays_date = date.today()
date_based_logfile = f"pumpLog-{todays_date}.log"

logging.basicConfig(
    filename=date_based_logfile,
    filemode='a',
    format='%(levelname)s - %(asctime)s - %(message)s',
    level=logging.INFO
)

"""for mac (and possibly other systems) make sure I have file permissions to write log file """
def test_permission():
    # file_path = os.path.directory(os.path.realpath(date_based_logfile))
    # print(file_path, permissions)
    try:
        logging.info("This is a test log message to check permissions.")
        ser=serial.Serial(port=PORT, baudrate=19200, timeout=5, 
                          parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE )
        ser.close()
    except (IOError, PermissionError) as e:
        print(f"Permission error encountered: {e}")
        print(f"The logging module does not have permission to write to: {log_file_path} or {PORT}")
        sys.exit(1)
""" command to write to pump without using async used just for testing"""
def write_to_NE_and_get_response( ser: serial, *messages: str):
        message_to_network = ""
        for message in messages:
            if message and isinstance(message, str):
                message_to_network += message
        ser.write(message_to_network.encode('utf-8'))
        time.sleep(0.05)  # Slight delay for pump processing
        response = ser.read(ser.in_waiting).decode('utf-8', 'ignore')
        return response.strip()

"""we test the pump addresses without async"""
def test_pump_addresses(number_of_pumps):
    try:
        ser=serial.Serial(port=PORT, baudrate=19200, timeout=5,
                          parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE )
        
        if ser.is_open:
            print("Connected to PORT ON: ", PORT, "\nChecking for NE pump firmware and Network Addresses...")
            #try all possible addresses
            address_list=[]
            correct_addresses = [i for i in range(0, number_of_pumps)]
            for n in range(10):
                ser.reset_input_buffer()
                pumpAddress = f"{n:02}"
                test_message = f"{pumpAddress} VER\r"
                print(test_message.encode('utf-8'))
                firmware_response=write_to_NE_and_get_response(ser,test_message)
                print(firmware_response)
                raw_response=write_to_NE_and_get_response(ser,test_message)
                if "NE" in firmware_response:
                    address_list.append(n)
            ser.close()
            if address_list!=correct_addresses:
                # print(address_list)
                # print(correct_addresses)
                raise Exception

    except Exception as e:
        print(f"There is an issue with the pump network number of pumps, firmware, or pump addresses !!!!!!! {e}")
        sys.exit(1)

""" This Class defines a Pump network consisting of at least one NE-1000 pump(s)
    Script users should set the port='USERPORT'. When the pumps run a basic logfile is 
    created. 
    Commands are sent to the pump network and await for a response, these responses include
    success and error messages which can be decifered using the pump user manual and to a limited degree this code.
    This may be helpful in debugging if your code isn't working correctly.
    If you are having trouble identifying the correct port, please use the pySerial tools.
    Some computer operating systems will require you to give permissions to both this script and the port in order
    for the program to run. Basic instructions are provided in the github repository, but please contact your systems
    administrator if you need further help.
"""
class PumpNE:
    def __init__(self, number_of_pumps, port=PORT,test_run=False): ## be sure to set this port to the correct one for your computer
        ## ports on windows look like COM3, on Linux they look like /dev/ttyUSB0
        #you should probably just set the permission correctly but you can run as administrator or using sudo on some systems
        self.pump_ID = []
        self.port = port
        self.number_of_pumps = number_of_pumps
        self.test_run=test_run
        print("Pump Created")
        self.ser = serial.Serial()
        CURRENT_PUMP_NETWORK=True
    def __enter__(self):
        ## suggested settings for the NE-1000 pump
        print(self.port)
        self.ser.port = self.port
        self.ser.baudrate = 19200
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout = 5
        self.ser.open()
        logging.info("Pump Network Connected!!")
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """ Correctly destruct pump network as well as make sure all pumps on the network are stopped and port is closed """
        for address in range(self.number_of_pumps):
            pumpAddress = f"{address:02}"
            stop_message = f"{pumpAddress} STP\r"
            self.ser.write(stop_message.encode('utf-8'))
            self.ser.reset_input_buffer()
        self.ser.close()
        print("Pump Disconnected.")

    async def initialize_pumps(self, syringe_diams):
        pass
    async def test_pump_addresses(self):
        pass

    async def write_to_NE_and_log_response(self, *messages: str):
        message_to_network = ""
        for message in messages:
            if message and isinstance(message, str):
                message_to_network += message
        if self.test_run: # for degbugging we don't want to actually run the pumps
            if "RUN" in message_to_network:
                message_to_network=message_to_network.replace("RUN","VER")
        self.ser.write(message_to_network.encode('utf-8'))
        await asyncio.sleep(0.05)  # Slightly longer delay for pump processing
        response = self.ser.read(self.ser.in_waiting).decode('utf-8', 'ignore')
        logging.info(f"Command Sent: {message_to_network.strip()} | Response: {response.strip()}")
        print(f"Command Sent: {message_to_network.strip()} | Response: {response.strip()}")
        return response.strip()

async def mixing_test(porty,test_run=False):
    """ Run Pump Network with Gradual Rate Changes """
    with PumpNE(2, port=porty, test_run=test_run) as p1:  # Adjusted for 2 pumps
        print(f"This is a test of a network of {p1.number_of_pumps} pumps")
        CURRENT_PUMP_NETWORK=p1
        # Set initial pump settings
        await p1.write_to_NE_and_log_response('00 DIA 10.30\r')  # Pump A diameter
        await p1.write_to_NE_and_log_response('01 DIA 10.30\r')  # Pump B diameter
        await p1.write_to_NE_and_log_response('00 VOL UM\r')  # Pump A unit
        await p1.write_to_NE_and_log_response('01 VOL UM\r')  # Pump B unit

        # Parameters for gradual rate adjustments
        duration_in_seconds = 10 * 60  # 10 minutes per ramp (up or down)
        step_length_in_seconds = 5  # Step duration
        steps = round(duration_in_seconds / step_length_in_seconds)  # Total steps
        max_rate = 20  # Maximum rate in uL/min

        # Gradually increase Pump B and decrease Pump A
        for step in range(steps):  # Loop through steps
            pump_a_rate = round(max_rate - step * (max_rate / steps), 2)  # Gradual decrease for Pump A
            pump_b_rate = round(step * (max_rate / steps), 2)  # Gradual increase for Pump B

            print(f"Step {step + 1}: Pump A Rate = {pump_a_rate}, Pump B Rate = {pump_b_rate}")

            # Stop pumps before setting new rates
            await p1.write_to_NE_and_log_response('00 STP\r')
            await p1.write_to_NE_and_log_response('01 STP\r')

            # Send rate commands
            await p1.write_to_NE_and_log_response(f'00 RAT {pump_a_rate} UM\r')  # Pump A
            await p1.write_to_NE_and_log_response(f'01 RAT {pump_b_rate} UM\r')  # Pump B

            # Start pumps
            await p1.write_to_NE_and_log_response('00 RUN\r')
            await p1.write_to_NE_and_log_response('01 RUN\r')

            await asyncio.sleep(step_length_in_seconds)  # Wait for the next step

        # Gradually increase Pump A and decrease Pump B
        for step in range(steps):  # Loop through steps
            pump_a_rate = round(step * (max_rate / steps), 2)  # Gradual increase for Pump A
            pump_b_rate = round(max_rate - step * (max_rate / steps), 2)  # Gradual decrease for Pump B

            print(f"Step {step + 1 + steps}: Pump A Rate = {pump_a_rate}, Pump B Rate = {pump_b_rate}")

            # Stop pumps before setting new rates
            await p1.write_to_NE_and_log_response('00 STP\r')
            await p1.write_to_NE_and_log_response('01 STP\r')

            # Send rate commands
            await p1.write_to_NE_and_log_response(f'00 RAT {pump_a_rate} UM\r')  # Pump A
            await p1.write_to_NE_and_log_response(f'01 RAT {pump_b_rate} UM\r')  # Pump B

            # Start pumps
            await p1.write_to_NE_and_log_response('00 RUN\r')
            await p1.write_to_NE_and_log_response('01 RUN\r')

            await asyncio.sleep(step_length_in_seconds)  # Wait for the next step

        # Stop both pumps at the end of the ramp sequence
        await p1.write_to_NE_and_log_response('00 STP\r')
        await p1.write_to_NE_and_log_response('01 STP\r')

        # Keep Pump A running at 20 µL/min for an additional 10 minutes
        additional_duration = 10 * 60  # 10 minutes in seconds
        await p1.write_to_NE_and_log_response(f'00 RAT {max_rate} UM\r')  # Pump A at 20 µL/min
        await p1.write_to_NE_and_log_response('00 RUN\r')  # Start Pump A
        print(f"Pump A continues running at {max_rate} µL/min for an additional 10 minutes.")
        await asyncio.sleep(additional_duration)  # Wait for 10 minutes

        # Stop Pump A after the additional 10 minutes
        await p1.write_to_NE_and_log_response('00 STP\r')
        print("Pump A stopped after additional 10 minutes.")
## This function is hardware specific use find_correct_port.py instead if you are using NE pumps
def auto_detect_syringe_pump(port_value):
    ports = serial.tools.list_ports.grep("Prolific")
    for port, description, hardware in sorted(ports):
        port_value = port
    return str(port_value)
def pretest():
        test_permission()
        test_pump_addresses(2)
async def main():
    try:
        ## Port value also needs to be set here
        # porty = '/dev/ttyUSB0'
        await mixing_test(PORT, test_run=True)
    except PermissionError as e:
        print("File or Port does not have the correct level of permission, try running as administrator! or adjust read/write access to allow port this directory")
    except Exception as e:
        print(f"!!!!!!!!! Something went wrong: {e} !!!!!!!")
        with PumpNE(2) as p1:
            await p1.write_to_NE_and_log_response('00 STP\r')
            await p1.write_to_NE_and_log_response('01 STP\r')
    finally:
        # stop all pumps even if code is exited or interupted
        with PumpNE(2) as p1:
            for n in range(10):
                pumpAddress = f"{n:02}"
                test_message = f"{pumpAddress} STP\r"
                await p1.write_to_NE_and_log_response(test_message)

if __name__ == '__main__':
    pretest()
    time.sleep(0.05)
    print("Pumps are ready! Running experiment!")
    asyncio.run(main())
