# 基于Django的face recognition 智能人脸识别监控系统

### 项目文件完整，理论上只要配置好环境即可运行(Windows 10 21h2)

#### 介绍
毕业设计，基于人脸识别的智能监控，致力于打造一个面向有小规模监控需求的用户的，低成本的，智能识别监控系统。

#### 硬件环境
CPU: i5-8300h;
GPU: GTX1060-6G
MEM: 16G
摄像头：本机自带 + 海康威视DS-E12 + 手机摄像头

#### 环境和主要依赖包
python 3.6，
face_recogition，
OpenCV，
pyzbar，
Django 3.2，
cuda 11.6（若不用GPU加速，则无需安装）
其他的依赖包按照他报错提示用最新版本的就行

#### 安装教程

1.  参考face_recognition库的安装教程：
> https://github.com/ageitgey/face_recognition/blob/master/README_Simplified_Chinese.md

2.  如果使用CPU版本的dlib直接用pip安装即可，省略以下步骤，若要开启GPU加速，请安装GPU版本的dlib，参考：
> https://blog.csdn.net/weixin_42568366/article/details/116864093

3.  在编译dlib时出现Could not load library cudnn_cnn_infer64_8.dll. Error code 126
    可能是因为没有安装zlib，可以在此下载安装
> http://www.winimage.com/zLibDll/zlib123dllx64.zip

#### 使用说明

1.  pycharm可以直接打开（导入为Django项目）
2.  若使用命令行运行，请在你安装相关依赖包的python环境下，cd到项目根目录，执行

```
python manage.py runserver
```

3.  默认摄像头选择以及主要功能代码详见views.py
4.  手机上安装“IP摄像头”这个APP，然后将它提供的IP地址复制到views.py中对应的变量处，即可使用手机摄像头