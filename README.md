# syringe_pump
A script to run a network of NE-1000 SyringeONE syringe pumps.
## NOTE: Always perform a test run with no solutions or just water to ensure everything is working properly. 
### If the script is cancelled during a run, it should send a stop command to all the pumps. However, if this signal is interrupted, the pumps will continue to run.

## Set up
The suggested way to run this script is using pip. Eventually, this script will get a GUI, time permitting.
1. Set up your virtual Python environment using something like:

   ```code python -m venv my_project_venv ```
2. Activate the virtual environment
    ### On Linux/macOS
    ```code source my_project_venv/bin/activate ```

    ### On Windows (Command Prompt)
    ```code my_project_venv\Scripts\activate.bat ```

    ### On Windows (PowerShell)
    ```code my_project_venv\Scripts\Activate.ps1 ```
   
3. Install the dependencies using the requirements.txt file:
   ###
   ```code pip install -r requirements.txt ```
   
5. Set all the script permissions to executable as well as the folder for storing log files
   ### On Linux/macOS
   - Navigate to the folder with the scripts
   ```code sudo chmod +x Pythonscript_jove_2025.py```
   ```code sudo chmod +x find_correct_port.py```
   - (*If Needed*) go up one level and give the folder read/write/execute (Mac OS):
   ```code cd..```
   ```code sudo chmod 775```
    ### On Windows (Command Prompt)


    ### On Windows (PowerShell)
 
   

6. Make sure the pumps have been wired correctly (see user manual if needed) and run (find_correct_port.py) to find the correct port:

   ```code python find_correct_port.py```
   If you have trouble identifying the correct port, PySerial has a set of tools for scanning the ports on your computer
   To scan the ports, use:
   ### On Linux/macOS
      ```code sudo chmod + Pythonscript_jove_2025.py```


    ### On Windows (Command Prompt)


    ### On Windows (PowerShell)
 
   
   Note that on some operating systems, you may need to grant access to read/write to the port in order for the script to work.
    ### On Linux/macOS
      ```code sudo chmod +765 Pythonscript_jove_2025.py```
   this will have to be rerun each time you log out/reboot, to avoid running the code as 'sudo' a better option is to set the user to have access to the port
   navigate to the the port and do
   sudo usermod -a -G dialout $USER

    ### On Windows (Command Prompt)


    ### On Windows (PowerShell)
 
   
8. Ensure the pump directly connected to the computer is set to address zero, and that each pump in the series is set to a unique address.
   You will probably get an error if you don't do this, but if something is wrong with the rates being pumped and it isnt the code, this is probably it.
   
10. Adjust the protocol to suit your experiment and perform a test run, making adjustments as needed. Comments in the code should direct you on how to make most adjustments.
   More advanced pump programming may require consulting the pySerial documentation and/or the pump user manual.  If you want to run the code with the right timing but without actually pumping anything,
   use test_run=True
