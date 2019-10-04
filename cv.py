from target import TargetType
import cv2

#每次进行模板匹配时尝试的次数
Detect_num = 1

class UIMatcher:
    @staticmethod
    def match(screen, target: TargetType):
        # 获取对应货物的图片。
        # 有个要点：通过截屏制作货物图片时，请在快照为实际大小的模式下截屏。
        template = cv2.imread(target.value)
        print(f'正在寻找{target.value[8:-4]}')
        # 获取货物图片的宽高。
        th, tw = template.shape[:2]

        # 调用 OpenCV 模板匹配。
        for i in range(Detect_num):
            res = cv2.matchTemplate(screen, template, cv2.TM_SQDIFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            # 阈值判断。
            if min_val <= 0.15:
                # 矩形左上角的位置。
                tl = min_loc
                # 这里，我随机加入了数字（15），用于补偿匹配值和真实位置的差异。
                print('找到了，开始供货！')
                return tl[0] + tw / 2 + 25, tl[1] + th / 2 + 25
        print('没找到，下一个！')
        return None


    @staticmethod
    def Detect_signal_object(screen, object_path):
        template = cv2.imread(object_path)

        # 调用 OpenCV 模板匹配。
        for i in range(Detect_num):
            res = cv2.matchTemplate(screen, template, cv2.TM_SQDIFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            # 阈值判断。
            if min_val <= 0.15:
                return True
        return False



    @staticmethod
    def read(filepath: str):
        return cv2.imread(filepath)
