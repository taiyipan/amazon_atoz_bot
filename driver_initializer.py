from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import platform

class DriverInitializer:
    def __init__(self, headless = False):
        # configure chromedriver options
        options = Options()
        if headless:
            options.headless = True
            options.add_argument('--log-level=3')
            options.add_argument('--window-size=1920x1080')

        # open chromedriver
        self.driver = webdriver.Chrome(executable_path = self.find_driver_path(), chrome_options = options)
        self.driver.maximize_window()
        print('Driver initialized, headless mode: {}'.format(headless))

    # determine driver_path
    def find_driver_path(self) -> str:
        # set chromedriver path for local machine
        driver_path = '/usr/bin/chromedriver' # Ubuntu
        driver_path2 = '/mnt/c/Users/taiyi/taiyi/automata/1_twitter_bot/sign_up_bot/chromedriver.exe' # Windows 10
        driver_path3 = '/Users/taiyipan/chromedriver' # Mac OSX
        # get current host computer name
        hostname = platform.node()
        # return driver_path
        if hostname == 'Galatea':
            return driver_path2
        elif hostname == 'sol.lan':
            return driver_path3
        elif hostname == 'eternal' or hostname == 'raspberrypi':
            return driver_path
        else: # if host computer is not recognized
            driver.close()
            quit()

    # return chromedriver object reference
    def get_driver(self):
        return self.driver
