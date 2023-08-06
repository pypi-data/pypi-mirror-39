import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import selsunpool
from selsunpool import (
    SeleniumPoolExecutor,
    SeleniumPoolException,
    selenium_job,
    WebDriver,
    config
)