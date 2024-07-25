import cv2
import matplotlib.pyplot as plt
import numpy as np
import pyautogui


class ImageFinder:
    def __init__(self, imgopcv):
        self.imgopcv = imgopcv
        self.screen_width, self.screen_height = pyautogui.size()

    # 相对于某个坐标系的屏幕截取
    def find_image_in_screen(
            self, image_path, top_left_right_pct, bottom_left_right_pct
    ):
        try:
            # 计算截取区域的坐标
            left = int(self.screen_width * top_left_right_pct[0])
            top = int(self.screen_height * top_left_right_pct[1])
            right = int(self.screen_width * bottom_left_right_pct[0])
            bottom = int(self.screen_height * bottom_left_right_pct[1])

            # 截取屏幕图像的特定区域
            screenshot = pyautogui.screenshot(
                region=(left, top, right - left, bottom - top)
            )
            screen_np = np.array(screenshot)
            img_rgb = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
            image_path = plt.imread(image_path)
            # 读取目标图片并转换为灰度图
            template = cv2.imread(
                image_path, cv2.IMREAD_GRAYSCALE
            )  # 使用cv2.IMREAD_GRAYSCALE确保以灰度图读取
            if template is None:
                print(
                    f"Error loading image '{image_path}'. Check the file path and integrity."
                )
                return None
            w, h = template.shape[::-1]

            # 将屏幕图像转换为灰度图
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

            # 模板匹配
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

            # 设定匹配阈值
            threshold = self.imgopcv
            loc = np.where(res >= threshold)

            # 寻找最佳匹配位置
            if len(loc[0]) > 0:
                # 找到最大值的索引
                pt = np.unravel_index(
                    res.argmax(), res.shape
                )  # 使用 argmax 找到最大值的索引

                # 计算匹配区域的中心点坐标
                center_point = (
                    pt[1] + w / 2,
                    pt[0] + h / 2,
                )  # pt[1] 是列索引，pt[0] 是行索引
                return center_point
            # 如果没有找到匹配，则返回None
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    # 相对于整个屏幕的屏幕截取
    def find_image_all(self, image_path):
        try:
            # 截取屏幕图像的特定区域
            screenshot = pyautogui.screenshot()
            screen_np = np.array(screenshot)
            img_rgb = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
            # 读取目标图片并转换为灰度图
            # image_path = plt.imread(image_path)
            # image_path = f"{image_path}".encode("utf-8")
            image_path = f"{image_path}"
            print("image_path", )
            template = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
            # template = cv2.imread(
            #     np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_GRAYSCALE
            # )  # 使用cv2.IMREAD_GRAYSCALE确保以灰度图读取
            if template is None:
                print(
                    f"Error loading image '{image_path}'. Check the file path and integrity."
                )
                return None
            w, h = template.shape[::-1]

            # 将屏幕图像转换为灰度图
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

            # 模板匹配
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

            # 设定匹配阈值
            threshold = self.imgopcv
            loc = np.where(res >= threshold)

            # 寻找最佳匹配位置
            if len(loc[0]) > 0:
                # 找到最大值的索引
                pt = np.unravel_index(
                    res.argmax(), res.shape
                )  # 使用 argmax 找到最大值的索引

                # 计算匹配区域的中心点坐标
                center_point = (
                    pt[1] + w / 2,
                    pt[0] + h / 2,
                )  # pt[1] 是列索引，pt[0] 是行索引
                return center_point
            # 如果没有找到匹配，则返回None
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    # 相对于整个屏幕截取找多张图
    def find_images_all(self, image_paths):
        try:
            # 截取屏幕图像的特定区域
            screenshot = pyautogui.screenshot()
            screen_np = np.array(screenshot)
            img_rgb = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)

            # 循环遍历提供的图片路径列表
            for image_path in image_paths:
                # image_path = plt.imread(image_path)
                # 读取目标图片并转换为灰度图
                image_path = f"{image_path}"
                template = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                if template is None:
                    print(
                        f"Error loading image '{image_path}'. Check the file path and integrity."
                    )
                    continue  # 如果图片加载失败，跳过这张图片

                w, h = template.shape[::-1]  # 获取图片的宽度和高度

                # 将屏幕图像转换为灰度图
                img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

                # 模板匹配
                res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

                # 设定匹配阈值
                threshold = self.imgopcv
                loc = np.where(res >= threshold)

                # 寻找最佳匹配位置
                if len(loc[0]) > 0:
                    # 找到最大值的索引
                    pt = np.unravel_index(res.argmax(), res.shape)

                    # 计算匹配区域的中心点坐标
                    center_point = (pt[1] + w // 2, pt[0] + h // 2)
                    return center_point  # 返回第一张找到的图片的中心点坐标

            # 如果没有找到匹配，则返回None
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


# 使用示例
if __name__ == "__main__":
    finder = ImageFinder()
    target_image_path = "../images/kaishi.jpg"
    search_area_percentages = (
        (0.1, 0.1),  # 顶部 left right
        (0.9, 0.1),  # 底部 left right
    )
    result = finder.find_image_in_screen(target_image_path, search_area_percentages)
    if result is not None:
        print(f"Found image at screen coordinates: {result}")
    else:
        print("No match found.")
