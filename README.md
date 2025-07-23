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
   ```code pip install -r requirements.txt ```
   
5. Set all the script permissions to executable as well as the folder for storing log files
   ### On Linux/macOS
   - Navigate to the folder with the script
   ```code sudo chmod +x Pythonscript_jove_2025.py```
   - go up one level and give the folder read/write/exectute if needed (Mac):
   ```code cd..```
   ```code sudo chmod 775```
    ### On Windows (Command Prompt)


    ### On Windows (PowerShell)
 
   

6. Make sure the pumps have been wired correctly (see diagram below) and run (script A) to find the correct port:
   If you have trouble identifying the correct port, PySerial has a set of tools for scanning the ports on your computer
   To scan the ports, use:
   ### On Linux/macOS
   

    ### On Windows (Command Prompt)


    ### On Windows (PowerShell)
 
   
   Note that on some operating systems, you may need to grant access to read/write to the port in order for the script to work.
    ### On Linux/macOS
   

    ### On Windows (Command Prompt)


    ### On Windows (PowerShell)
 
   
8. Ensure the pump directly connected to the computer is set to address zero, and that each pump in the series is set to a unique address.
   
9. Adjust the protocol to suit your experiment and perform a test run, making adjustments as needed. Comments in the code should direct you on how to make most adjustments.
   More advanced pump programming may require consulting the pySerial documentation and/or the pump user manual.  
