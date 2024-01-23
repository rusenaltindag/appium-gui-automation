# helpers.py

from PIL import Image
import imagehash

from pixelmatch.contrib.PIL import pixelmatch
import allure
from allure import attachment_type


class ImageComparisonUtil:
    def __init__(self, img1, img2):
        self.img1 = img1
        self.img2 = img2

    def login(self):
        # Code to perform login
        print(f"Logging in with username: {self.img1} and password: {self.img2}")

    def compareWithImageHash(self):
        img2_resized = self.img2.resize(self.img1.size)

        img1_hash = imagehash.average_hash(self.img1)
        img2_hash = imagehash.average_hash(img2_resized)

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
