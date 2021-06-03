from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from credential import Credential
from backend import Backend
from email_interface import EmailInterface
from datetime import datetime
from datetime import timedelta
import time
import platform
import traceback

class Schedule:
    def __init__(self, driver, raw_input: list):
        self.driver = driver
        self.credential = Credential()
        self.backend = Backend()
        self.interface = EmailInterface()
        self.priority_list = self.backend.build_priority_list(raw_input)
        print('Priority List:', self.priority_list)
        self.wait_time = 4 # seconds - time to check presence of shifts
        self.max_wait_time = 30 # seconds - time to wait for webpage loading
        self.continue_loop = True # whether or not to continue loop
        self.activation = True
        self.clock_now = None
        self.final_shift_selection = None
        print('Schedule initialized')

    def run(self):
        time.sleep(15)
        self.go_to_schedule()
        time.sleep(6)
        self.apply_filters()
        time.sleep(3)
        self.loop()
        self.status_report()
        self.check_password()

    def go_to_schedule(self):
        # locate dropdown_menu
        dropdown_menu = WebDriverWait(WebDriverWait(self.driver, 7).until(
            EC.presence_of_element_located((
                By.ID,
                'navbar-menu'
            ))
        ), 7).until(
            EC.presence_of_element_located((
                By.XPATH,
                './/ul[1]/li[@class="dropdown"]'
            ))
        )
        # locate and click schedule_tab
        schedule_tab = WebDriverWait(dropdown_menu, 5).until(
            EC.presence_of_element_located((
                By.XPATH,
                './/a'
            ))
        )
        self.driver.execute_script("arguments[0].click();", schedule_tab)
        # locate and click find_shifts
        find_shifts = WebDriverWait(dropdown_menu, 5).until(
            EC.presence_of_element_located((
                By.XPATH,
                './/ul/li[1]/a'
            ))
        )
        self.driver.execute_script("arguments[0].click();", find_shifts)

    def apply_filters(self):
        self.filter_site()
        self.filter_date()
        # self.filter_unavailables()

    def filter_site(self):
        # locate sites
        sites = WebDriverWait(WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((
                    By.CLASS_NAME,
                    'atoz-filterContent'
                ))
        ), 5).until(
            EC.presence_of_element_located((
                By.XPATH,
                './/fieldset[3]/div[2]/div/form'
            ))
        )
        # locate and click all_sites
        all_sites = WebDriverWait(sites, 5).until(
            EC.presence_of_element_located((
                By.XPATH,
                './/div[@data-test-checkbox-wrapper-id="all"]'
            ))
        )
        self.driver.execute_script("arguments[0].click();", all_sites)
        # locate and click work_site
        work_site = WebDriverWait(sites, 5).until(
            EC.presence_of_element_located((
                By.XPATH,
                './/div[@data-test-checkbox-wrapper-id="{}"]'.format(self.credential.workgroup_name())
            ))
        )
        self.driver.execute_script("arguments[0].click();", work_site)

    def filter_unavailables(self):
        # locate sites
        sites = WebDriverWait(WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((
                    By.CLASS_NAME,
                    'atoz-filterContent'
                ))
        ), 5).until(
            EC.presence_of_element_located((
                By.XPATH,
                './/fieldset[4]/div[2]/div/form'
            ))
        )
        # locate and click unavailables
        unavailables = WebDriverWait(sites, 5).until(
            EC.presence_of_element_located((
                By.XPATH,
                './/div[@data-test-checkbox-wrapper-id="all"]'
            ))
        )
        self.driver.execute_script("arguments[0].click();", unavailables)

    def filter_date(self):
        # locate and click date_tab
        date_tab = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((
                By.ID,
                'daybutton-{}'.format(self.backend.get_shift_date())
            ))
        )
        self.driver.execute_script("arguments[0].click();", date_tab)

    def filter_time(self):
        # locate time_field
        time_field = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((
                By.CLASS_NAME,
                'atoz-filter-start-time'
            ))
        )
        # locate and enter start_time
        start_time = WebDriverWait(time_field, 5).until(
            EC.presence_of_element_located((
                By.XPATH,
                './/span[@data-testid="start-time"]/input'
            ))
        )

    def clock(self):
        clock_now = datetime.now().strftime('%-I:%M%p')
        if self.clock_now is None or not self.clock_now == clock_now:
            print(clock_now)
        self.clock_now = clock_now

    def check_password(self):
        if platform.node() == 'Galatea' and not self.backend.check_password():
            self.interface.password_reminder()

    def status_report(self):
        status = not self.continue_loop
        message = self.backend.get_shift_date() + ' ' + self.backend.get_shift_weekday() + ' '
        if status:
            message += self.final_shift_selection
        else:
            message += str(self.priority_list)
        self.interface.status_report(status, message)

    # main loop function to mine for shift blocks
    def loop(self):
        i = 0 # cycle counter
        t_0 = None # cycle timer
        while self.continue_loop and self.backend.validate_duration():
            # display clock
            self.clock()
            # measure cycle performance
            if t_0 is None:
                t_0 = time.perf_counter()
            else:
                t_1 = time.perf_counter()
                print('Cycle {}: {:.4f} sec'.format(i, t_1 - t_0))
                # print(''.join(['-' for i in range(30)]))
                t_0 = t_1
            # update cycle
            i += 1

            # refresh browser
            self.driver.refresh()

            # attempt to retrieve shifts_list, else repeat loop
            t0 = time.perf_counter()
            shifts_list = WebDriverWait(WebDriverWait(self.driver, self.max_wait_time).until(
                EC.presence_of_element_located((
                        By.ID,
                        'schedule-app'
                    ))
            ), self.max_wait_time).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    './/div[@class="find-shifts-page"]/div[2]/div[1]/div[@class="atoz-viewShift"]/div[@class="single-day-shifts-container"]/div[@class="single-day-shifts"]/div[2]'
                ))
            )
            print('list element {}: {:.4f} sec'.format(i, time.perf_counter() - t0)) # measure list element speed

            # DEBUG: test javascript ready state
            # t0 = time.perf_counter()
            # driver = self.driver
            # WebDriverWait(driver, 5).until(lambda driver: driver.execute_script("return document.readyState") == 'complete')
            # print('website ready state {}: {:.4f} sec'.format(i, time.perf_counter() - t0)) # measure website ready state speed

            # wait for website to load content fully, search blocks, and repeat
            t0 = time.perf_counter()
            endpoint = datetime.now() + timedelta(seconds = self.wait_time)
            while datetime.now() < endpoint:
                if not str(shifts_list.get_attribute('class')) == 'shifts-list':
                    empty = True
                else:
                    empty = False
                    break
            # if not str(shifts_list.get_attribute('class')) == 'shifts-list':
            #     empty = True
            # else:
            #     empty = False
            print('website load {}: {:.4f} sec'.format(i, time.perf_counter() - t0)) # measure website loading speed
            if empty:
                continue

            # get shift blocks
            t0 = time.perf_counter()
            blocks = WebDriverWait(shifts_list, 5).until(
                EC.presence_of_all_elements_located((
                    By.XPATH,
                    './/ul/li'
                ))
            )
            print('blocks {}: {:.4f} sec'.format(i, time.perf_counter() - t0)) # measure blocks speed

            # linear search blocks
            for start, end in self.priority_list:
                shift_string = self.backend.get_shift_string(start, end)
                print('Target:', shift_string)
                for block in blocks:
                    # extract shift_time
                    shift_time = WebDriverWait(block, 3).until(
                        EC.presence_of_element_located((
                            By.XPATH,
                            './/div/div[@data-testid="atoz-card"]/div[@data-test-component="StencilReactCard"]/div[@class="header"]/h4[@data-testid="card-title"]/div[@data-testid="atoz-shiftCard-time-range"]'
                        ))
                    )
                    print(shift_time.text)
                    # match shift_time
                    if shift_time.text == shift_string:
                        print('match found')
                        # locate and click add button
                        if self.activation:
                            add = WebDriverWait(block, 3).until(
                                EC.presence_of_element_located((
                                    By.XPATH,
                                    './/div/div[@data-testid="atoz-card"]/div[@data-test-component="StencilReactCard"]/div[@data-testid="card-action"]/button'
                                ))
                            )
                            self.driver.execute_script("arguments[0].click();", add)
                            print('add button clicked')
                            time.sleep(10)
                        self.continue_loop = False
                        self.final_shift_selection = shift_string
                        break
                if not self.continue_loop:
                    break
