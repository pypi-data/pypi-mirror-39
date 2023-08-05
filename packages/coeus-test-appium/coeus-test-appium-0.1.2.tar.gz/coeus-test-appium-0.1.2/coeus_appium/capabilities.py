
def get_capabilities(platform):
    if platform is "ios":
        return get_ios_capabilities()
    elif platform is "android":
        return get_android_capabilities()
    else:
        raise ValueError("Unexpected platform passed!")


def get_android_capabilities():
    caps = {
        'platformName': 'Android',
        'deviceName': 'Android Emulator',
        'autoGrantPermissions': 'true',
        'automationName': 'UIAutomator2',
        'newCommandTimeout': 120,
        'fullReset': 'false',
    }

    return caps


def get_ios_capabilities():
    caps = {
        'platformName': 'iOS',
        'platformVersion': '10.3.2',
        'deviceName': 'device',
        'autoGrantPermissions': 'true',
        'automationName': 'XCUITest',
        'newCommandTimeout': 60,
        'fullReset': 'true',
        'showXcodeLog': 'true'
    }

    return caps
