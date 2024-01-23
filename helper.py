# helpers.py

from PIL import Image
import imagehash

from pixelmatch.contrib.PIL import pixelmatch
import allure
from allure import attachment_type
from appium.webdriver.common.appiumby import AppiumBy
import os


class ImageComparisonUtil:
    def __init__(self, img1, img2):
        self.img1 = img1
        self.img2 = img2

    @allure.step("Compare images using imagehash library and average-hash algorithm ")
    def compareWithImageHash(self):
        self.img2 = self.img2.resize(self.img1.size)

        img1_hash = imagehash.average_hash(self.img1)
        img2_hash = imagehash.average_hash(self.img2)

        img_diff = Image.new("RGBA", self.img1.size)
        pixelmatch(self.img1, self.img2, img_diff)
        img_diff.save("img1_vs_img2_difference_with_pixel_match.png")
        allure.attach.file(
            "img1_vs_img2_difference_with_pixel_match.png",
            name="Differences between IMG1 and IMG2",
            attachment_type=attachment_type.PNG,
        )

        similarity = 1 - (img1_hash - img2_hash) / len(img1_hash.hash) ** 2

        return similarity

    @allure.step("Compare Images using classic pixelmatch")
    def compareWithPixelMatch(self):
        img_diff = Image.new("RGBA", self.img1.size)
        self.img2 = self.img2.resize(self.img1.size)
        mismatch = pixelmatch(self.img1, self.img2, img_diff)
        img_diff.save("img1_vs_img2_difference_with_pixel_match.png")
        allure.attach.file(
            "img1_vs_img2_difference_with_pixel_match.png",
            name="Differences between IMG1 and IMG2",
            attachment_type=attachment_type.PNG,
        )
        return mismatch


class IOHelper:
    def __init__(self):
        pass

    def getFullPathNameOfImage(self, image_name, parent_directory="output"):
        return os.path.join(os.getcwd, parent_directory, image_name)


class PreviewApp:
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Import Image on Menubar File > Open")
    def ImportImageFromMenuBar(self):
        self.driver.find_element(
            by=AppiumBy.IOS_PREDICATE, value="elementType == 56 AND title == 'File'"
        ).click()
        self.driver.find_element(
            by=AppiumBy.IOS_PREDICATE, value="elementType == 54 AND title == 'Open…'"
        ).click()

    @allure.step("Click to Export: File > Export")
    def ExportImageFromMenuBar(self):
        self.driver.find_element(
            by=AppiumBy.IOS_PREDICATE, value="elementType == 56 AND title == 'File'"
        ).click()
        self.driver.find_element(
            by=AppiumBy.IOS_PREDICATE, value="elementType == 54 AND title == 'Export…'"
        ).click()

    @allure.step("Going to the direct path with shortcut")
    def OpenGoToFolderWindow(self):
        flagsShift = (1 << 1) | (1 << 4)
        self.driver.execute_script(
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

    @allure.step("Type full path of Base Image")
    def EnterFullPathNameForBaseImage(self, img_name):
        image_path = os.path.join(os.getcwd(), "base_images", img_name)
        self.driver.execute_script(
            "macos:keys",
            {"keys": [*image_path]},
        )

    @allure.step("Type full path of To Be Exported Image")
    def EnterNameForToBeExportedImage(self, img_name):
        image_path = os.path.join(os.getcwd(), img_name)
        self.driver.execute_script(
            "macos:keys",
            {"keys": [*image_path]},
        )

    @allure.step("Select Exported Image Type")
    def SelectToBeExportedImageFormat(self, img_type="JPEG"):
        self.driver.find_element(
            by=AppiumBy.IOS_PREDICATE,
            value="elementType == 14 AND identifier == '_NS:120'",
        ).click()
        self.driver.find_element(
            by=AppiumBy.IOS_PREDICATE,
            value=f"elementType == 54 AND title == '{img_type}'",
        ).click()
        self.driver.find_element(
            by=AppiumBy.IOS_PREDICATE,
            value="elementType == 9 AND identifier == 'OKButton'",
        ).click()

    @allure.step("Click Enter")
    def ClickEnter(self):
        self.driver.execute_script(
            "macos:keys",
            {"keys": ["XCUIKeyboardKeyEnter"]},
        )

    @allure.step("Screenshot of what is displayed")
    def ScreenShotThePreview(self, ss_name):
        self.driver.find_element(
            by=AppiumBy.CLASS_NAME, value="XCUIElementTypeImage"
        ).screenshot(ss_name)

    @allure.step("Get the Status of Application")
    def GetAppState(self):
        # https://developer.apple.com/documentation/xctest/xcuiapplicationstate?language=objc
        return (
            "Running"
            if self.driver.execute_script(
                "macos: queryAppState", {"bundleId": "com.apple.Preview"}
            )
            == 4
            else "Not Running"
        )

    @allure.step("Delete Test Artifacts Created During Test Executions")
    def cleanCreatedScreenShots(self):
        for file_name in os.listdir(os.getcwd()):
            if file_name.endswith(".png") or file_name.endswith(".jpg"):
                os.remove(os.path.join(file_name))

    @allure.step("Quit Driver")
    def TearDown(self):
        self.driver.quit()
