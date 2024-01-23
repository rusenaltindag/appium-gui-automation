# Python3 + PyTest
import pytest
import os
from PIL import Image

from pixelmatch.contrib.PIL import pixelmatch

from appium import webdriver

# Options are available in Python client since v2.6.0
from appium.options.mac import Mac2Options
from appium.webdriver.common.appiumby import AppiumBy

import allure
from allure import attachment_type


@pytest.fixture(scope="session")
def driver(request):
    options = Mac2Options()
    options.bundle_id = "com.apple.Preview"
    drv = webdriver.Remote("http://127.0.0.1:4723", options=options)
    # None if os.path.exists("output") else os.mkdir("output")

    # Cleanup step: Delete all created images in the output directory at the end
    # def cleanup():
    #     for file_name in os.listdir(os.getcwd()):
    #         if file_name.endswith(".png") or file_name.endswith(".jpg"):
    #             os.remove(os.path.join(file_name))

    # # Register the cleanup function
    # request.addfinalizer(cleanup)
    yield drv
    drv.quit()


@pytest.fixture
def test_environment_setup(request):
    # Ensure output directory exists
    pass


# Common setup and teardown logic for each test
def setup_method(self, method):
    # Add setup logic here, if needed
    print("set up")


def teardown_method(self, method):
    # Add teardown logic here, if needed
    print("tear down up")


@allure.title(
    "Start any Image Editing application for desktop that can import & export images with different formats (ex. Paint)"
)
@allure.description("Open Preview App on MAC")
def test_open_image_editor(driver):
    pass


@allure.title("Import Image: IMAGE_1")
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
    image_path = os.path.join(os.getcwd(), "IMAGE_1.png")
    driver.execute_script(
        "macos:keys",
        {"keys": [*image_path, "XCUIKeyboardKeyEnter", "XCUIKeyboardKeyEnter"]},
    )
    driver.find_element(
        by=AppiumBy.CLASS_NAME, value="XCUIElementTypeImage"
    ).screenshot("IMAGE_1_preview_ss_class_name.png")


@allure.title(
    "Verify with image comparison that the imported Image looks correctly in the Image Editor"
)
def test_preview_of_image_with_original(driver):
    original_img = Image.open("IMAGE_1.png")
    preview_img = Image.open("IMAGE_1_preview_ss_class_name.png")

    preview_img = preview_img.resize(original_img.size)
    img_diff = Image.new("RGBA", original_img.size)
    mismatch = pixelmatch(original_img, preview_img, img_diff)
    img_diff.save("original_vs_preview_diff.png")
    allure.attach.file(
        "original_vs_preview_diff.png",
        name="Differences between Preview and Original IMG",
        attachment_type=attachment_type.PNG,
    )
    assert mismatch == 0


@allure.title("Export the Image in JPG format to a local drive")
def test_export_func(driver):
    driver.find_element(
        by=AppiumBy.IOS_PREDICATE, value="elementType == 56 AND title == 'File'"
    ).click()
    driver.find_element(
        by=AppiumBy.IOS_PREDICATE, value="elementType == 54 AND title == 'Export…'"
    ).click()

    # Select Name Section
    driver.find_element(
        by=AppiumBy.IOS_PREDICATE,
        value="elementType == 49 AND identifier == 'saveAsNameTextField'",
    ).click()

    driver.find_element(
        by=AppiumBy.IOS_PREDICATE,
        value="elementType == 14 AND identifier == '_NS:120'",
    ).click()
    driver.find_element(
        by=AppiumBy.IOS_PREDICATE, value="elementType == 54 AND title == 'JPEG'"
    ).click()
    driver.find_element(
        by=AppiumBy.IOS_PREDICATE, value="elementType == 9 AND identifier == 'OKButton'"
    ).click()


@allure.title("Verify that the exported image exists")
def test_verify_that_the_exported_image_exists(driver):
    assert os.path.exists("IMAGE_1.jpg")


@allure.title(
    "Verify with image comparison whether the exported image is equal to IMAGE_2"
)
def test_verify_with_image_comparison_whether_the_exported_image_is_equal_to_IMAGE_2(
    driver,
):
    img1 = Image.open("IMAGE_1.jpg")
    img2 = Image.open("IMAGE_2.png")
    img_diff = Image.new("RGBA", img1.size)
    mismatch = pixelmatch(img1, img2, img_diff)
    img_diff.save("IMAGE_1_diff.png")
    allure.attach.file(
        "IMAGE_1_diff.png",
        name="Differences between IMG1 and IMG2",
        attachment_type=attachment_type.PNG,
    )
    assert mismatch == 0
