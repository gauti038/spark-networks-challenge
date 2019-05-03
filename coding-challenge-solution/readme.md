CODING CHALLENGE:
The idea is to create a “daemon supervisor”. This tool should check that the process is
running and at all times and starts it in case is down. It should take as parameters:
 Seconds to wait between attempts to restart service
 Number of attempts before giving up
 Name of the process to supervise
 Check interval in seconds
 Generate logs in case of events.



Coding challenge:
Here we want to see your coding/scripting skills. We want to see how you structure the code,
documentation. You can choose the language you want



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
5. Unit tests are written for each of the functions.
6. 


