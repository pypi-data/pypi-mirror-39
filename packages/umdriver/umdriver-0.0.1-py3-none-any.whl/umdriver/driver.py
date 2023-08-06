from selenium.webdriver import Chrome, Firefox, Ie, PhantomJS
from selenium.common.exceptions import TimeoutException

from umdriver.pages import LoginPage


class UMDriver(Chrome, Firefox, Ie, PhantomJS):

    def __init__(self, driver='chrome', **kwargs):
        if driver.lower() == 'chrome':
            Chrome.__init__(self, **kwargs)
        elif driver.lower() == 'ie':
            Ie.__init__(self, **kwargs)
        elif driver.lower() == 'firefox':
            Firefox.__init__(self, **kwargs)
        else:
            PhantomJS.__init__(self, **kwargs)

    def login(self, username, password):
        url = 'https://weblogin.umich.edu'
        self.get(url)
        page = LoginPage(self)
        page.username = username
        page.password = password
        assert len(page.password)
        page.submit()
