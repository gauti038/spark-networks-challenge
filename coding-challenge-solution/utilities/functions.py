import subprocess

def runShellCommand( command, logger ):
    try:
        shell_command = subprocess.Popen(command, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        output,err = shell_command.communicate()
    except e:
        logger.error("Error while running shell command: %s ",e)
        return False
    if err != None:
        logger.error("Command stderr is : %s ",e)
    return output    

def findProcessID( process_name, logger ):
    command = "pgrep " + process_name
    pid = runShellCommand(command, logger).decode("utf-8")
    # if pid is False:
    #     logger.error()
    return pid

def listAllDaemon():
    command = "ps -ef | awk '$3 == 1'| awk '{print $8}'|  awk -F / '{print $NF}'"
    daemon_list = runShellCommand(command).decode("utf-8") 
    return daemon_list

def restart_process(command, logger):
    restart_output = runShellCommand(command, logger).decode("utf-8")
    logger.debug("Restart command output: %s ", restart_output)
    return True


# print(type(findProcessID("asdf")))

# def startMonitoring(restart_wait_interval, max_fail_count, process_name, health_check_interval):
