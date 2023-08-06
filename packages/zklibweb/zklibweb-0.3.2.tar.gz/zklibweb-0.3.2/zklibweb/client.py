import requests
import os
import time
import sys

from datetime import datetime as dt

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, WebDriverException, SessionNotCreatedException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from .domain import Maquine
from .utils import raw_data
from .exceptions import ZklibWebNetworkException, ZklibWebFirefoxNotFoundException


class ZkMaquine:
    def __init__(self, maquine: Maquine, headless=True, firefox_path='firefox'):
        self._maquine = maquine
        try:
            if headless:
                os.environ['MOZ_HEADLESS'] = '1'
                binary = FirefoxBinary(firefox_path, log_file=sys.stdout)
                binary.add_command_line_options('--headless')
                self._driver = webdriver.Firefox(firefox_binary=binary)
            else:
                self._driver = webdriver.Firefox()
            self._requests = requests
            self._is_login = False
        except SessionNotCreatedException as ex:
            raise ZklibWebFirefoxNotFoundException(ex.msg)

    def login(self, timeout=1):
        """
        Login with the creedencial to maquine

        Keyword Arguments:
            timeout {int} -- Time fot wait to login method (default: {1})

        Raises:
            ZklibWebNetworkException -- When there's a problem with the network

        Returns:
            bool -- Truen en case the login was success
        """

        try:
            self._driver.get(self._maquine.get_host())
            username_input = self._driver.find_element_by_name('username')
            password_input = self._driver.find_element_by_name('userpwd')
            username_input.send_keys(self._maquine.username)
            password_input.send_keys(self._maquine.password)
            password_input.send_keys(Keys.ENTER)
            time.sleep(timeout)
            alert = self._driver.switch_to.alert
            alert.accept()
        except NoAlertPresentException as ex:
            self._is_login = True
        except WebDriverException as ex:
            raise ZklibWebNetworkException(ex.msg)
        return self._is_login

    def get_uids(self):
        """ Return unique codes for all users registed

        Raises:
            ValueError -- Then the client isn't login

        Returns:
            List -- List with all codes
        """

        if not self._is_login:
            raise ValueError('You must call login method first')
        self._driver.get(self._maquine.get_url_for_uids())
        form = self._driver.find_element_by_name('mainform')
        uids = []
        for i in form.find_elements(By.XPATH, '//input[@type=\'checkbox\']'):
            uids.append(i.get_property('value'))
        return uids

    def get_data(self, start_date: dt, end_date: dt):
        """
        Return attendance data from maquine

        Arguments:
            start_date {datetime} -- Start date
            end_date {datetime} -- End date

        Returns:
            List -- All attendance information
        """

        data = self._requests.post(self._maquine.get_url_for_download(), data={
            'sdate': start_date.strftime('%Y-%m-%d'),
            'edate': end_date.strftime('%Y-%m-%d'),
            'period': 0,
            'uid': self.get_uids()
        })
        return raw_data(data.text)

    def close(self):
        """
        Close the client
        """
        self._driver.close()
        self._driver.quit()
        time.sleep(1)
        self._is_login = False
