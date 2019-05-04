# Coding Challenge - daemon supervisor #

## Assumptions ##
1. Donot use 3rd party supervisor tools. I have written this code using python. without using any 3rd party publicly available tools like supervisord 
2. Write unit test cases for the functions
3. Log events or any errors
4. Parameters can be passed while starting the function or at runtime
5. The process is run on a Linux Machine

## Run the application ##
1. create a python virtual environment (optional)
   ``` virtualenv -p python3 daemon-dependencies ```
   and activate the environment ``` source daemon-dependencies/bin/activate ```
2. Install the oython requirements  
    ``` pip install -r requirements.txt ```
3. Run the monitor application 
    ``` python monitor.py --restart_wait_interval 5 --max_fail_count 3 --process_name docker --health_check_interval 1 --start_command "service docker start" ```
4. Make sure you are running this as a user who has permission to run start_command
5. You can start this in either background or foreground or as daemon process 
6. The script writes logs to file app.log --> ADD LOG ROTATE <---

## WORKFLOW ##
1. When starting the script, it will check if all parameters are passed (order doesn't matter). If any of the required params are missing, it asks the user to submit those values as interactive inputs.
2. After the code has all the params, it checks if the time parameters are indeed positive numbers. Else it throws an error.
3. I have used a python scheduler module to schedule health checks at every time interval
4. When the code starts, it checks if the OS supports the code. (Linux in this case). Else throws an error and shuts down.
5. Using pgrep command of ubuntu, I check for the pid of the process. If it returns a value, the process is still running, else it is down. 
6. If the process is down, the start command is run. (Please ensure the user who calls this script has access to run start command). There is also a counter that keeps track of the number of times this start command is called
7. If the process is not running after max_fail_count number of retries, the program logs the detail and stops execution. 
8. The logs are written in logs folder using a specific format with loglevel and timestamp
9. Unit tests are written for each of the functions in tests.py file




