from appium import webdriver

DEFAULT_TAP_DURATION = 1
DEFAULT_SWIPE_DURATION = 1
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 4723


class AppiumDriver:
    driver = None
    capabilities = None

    def connect(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.driver = webdriver.Remote('http://{0}:{1}/wd/hub'.format(host, port), self.capabilities)

    def stop(self):
        self.driver.quit()

    def tap(self, x, y, tap_duration=DEFAULT_TAP_DURATION):
        self.driver.tap([[x, y]], tap_duration)

    def swipe(self, start_x, start_y, end_x, end_y, swipe_duration=DEFAULT_SWIPE_DURATION):
        self.driver.swipe(start_x, start_y, end_x, end_y, swipe_duration)

    def press_key(self, keycode):
        self.driver.press_keycode(keycode)

    def setup_android_simulator(self):
        self.capabilities = {
            'platformName': 'Android',
            'deviceName': 'Android Emulator',
            'autoGrantPermissions': 'true',
            'automationName': 'UIAutomator2',
            'newCommandTimeout': 60,
            'fullReset': 'true'
        }

    def setup_android_device(self, device_name="device"):
        self.capabilities = {
            'platformName': 'Android',
            'deviceName': device_name,
            'autoGrantPermissions': 'true',
            'automationName': 'UIAutomator2',
            'newCommandTimeout': 60,
            'fullReset': 'true'
        }

    def setup_ios_device(self, device_name="device"):
        self.capabilities = {
            'platformName': 'iOS',
            'deviceName': device_name,
            'autoGrantPermissions': 'true',
            'automationName': 'XCUITest',
            'newCommandTimeout': 60,
            'fullReset': 'true'
        }

    def setup_iphone_simulator(self):
        self.capabilities = {
            'platformName': 'iOS',
            'deviceName': 'iPhone Simulator',
            'autoGrantPermissions': 'true',
            'automationName': 'XCUITest',
            'newCommandTimeout': 60,
            'fullReset': 'true'
        }

    def setup_ipad_simulator(self):
        self.capabilities = {
            'platformName': 'iOS',
            'deviceName': 'iPad Simulator',
            'autoGrantPermissions': 'true',
            'automationName': 'XCUITest',
            'newCommandTimeout': 60,
            'fullReset': 'true'
        }