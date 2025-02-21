from target import TargetType
from cv import UIMatcher
import uiautomator2 as u2
from datetime import datetime,timedelta
import time
from sendmail import mail


class Automator:
    def __init__(self, device: str, targets: dict):
        # device: 如果是 USB 连接，则为 adb devices 的返回结果；如果是模拟器，则为模拟器的控制 URL 。

        self.d = u2.connect(device)
        self.targets = targets
        self.positions = {
            1: (294, 1184),
            2: (551, 1061),
            3: (807, 961),
            4: (275, 935),
            5: (535, 810),
            6: (799, 687),
            7: (304, 681),
            8: (541, 568),
            9: (787, 447)
        }

    def start(self):
        sleep_time = 3      #两次检测之间的间隔
        no_train_counter = 0        #连续没有检测到火车的次数
        flag_start = 0
        send_mail_count = 0
        while True:
            # 判断是否出现货物。
            Screen = self.d.screenshot(format="opencv")
            self.d.click(550, 1650)


            # 滑动屏幕，收割金币。
            self._swipe()
            flag_start += 1
            print("收金币次数：",flag_start)
            # 设置收五次金币就检测一次火车
            if flag_start == 5 :
                flag_start = 0
                if UIMatcher.Detect_signal_object(Screen, 'Train.jpg'):
                    screen = self.d.screenshot(format="opencv")
                    for target in TargetType:
                        self._match_target(target, screen)
                        print('检查有无漏网之鱼')
                    # time.sleep(1)
                    # 关闭家国梦
                    # screen = self.d.screenshot(format="opencv")
                    # if UIMatcher.Detect_signal_object(Screen, 'Train.jpg'):
                    print("重启家国梦，wait 10s")
                    self.d.app_stop("com.tencent.jgm")
                    self.d.app_start("com.tencent.jgm")
                    time.sleep(12)
                    # self.d.adb_shell("adb shell am force-stop com.tencent.jgm")
                    # print('重启家国梦')
                    # self.d.adb_shell("adb shell am start -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -n com.tencent.jgm/com.tencent.jgm.MainActivity")
                    # time.sleep(5)
                else:
                    print("继续")
                    # no_train_counter = 0
            train_jiance = 0
            if UIMatcher.Detect_signal_object(Screen, 'Train.jpg'):
                train_jiance += 1
                print('火车来了！')
                no_train_counter = 0
                success_counter = 0
                if train_jiance == 0:
                    time.sleep(2)       #第一次检测确保火车停了下来
                screen = self.d.screenshot(format="opencv")
                for target in TargetType:
                    if success_counter > 2:
                        print('成功找到3个货物，提前结束！')
                        break
                    if self._match_target(target,screen):
                        success_counter += 1
            else:
                no_train_counter += 1
                # 连续20次没检测到火车 说明火车跑完了
                # 这里整个else可以不要 我是为了发邮件提醒自己 换建筑了
                print("无火车次数：",no_train_counter)
                if no_train_counter >= 20:
                    print(f'连续{no_train_counter*sleep_time}s没有检测到火车,今日火车发货over！报告老大')
                    send_mail_count += 1
                    # 发送3次邮件提醒
                    if send_mail_count <= 3:
                        if mail(ret=True):
                            print("发送邮件成功")
            #
    # 这个暂时没用 容易跑死
    def upgrade_building(self,building_id,building_id2):
        flag = 0
        building_count1 = 0
        building_count2 = 0
        while True:
            self._swipe()
            flag = flag + 1
            print(f"执行{flag}次")
            if flag == 15:
                # 右侧进入升级
                self.d.click(952, 1132)
                time.sleep(1)
                if building_count1 == 3:
                    sx, sy = self._get_position(building_id2)
                    building_count1 = 0
                    building_count2 += 1
                else:
                    sx, sy = self._get_position(building_id)
                    building_count1 += 1
                self.d.click(sx, sy)
                time.sleep(1)
                # 升级
                self.d.click(870,1741)
                # self.d.click(870,1741)
                print(f"升级成功:次升级建筑{building_count2}，主升{building_count1}")
                time.sleep(1)
                self.d.click(952, 1132)
                time.sleep(1)
                self.d.click(1023,1635)
                self.d.click(1023,1635)
                time.sleep(0.5)
                flag = 0


    def _swipe(self):
        # 滑动屏幕，收割金币。
        for i in range(3):
            # 横向滑动，共 3 次。
            sx, sy = self._get_position(i * 3 + 1)
            ex, ey = self._get_position(i * 3 + 3)
            self.d.swipe(sx, sy, ex, ey)

    def _get_position(self,key):
        # 获取指定建筑的屏幕位置。
        return self.positions.get(key)

    def _get_target_position(self, target: TargetType):
        # 获取货物要移动到的屏幕位置。
        return self._get_position(self.targets.get(target))

    def _match_target(self, target: TargetType,screen):
        # 探测货物，并搬运货物。

        result = UIMatcher.match(screen, target)
        if result is not None:
            sx, sy = result
            # 获取货物目的地的屏幕位置。
            ex, ey = self._get_target_position(target)

            # 搬运货物。
            for j in range(4):
                self.d.swipe(sx, sy, ex, ey)
            return True
        return False


