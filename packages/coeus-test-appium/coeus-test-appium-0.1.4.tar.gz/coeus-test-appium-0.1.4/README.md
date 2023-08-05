# Coeus-Appium-Bindings

[pypi-build-status]: https://img.shields.io/pypi/v/coeus-test-appium.svg
[travis-ci-status]: https://img.shields.io/travis/AgeOfLearning/coeus-appium-bindings.svg

[![pypi][pypi-build-status]](https://pypi.python.org/pypi/coeus-test-appium)
[![travis][travis-ci-status]](https://travis-ci.org/AgeOfLearning/coeus-appium-bindings)

## About
A set of wrappers to simplify the setup, and usage of appium calls to tap, swip, and send key events. 

## Setup
Simply install the requirement into your package.

```python
pip install coeus-test-appium
```

## AppiumDriver
Utilize the AppiumDriver class to create a connection to the server.

```python
driver = AppiumDriver.AppiumDriver("ios" | "android")
# add additional capabilities...
driver.capabilities['app'] = "/my/Path/to/apk"
driver.connect()

# send commands to device...
driver.tap(23, 400)
driver.swipe(23, 400, 100, 400)
```