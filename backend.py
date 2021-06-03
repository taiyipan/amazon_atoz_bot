from datetime import date
from datetime import timedelta
from datetime import datetime
from credential import Credential
import platform

# perform backend calculations to support frontend interface programs
class Backend:
    def __init__(self):
        self.password_threshold = 3 # days prior
        self.test = False # test mode toggle
        self.end_time = datetime.now() + timedelta(minutes = self.search_time(self.base_time())) # calculate end program time
        self.credential = Credential()
        print('Backend initialized')

    def base_time(self) -> int:
        if self.test:
            return 1
        else:
            return 5

    def search_time(self, base: int) -> int: # minutes
        if platform.node() == 'Galatea': # 6:13pm-6:18pm
            return base
        elif platform.node() == 'eternal': # 6:12pm-6:18pm
            return base + 1
        elif platform.node() == 'raspberrypi': # 6:10pm-6:18pm
            return base + 3
        else:
            return None

    # validate whether program should continue execution
    def validate_duration(self) -> bool:
        if datetime.now() < self.end_time:
            return True # continue execution
        else:
            return False # terminate program

    # variation: Sunday -> Sunday
    # def calculate_shift_date(self):
    #     today = date.today()
    #     weekday = today.weekday()
    #     if weekday == 0 or weekday == 1 or weekday == 2:
    #         shift_date = today + timedelta(days = 3)
    #     elif weekday == 3 or weekday == 4:
    #         shift_date = today + timedelta(days = 4)
    #     elif weekday == 6:
    #         shift_date = today + timedelta(days = 7)
    #     else: # if today is Saturday (weekday = 5)
    #         shift_date = None
    #     return shift_date

    # variation: Thursday -> Sunday, Friday -> Tuesday
    def calculate_shift_date(self):
        today = date.today()
        weekday = today.weekday()
        if weekday == 0 or weekday == 1 or weekday == 2 or weekday == 3 or weekday == 6:
            shift_date = today + timedelta(days = 3)
        elif weekday == 4:
            shift_date = today + timedelta(days = 4)
        else: # if today is Saturday (weekday = 5)
            shift_date = None
        return shift_date

    # def calculate_shift_date(self):
    #     today = date.today()
    #     weekday = today.weekday()
    #     if weekday == 0 or weekday == 1 or weekday == 2 or weekday == 6:
    #         shift_date = today + timedelta(days = 3)
    #     elif weekday == 3 or weekday == 4:
    #         shift_date = today + timedelta(days = 4)
    #     else: # if today is Saturday (weekday = 5)
    #         shift_date = None
    #     return shift_date

    # <-- Debug function -->
    # def calculate_shift_date(self):
    #     today = date.today()
    #     weekday = today.weekday()
    #     if weekday == 0 or weekday == 1 or weekday == 2 or weekday == 6:
    #         shift_date = today + timedelta(days = 2)
    #     elif weekday == 3 or weekday == 4:
    #         shift_date = today + timedelta(days = 2)
    #     else: # if today is Saturday (weekday = 5)
    #         shift_date = None
    #     return shift_date

    def get_shift_date(self) -> str:
        return str(self.calculate_shift_date())

    def get_shift_weekday(self) -> str:
        return self.calculate_shift_date().strftime('%A')

    # build shift list
    def build_priority_list(self, raw_input: list) -> list:
        input = raw_input[1:]
        assert len(input) % 2 == 0 # make sure it's even length
        priority_list = list()
        for i in range(len(input)):
            if i % 2 == 0: # even
                start = input[i]
            else: # odd
                end = input[i]
                priority_list.append((start, end)) # add tuple
        return priority_list

    # input strings format: %H:%M
    def get_shift_string(self, start_string: str, end_string: str) -> str:
        # convert input strings into datetime objects
        start = datetime.strptime(start_string, '%H:%M')
        end = datetime.strptime(end_string, '%H:%M')
        # calculate timedelta
        delta = end - start
        # calculate minutes
        minutes = delta.total_seconds() // 60
        # convert to hours and minutes
        hours = int(minutes // 60)
        minutes = int(minutes % 60)
        # return formatted shift string
        if minutes > 0:
            return '{}-{} ({}hrs {}mins)'.format(start.strftime('%-I:%M%P'), end.strftime('%-I:%M%P'), hours, minutes)
        else:
            return '{}-{} ({}hrs)'.format(start.strftime('%-I:%M%P'), end.strftime('%-I:%M%P'), hours)

    # determine if the password is expiring soon; True is valid, False is expiring soon
    def check_password(self) -> bool:
        expiration_date = datetime.strptime(self.credential.password_expiration_date(), '%Y-%m-%d')
        if datetime.now() < (expiration_date + timedelta(days = -self.password_threshold)):
            return True
        else:
            return False
