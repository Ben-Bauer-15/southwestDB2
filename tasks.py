import os
import sys
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DB2.settings")

while True:
    print('running a periodic task')
    time.sleep(10)