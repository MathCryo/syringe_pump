This repository corresponds to the work presented in:
Low-Cost 3D-Printed Microfluidic Devices for Rapid Prototyping and Biological Applications
DOI: 10.3791/69494




# syringe_pump
A script to run a network of NE-1000 SyringeONE syringe pumps. Along with files for 3D printing a microfluidic mixing slide and connectors. 
For instructions on how to assemble and seal the slide, please see the published work at:


## NOTE: Always perform a test run with no solutions or just water to ensure everything is working properly. 
### If the script is cancelled during a run, it should send a stop command to all the pumps. However, if this signal is interrupted, the pumps will continue to run.

## Script Set up
The suggested way to run this script is using pip. Eventually, this script will get a GUI, time permitting.
1. Set up your virtual Python environment using something like:

   ``` python -m venv my_project_venv ```
2. Activate the virtual environment
    ### On Linux/macOS
    ``` source my_project_venv/bin/activate ```

    ### On Windows (Command Prompt)
    ``` my_project_venv\Scripts\activate.bat ```

    ### On Windows (PowerShell)
    ``` my_project_venv\Scripts\Activate.ps1 ```
   
3. Install the dependencies using the requirements.txt file:
   ###
   ``` pip install -r requirements.txt ```
   
4. Set all the script permissions to executable as well as the folder for storing log files
   ### On Linux/macOS
   - Navigate to the folder with the scripts
   
      ``` sudo chmod +x Pythonscript_jove_2025.py```
   
      ``` sudo chmod +x find_correct_port.py```

   - (*If Needed*) go up one level and give the folder read/write/execute (Mac OS):

      ``` cd..```

      ``` sudo chmod .../folder_name 775```

   ### On Windows (Command Prompt)
   - Should just work, but you may need to run as Administrator

   ### On Windows (PowerShell)
   - Should just work, but you may need to run as Administrator
   

6. Make sure the pumps have been wired correctly (see user manual if needed) and run (find_correct_port.py) to find the correct port:

      ``` python find_correct_port.py```

   Note that on some operating systems, you may need to grant access to read/write to the port in order for the script to work. You can also run it as Administrator/Sudo.

      ### On Linux/macOS

      ```sudo chmod 765 Pythonscript_jove_2025.py```
   
      #### This will have to be rerun each time you log out/reboot. To avoid running the code as 'sudo', a better option is to set the user to have access to the port.
      - Navigate to the port and do
         ``` sudo usermod -a -G dialout $USER ``` (the usergroup will be uucp for the arch users, but if that's you (or some similar distro), you probably don't need this guide)

   If you still have trouble identifying the correct port, PySerial has a set of tools for scanning the ports on your computer
   To scan the ports, use:
   ### On most OSes:
      ``` python serial.tools.list_ports```
   
8. Ensure the pump directly connected to the computer is set to address zero, and that each pump in the series is set to a unique address.
   The code should throw an error if you don't do this, but if something is wrong with the rates being pumped and it isn't the code, this is probably the cause.
   
9. Adjust the protocol to suit your experiment and perform a test run, making adjustments as needed. Comments in the code should direct you on how to make most adjustments.
   More advanced pump programming may require consulting the pySerial documentation and/or the pump user manual.  If you want to run the code with the right timing but without actually pumping anything,
   use test_run=True; this will issue a command asking the pump for its firmware version instead of issuing the run command.

10. Run with the usual Python command and your active virtual environment:
   ``` python Pythonscript_jove_2025.py ```
