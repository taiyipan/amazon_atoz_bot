from driver_initializer import DriverInitializer
from login import Login
from schedule import Schedule
import traceback
import time
import sys

# verify command line arguments presence (script, arg1, arg2, ...)
assert len(sys.argv) == 7

try:
    # create driver
    driver = DriverInitializer(headless = True).get_driver()

    # bypass security
    login = Login(driver)
    login.run()

    # mine for shift blocks
    schedule = Schedule(driver, sys.argv)
    schedule.run()

except:
    traceback.print_exc()

# terminate program
def terminate():
    if driver is not None:
        driver.quit()
        time.sleep(5)
    print('program termination process')
    quit()
terminate()
