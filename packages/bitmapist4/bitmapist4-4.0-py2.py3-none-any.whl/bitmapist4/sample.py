import math
import datetime
import random
import bitmapist4

USERS = 50
DAYS = 60
MAX_STICKYNESS = 8
EVENTS = ['task:added', 'task:completed', 'task:deleted',
          'project:added', 'project:deleted', 'note:added', 'note:deleted']


def create_sample_data():
    b = bitmapist4.Bitmapist()
    start = datetime.date.today() - datetime.timedelta(DAYS)
    for uid in range(1, USERS + 1):
        with b.transaction():
            stickyness = random.randint(1, MAX_STICKYNESS)
            for d in range(DAYS):
                timestamp = start + datetime.timedelta(d + 1)
                active = False
                for event in EVENTS:
                    threshold = 1 / math.log2(2 + (float(d) / stickyness))
                    if random.random() < threshold:
                        b.mark_event(event, uid, timestamp=timestamp)
                        active = True
                if active:
                    b.mark_event('active', uid, timestamp=timestamp)
