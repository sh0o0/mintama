import time
import random

from django.test import tag

from .base_tests import BaseTestWeb


@tag('web')
class TestLoginAndSignup(BaseTestWeb):

    @property
    def url(self):
        return self.base_url + 'login-or-signup/'

    def test_login(self):
        self.selenium.get(self.url)

        username_input = self.selenium.find_element_by_id('username')
        username_input.send_keys(self.username)
        password_input = self.selenium.find_element_by_id('password')
        password_input.send_keys(self.password)
        self.selenium.find_element_by_id('login').click()
        time.sleep(3)

        self.assertEqual('みんたま / {}'.format(self.username), self.selenium.title)

    def test_move_login_and_signup(self):
        self.selenium.get(self.url)

        toolber_tille = self.selenium.find_element_by_css_selector('.font-weight-bold.display-1')
        self.assertEqual(toolber_tille.text, 'Login')
        self.selenium.find_element_by_id('move-signup').click()
        time.sleep(3)

        toolber_tille = self.selenium.find_element_by_css_selector('.font-weight-bold.display-1')
        self.assertEqual(toolber_tille.text, 'Signup')
        self.selenium.find_element_by_id('move-login').click()
        time.sleep(3)

        toolber_tille = self.selenium.find_element_by_css_selector('.font-weight-bold.display-1')
        self.assertEqual(toolber_tille.text, 'Login')

    def test_signup(self):
        username = random.randrange(100000000)
        self.selenium.get(self.url)

        self.selenium.find_element_by_id('move-signup').click()
        time.sleep(3)

        username_input = self.selenium.find_element_by_id('username')
        username_input.send_keys(username)
        password_input = self.selenium.find_element_by_id('password1')
        password_input.send_keys(self.password)
        password_input = self.selenium.find_element_by_id('password2')
        password_input.send_keys(self.password)
        self.selenium.find_element_by_id('signup').click()
        time.sleep(3)

        self.assertEqual('みんたま / {}'.format(username), self.selenium.title)


# @tag('web')
# class TestWebView(BaseTestWeb):
#
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#
#         url = cls.base_url + 'login-or-signup/'
#         cls.selenium.get(url)
#
#         username_input = cls.selenium.find_element_by_id('username')
#         username_input.send_keys(cls.username)
#         password_input = cls.selenium.find_element_by_id('password')
#         password_input.send_keys(cls.password)
#         cls.selenium.find_element_by_id('login').click()
#         time.sleep(3)