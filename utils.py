from datetime import datetime, timedelta


def clamp(num: int, min_value: int, max_value: int):
    return max(min(num, max_value), min_value)


def is_in_range(num, min, max):
    return min <= num <= max


class Timer:
    def __init__(self, countdown_time):
        self.countdown_time = timedelta(seconds=countdown_time)
        self.startTime = datetime.now()
        self.done = False

    def update(self):
        self.done = self.startTime + self.countdown_time <= datetime.now()
