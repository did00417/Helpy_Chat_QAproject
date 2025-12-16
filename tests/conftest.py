import sys
import os
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from utils.driver import get_driver

@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()