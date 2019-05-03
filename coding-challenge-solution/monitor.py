#!/usr/bin/python3

import time
import argparse 
import schedule
import logging
import logging.handlers as handlers

from utilities import requirementCheck
from utilities import functions

logging.getLogger('schedule').propagate = False
logging.basicConfig(
    filename="logs/app.log",
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s"
)

logger = logging.getLogger(__name__)

requirementCheck.check_os_version(logger)

if __name__ == "__main__":
    ARG_PARSER = argparse.ArgumentParser()
    ARG_PARSER.add_argument(
        '--restart_wait_interval',
        help="Seconds to wait between attempts to restart service",
        required=False)
    ARG_PARSER.add_argument(
        '--max_fail_count',
        help="Number of attempts before giving up",
        required=False)
    ARG_PARSER.add_argument(
        '--process_name',
        help="Name of the process to monitor",
        required=False)
    ARG_PARSER.add_argument(
        '--health_check_interval',
        help="Health Check interval in seconds",
        required=False)
    ARG_PARSER.add_argument(
        '--start_command',
        help="Command to start the process",
        required=False)
    
    ARGUMENTS = ARG_PARSER.parse_args()

    restart_wait_interval = ARGUMENTS.restart_wait_interval
    max_fail_count = ARGUMENTS.max_fail_count
    process_name = ARGUMENTS.process_name
    health_check_interval = ARGUMENTS.health_check_interval
    start_command = ARGUMENTS.start_command

if restart_wait_interval is None:
    restart_wait_interval = input("Seconds to wait between attempts to restart service: ")


if max_fail_count is None:
    max_fail_count = input("Number of attempts before giving up: ")

if process_name is None:
    process_name = input("Name of the process to monitor: ")

if health_check_interval is None:
    health_check_interval = input("Health Check interval in seconds: ")

if start_command is None:
    start_command = input("command to re-start the process: ")

if not restart_wait_interval.isdigit() or int(restart_wait_interval) < 0:
    print("restart_wait_interval must be a positive integer")
    logger.error("restart_wait_interval must be a positive integer")
    exit()

if not max_fail_count.isdigit() or int(max_fail_count) < 0:
    print("max_fail_count must be a positive integer")
    logger.error("max_fail_count must be a positive integer")
    exit()

if not health_check_interval.isdigit() or int(health_check_interval) < 0:
    print("health_check_interval must be a positive integer")
    logger.error("health_check_interval must be a positive integer")
    exit()

COUNTER = 0
logger.info("######## New Process ######## \n \
    \tMonitoring params are: \n \
    \trestart_wait_interval = %s, \n \
    \tmax_fail_count = %s , \n \
    \tprocess_name = %s , \n \
    \thealth_check_interval = %s , \n \
    \tstart_command = %s \n ",
    restart_wait_interval, max_fail_count, process_name, health_check_interval, start_command )

def job():
    global COUNTER
    pids = functions.findProcessID(process_name, logger)

    if pids is '':
        logger.info("the process in down.. restarting")
        functions.restart_process(start_command, logger)
        COUNTER = COUNTER + 1
        if COUNTER >= int(max_fail_count):
            logger.error("max number of retires reached.. program unable to start.. shutting down")
            exit()
        time.sleep(int(restart_wait_interval))
    else:
        logger.debug("%s is running with pid: %s", process_name, pids)
        COUNTER = 0
    logger.info("#### Iteration complete ####")

schedule.every(int(health_check_interval)).seconds.do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)



# python monitor.py --restart_wait_interval 5 --max_fail_count 3 --process_name docker --health_check_interval 1 --start_command "service docker start"