Automated Desktop App Testing with Appium
This repository contains automated tests for mobile applications using Appium. The tests are designed to run on a macOS environment and utilize the Appium framework, mac2 driver for Appium, Allure for reporting, Python, and pytest.

Prerequisites
Before running the tests, make sure you have the following software installed on your machine:
```
Appium 2.4.1
Appium mac2 driver version 1.10.2
Allure 2.26.0
Python 3.11.0
macOS Sonoma Version 14.3 (23D56)
```


Installation
To set up the required dependencies, follow these steps:

Install Appium:


```bash
npm install -g appium@2.4.1
Install mac2 driver for Appium:
```


```bash
brew install allure
```


```bash
pip install -r requirements.txt
```

# Install pytest and other dependencies from requirements.txt

Running Tests
Start Appium:
```bash
appium
```

Run the tests:

```bash
python -m pytest
```

This command will execute the automated tests.

After the tests have finished, generate and serve Allure report:

```bash
allure serve
```

Open the generated URL in your browser to view the detailed test report.

Here is the sample report link generated by executing this test suite: 

Please make sure that your mac configured for testing Here is the link for XCode: 

Adjust the capabilities in the test scripts as needed based on your setup.