import unittest 
import logging
import time

from utilities import functions
from utilities import requirementCheck

logging.getLogger('schedule').propagate = False
logging.basicConfig(
    filename="logs/test.log",
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s"
)

logger = logging.getLogger(__name__)

class TestUtilityFunctions(unittest.TestCase): 
      
    def setUp(self):
        pass

    def test_checkOs(self): 
        expected = True
        value = requirementCheck.check_os_version(logger)
        self.assertEqual(value, expected)

    def test_run_shell_command(self):
        output = functions.runShellCommand(' date +"%T"', logger).decode("utf-8").split('\n')[0]
        expected = str(time.strftime('%H:%M:%S'))
        self.assertEqual(output, expected)

    def test_find_process_id(self):
        process_name = "python"
        pid = functions.findProcessID(process_name, logger)
        self.assertNotEqual(pid, '')
  
if __name__ == '__main__': 
    unittest.main()