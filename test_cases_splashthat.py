from splash_test import SplashFramework
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import sys

start_page = "https://www.splashthat.com"
user = "qacandidate@splashthat.com"
pwd = "testingislife"


class TestCases:

    st = SplashFramework()

    def test_login(self, user, pwd):
        self.st(user, pwd)
        assert True

    def test_failed_login(self):
        assert True

