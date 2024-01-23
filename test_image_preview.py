# Python3 + PyTest
import pytest
import os
import imagehash
from PIL import Image

from pixelmatch.contrib.PIL import pixelmatch

from appium import webdriver

# Options are available in Python client since v2.6.0
from appium.options.mac import Mac2Options
from appium.webdriver.common.appiumby import AppiumBy

import allure
from allure import attachment_type
from helper import ImageComparisonUtil, PreviewApp


@pytest.fixture(scope="session")
def driver(request):
    options = Mac2Options()
    options.bundle_id = "com.apple.Preview"
    drv = webdriver.Remote("http://127.0.0.1:4723", options=options)
    yield drv
    # for file_name in os.listdir(os.getcwd()):
    #     if file_name.endswith(".png") or file_name.endswith(".jpg"):
    #         os.remove(os.path.join(file_name))
    drv.quit()


def test_rusen(driver):
    # preview_app = PreviewApp(driver)
    # preview_app.ImportImageFromMenuBar()
    # preview_app.OpenGoToFolderWindow()
    # preview_app.EnterFullPathNameForBaseImage("IMAGE_1.png")
    # preview_app.ClickEnter()
    # preview_app.ClickEnter()
    # driver.find_element(
    #     by=AppiumBy.IOS_PREDICATE, value="elementType == 56 AND title == 'File'"
    # ).click()
    # driver.find_element(
    #     by=AppiumBy.IOS_PREDICATE, value="elementType == 54 AND title == 'Open…'"
    # ).click()
    pass


@allure.title(
    "Start any Image Editing application for desktop that can import & export images with different formats (ex. Paint)"
)
@allure.description("Open Preview App on MAC")
def test_open_image_editor(driver):
    status = driver.execute_script(
        "macos: queryAppState", {"bundleId": "com.apple.Preview"}
    )
    # https://developer.apple.com/documentation/xctest/xcuiapplicationstate?language=objc
    assert status == 4


@pytest.mark.image
@allure.title("Import Image: IMAGE_1")
def test_import_image(driver):
    preview_app = PreviewApp(driver)
    preview_app.ImportImageFromMenuBar()
    preview_app.OpenGoToFolderWindow()
    preview_app.EnterFullPathNameForBaseImage("IMAGE_1.png")
    preview_app.ClickEnter()
    preview_app.ClickEnter()
    driver.find_element(
        by=AppiumBy.CLASS_NAME, value="XCUIElementTypeImage"
    ).screenshot("IMAGE_1_preview_ss_class_name.png")


@pytest.mark.image
@allure.title(
    "Verify with image comparison that the imported Image looks correctly in the Image Editor- pixelmatch approach"
)
def test_preview_of_image_with_original_with_pixel_match(driver):
    original_img = Image.open(os.path.join(os.getcwd(), "base_images", "IMAGE_1.png"))
    preview_img = Image.open("IMAGE_1_preview_ss_class_name.png")

    img_comparison = ImageComparisonUtil(original_img, preview_img)

    assert img_comparison.compareWithPixelMatch() == 0


@allure.title(
    "Verify with image comparison that the imported Image looks correctly in the Image Editor - imagehash approach"
)
def test_preview_of_image_with_original_with_hash(driver):
    original_img = Image.open(os.path.join(os.getcwd(), "base_images", "IMAGE_1.png"))
    preview_img = Image.open("IMAGE_1_preview_ss_class_name.png")

    img_comparison = ImageComparisonUtil(original_img, preview_img)

    assert img_comparison.compareWithImageHash() == 1.0


@allure.title("Export the Image in JPG format to a local drive")
def test_export_func(driver):
    preview_app = PreviewApp(driver)
    preview_app.ExportImageFromMenuBar()
    preview_app.OpenGoToFolderWindow()
    preview_app.EnterNameForToBeExportedImage("IMAGE_1.jpg")
    preview_app.ClickEnter()
    preview_app.SelectToBeExportedImageFormat()


@allure.title("Verify that the exported image exists")
def test_verify_that_the_exported_image_exists(driver):
    assert os.path.exists("IMAGE_1.jpg")


@allure.title(
    "Verify with image comparison whether the exported image is equal to IMAGE_2 - pixelmatch"
)
def test_verify_with_image_comparison_whether_the_exported_image_is_equal_to_IMAGE_2(
    driver,
):
    img1 = Image.open("IMAGE_1.jpg")
    img2 = Image.open(os.path.join(os.getcwd(), "base_images", "IMAGE_2.png"))

    img_comparison = ImageComparisonUtil(img1, img2)
    assert img_comparison.compareWithPixelMatch() == 0


@allure.title(
    "Verify with image comparison whether the exported image is equal to IMAGE_2 - imagehash"
)
def test_verify_with_image_comparison_whether_the_exported_image_is_equal_to_IMAGE_2_image_hash(
    driver,
):
    img1 = Image.open("IMAGE_1.jpg")
    img2 = Image.open(os.path.join(os.getcwd(), "base_images", "IMAGE_2.png"))

    img_comparison = ImageComparisonUtil(img1, img2)
    assert img_comparison.compareWithImageHash() == 1.0
