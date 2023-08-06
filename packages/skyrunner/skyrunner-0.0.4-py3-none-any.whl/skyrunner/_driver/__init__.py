from selenium.webdriver import DesiredCapabilities, ChromeOptions, FirefoxOptions, FirefoxProfile
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.proxy import *
from selenium import webdriver
from base64 import b64encode

from .._enums.supported_browser import SupportedBrowser
from .._enums.supported_driver import SupportedDriver


class Driver:
    def __init__(self, config):
        self.config = config
        self.driver = self.__setup()

    def __setup(self):
        if self.config.browser not in SupportedBrowser.list():
            raise ValueError("Unsupported driver {0}".format(self.config.browser))

        options = self.__options()
        proxy = self.__proxy()
        capabilities = self.__capabilities()
        proxy.add_to_capabilities(capabilities)

        if hasattr(object, 'remote'):
            return self.__remote(options, proxy, capabilities)
        elif self.config.name == SupportedDriver.WEBDRIVER.value:
            return self.__webdriver(options, proxy, capabilities)

    def __remote(self, options, proxy, capabilities):
        if self.config.browser == SupportedBrowser.FIREFOX.value:
            return webdriver.Remote(
                command_executor=self.config.command_executor,
                desired_capabilities=capabilities,
                options=options,
                proxy=proxy
            )
        elif self.config.browser == SupportedBrowser.CHROME.value:
            return webdriver.Remote(
                command_executor=self.config.command_executor,
                desired_capabilities=capabilities,
                options=options
            )

    def __webdriver(self, options, proxy, capabilities):
        if self.config.browser == SupportedBrowser.FIREFOX.value:
            return webdriver.Firefox(firefox_options=options, desired_capabilities=capabilities)
        elif self.config.browser == SupportedBrowser.CHROME.value:
            return webdriver.Chrome(chrome_options=options, desired_capabilities=capabilities)

    def __capabilities(self):
        if self.config.browser == SupportedBrowser.FIREFOX.value:
            return webdriver.DesiredCapabilities.FIREFOX
        elif self.config.browser == SupportedBrowser.CHROME.value:
            return webdriver.DesiredCapabilities.CHROME

    def __options(self):
        if not hasattr(self.config, 'options'):
            return None

        options = None
        if self.config.browser == SupportedBrowser.FIREFOX.value:
            options = FirefoxOptions()
        elif self.config.browser == SupportedBrowser.CHROME.value:
            options = ChromeOptions()
        options.add_argument(self.config.options)

        return options

    def __profile(self):
        if not hasattr(self.config, 'proxy') and not self.config.browser == SupportedBrowser.FIREFOX.value:
            return None

        profile = FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", self.config.proxy.host)
        profile.set_preference("network.proxy.http_port", self.config.proxy.port)
        profile.set_preference("network.proxy.ssl", self.config.proxy.host)
        profile.set_preference("network.proxy.ssl_port", self.config.proxy.port)

        credencials = "{}:{}".format(self.config.proxy.username, self.config.proxy.password)
        credencials = b64encode(credencials.encode('ascii')).decode('utf-8')
        profile.set_preference("extensions.closeproxyauth.authtoken", credencials)

        return profile

    def __proxy(self):
        if not hasattr(self.config, 'proxy'):
            return None

        PROXY = "{}:{}".format(self.config.proxy.host, self.config.proxy.port)

        proxy = Proxy()
        proxy.http_proxy = PROXY
        proxy.ftp_proxy = PROXY
        proxy.sslProxy = PROXY
        proxy.no_proxy = self.config.proxy.no_proxy
        proxy.proxy_type = ProxyType.MANUAL
        proxy.autodetect = False

        return proxy
