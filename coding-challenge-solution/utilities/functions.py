import subprocess
import json

# read the config file 
with open('config.json') as config_file:
    config = json.load(config_file)

# run any shell command on the os with stdout and stderr streams
def runShellCommand( command, logger ):
    try:
        shell_command = subprocess.Popen(command, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        output,err = shell_command.communicate()
    except e:
        logger.error("Error while running shell command: %s ",e)
        exit()
    if err != None:
        logger.error("Command stderr is : %s ",e)
    return output    

# find process ID of the process 
def findProcessID( process_name, logger ):
    command = config["checkCommand"] +" " + process_name
    pid = runShellCommand(command, logger).decode("utf-8")
    return pid

# get list of all daemon process - PPID = 1
def listAllDaemon():
    command = "ps -ef | awk '$3 == 1'| awk '{print $8}'|  awk -F / '{print $NF}'"
    daemon_list = runShellCommand(command).decode("utf-8") 
    return daemon_list

# restart the process using command
def restart_process(command, logger):
    restart_output = runShellCommand(command, logger).decode("utf-8")
    logger.debug("Restart command output: %s ", restart_output)
    return True

