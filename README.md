# 高效家国梦自动收割脚本

> 这是基于 OpenCV 模板匹配的《家国梦》游戏自动化脚本。

> （这个貌似只能本地用了）建议与[家国梦最佳建筑摆放计算](https://github.com/SQRPI/JiaGuoMeng)一起使用

> 墙裂推荐（可以在线）与[家国梦最佳建筑摆放计算](https://lintx.github.io/jgm-calculator/index.html)一起使用
牛掰的地方自己去瞧吧

## 安装与运行

```bash
# 安装依赖
python -m pip install uiautomator2 opencv-python

# adb 连接
# 使用 MuMu 模拟器，确保屏幕大小为 1920（长） * 1080（宽）
adb connect 127.0.0.1:7555

# 获取 device 名称,并填写至 main.py,如果用的是MuMU（推荐）就忽略这一步
adb devices

# 在已完成 adb 连接后，在手机安装 ATX 应用
python -m uiautomator2 init

# 打开 ATX ，点击“启动 UIAutomator”选项，确保 UIAutomator 是运行的。

# 进入游戏页面，启动自动脚本。
python main.py
```
## 自定义
请在target.py和main.py中根据自己的实际情况修改货物种类和建筑物位置，如需添加新的货物类型请再1920*1080分辨率下的MuMu中截图并添加。



##自己做的diy
> 增加了自动收橙色建筑货物，并自动重启，赶走火车

> adb连接不上的参考这个“https://www.jianshu.com/p/3302ff6a3920”
> 我的建筑摆放图在assets里面

> 容易出现报错的情况
```1.src\loadsave.cpp:725: error:cv2.error: OpenCV(4.0.0) C:\projects\opencv-python\opencv\modules\imgcodecs\```
打开 ATX ，点击“启动 UIAutomator”选项，确保 UIAutomator 是运行的
'''如果ATX打开UIAutomator还是无法启动'''命令行进入模拟器的bin文件夹python -m uiautomator2 init
其他错误的话根据打印信息自己调试把