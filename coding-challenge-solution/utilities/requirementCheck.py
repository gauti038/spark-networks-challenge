import platform

# check the os platform 
def check_os_version(logger):
    os_platform = platform.system()

    if os_platform != 'Linux':
        logger.error("This runs only on Linux..")
        shutdown_monitoring()
    else:
        logger.info("Linux OS - Check")
        return True

def shutdown_monitoring():
    exit()