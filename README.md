## Automated Desktop App Testing with Appium
This repository contains automated tests for mobile applications using Appium. The tests are designed to run on a macOS environment and utilize the Appium framework, mac2 driver for Appium, Allure for reporting, Python, and pytest.

Due to the mac retina display, original pixel size cannot be able to compared with real pixel. For example, when screenshot taken on 200x200 it becomes 500x500 so base_images 1920 x 1080 however whenever I try to take screenshot using appium or manually image size getting bigger and bigger. For comparison, resize can be made according to the base_image however, there will be loss between pixel values and it will be fail on pixelmatch. 

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
appium driver install mac2
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
Here is the link that showing quick demo: https://youtu.be/QjH8ORG5mRM 

Open the generated URL in your browser to view the detailed test report.

Please make sure that your mac configured for testing Here is the link for XCode: https://github.com/appium/appium-mac2-driver?tab=readme-ov-file#requirements

Adjust the capabilities in the test scripts as needed based on your setup.

## Notes
- Screenshoted images resize since mac retina causing doubling or tribling the image width and height 
- 2 different method used in tests, pixelmatch and imagehash 
