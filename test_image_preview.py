# Python3 + PyTest
import pytest
import os
from PIL import Image

from pixelmatch.contrib.PIL import pixelmatch

from appium import webdriver

# Options are available in Python client since v2.6.0
from appium.options.mac import Mac2Options
from appium.webdriver.common.appiumby import AppiumBy


@pytest.fixture()
def driver():
    options = Mac2Options()
    options.bundle_id = "com.apple.Preview"
    drv = webdriver.Remote("http://127.0.0.1:4723", options=options)
    yield drv
    drv.quit()


def test_open_image_editor(driver):
    pass


def test_import_image(driver):
    driver.find_element(
        by=AppiumBy.IOS_PREDICATE, value="elementType == 56 AND title == 'File'"
    ).click()
    driver.find_element(
        by=AppiumBy.IOS_PREDICATE, value="elementType == 54 AND title == 'Open…'"
    ).click()

    flagsShift = (1 << 1) | (1 << 4)
    driver.execute_script(
        "macos: keys",
        {
            "keys": [
                {
                    "key": "g",
                    "modifierFlags": flagsShift,
                },
            ]
        },
    )
    image_path = "/Users/rusen/chaos/IMAGE_1.png"
    driver.execute_script("macos:keys", {"keys": [*image_path]})
    driver.execute_script("macos:keys", {"keys": ["XCUIKeyboardKeyEnter"]})
    driver.execute_script("macos:keys", {"keys": ["XCUIKeyboardKeyEnter"]})

    # TODO: Verify with image comparison that the imported Image looks correctly in the Image Editor

    driver.find_element(
        by=AppiumBy.IOS_PREDICATE, value="elementType == 56 AND title == 'File'"
    ).click()
    export_image = driver.find_element(
        by=AppiumBy.IOS_PREDICATE, value="elementType == 54 AND title == 'Export…'"
    )
    export_image.click()

    export_image = driver.find_element(
        by=AppiumBy.IOS_PREDICATE,
        value="elementType == 49 AND identifier == 'saveAsNameTextField'",
    )
    export_image.click()

    export_image = driver.find_element(
        by=AppiumBy.IOS_PREDICATE,
        value="elementType == 14 AND identifier == '_NS:120'",
    )
    export_image.click()
    png_image = driver.find_element(
        by=AppiumBy.IOS_PREDICATE, value="elementType == 54 AND title == 'JPEG'"
    )
    png_image.click()

    save = driver.find_element(
        by=AppiumBy.IOS_PREDICATE, value="elementType == 9 AND identifier == 'OKButton'"
    )
    save.click()


def test_verify_that_the_exported_image_exists(driver):
    assert os.path.exists("IMAGE_1.jpg")


def test_verify_with_image_comparison_whether_the_exported_image_is_equal_to_IMAGE_2(
    driver,
):
    img1 = Image.open("IMAGE_1.jpg")
    img2 = Image.open("IMAGE_2.png")

    img_diff = Image.new("RGBA", img1.size)
    mismatch = pixelmatch(img1, img2, img_diff)
    assert mismatch == 0
    img_diff.save("IMAGE_1_diff.png")