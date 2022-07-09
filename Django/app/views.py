import json
import os

import cv2
import face_recognition
from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render, redirect
from pyzbar import pyzbar as pyzbar

# 全局变量：视频源；监测到的人脸，数据集预编码
video = "http://admin:123456@192.168.136.231:8081/"  # 远程IP摄像头
# 0：本机摄像头，1：USB摄像头，video：无线摄像头（手机）
camera = cv2.VideoCapture(0)  # 默认一定使用本机摄像头
person_names = []  # 人姓名
person_face_encodings = []  # 人面部信息
detected_faces = []  # 目前画面中检测到的人脸


# 人脸数据预处理
def dataset_handle():
    # 路径格式："D:/xxx/xxx"
    img_dir = "D:/GraguateProject/Django/app/static/img/faces"
    files = os.listdir(img_dir)
    for file in files:
        if file.endswith("jpg") or file.endswith("png"):
            # 去除文件后缀类型
            name, _ = os.path.splitext(file)
            person_names.append(name)
            # 拼接图片完整路径
            img_path = os.path.join(img_dir, file)
            # 解析出已有图片的脸部信息
            img_file = face_recognition.load_image_file(img_path)
            face_encoding = face_recognition.face_encodings(img_file)[0]
            person_face_encodings.append(face_encoding)


# 基于的opencv二维码识别函数
# 很难用，又卡又不稳定
"""
def qr_code_handle(frame):
    detector = cv2.QRCodeDetector()
    # _, img = camera.read()
    data, bbox, _ = detector.detectAndDecode(frame)
    if bbox is not None:
        for i in range(len(bbox)):
            cv2.line(frame, tuple(bbox[i][0]), tuple(bbox[(i + 1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)
        if data:
            print("[+] QR Code detected, data:", data)
        # cv2.imshow("img", img)

"""


# 基于pyzbar的二维码侦测与标示
def qr_detect(image):
    barcodes = pyzbar.decode(image)
    for barcode in barcodes:
        # 提取二维码的边界框的位置
        # 画出图像中条形码的边界框
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (127, 127, 255), 2)

        # 提取二维码数据为字节对象，所以如果我们想在输出图像上
        # 画出来，就需要先将它转换成字符串
        barcodeData = barcode.data.decode("UTF8")
        barcodeType = barcode.type

        # 绘出图像上条形码的数据和条形码类型
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 0.7, (127, 127, 255), 1)
        # 向终端打印条形码数据和条形码类型
        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
    return image


# 视频帧识别函数与流生成
def gen_frames():
    # 初始化变量
    face_locations = []  # 脸部位置列表
    face_encodings = []  # 脸部编码列表
    face_names = []  # 脸的人名列表
    process_this_frame = True  # 是否识别当前帧
    # counter = interval

    while True:
        # 读取帧 ###########################################################
        ret, origin_frame = camera.read()
        # 读取失败，就退出
        if not ret:
            break

        # 二维码识别 ########################################################
        frame = qr_detect(origin_frame)

        # 人脸识别 #########################################################
        # 缩放当前帧为1/2，以提高后面的识别速度
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        # 转换BGR为RGB，方便face_recognition使用
        rgb_small_frame = small_frame[:, :, ::-1]

        # 识别处理
        if process_this_frame:
            # 获取当前帧的人脸位置、编码
            # model: cnn卷积神经网络 hog:方向梯度 + svm，这里使用卷积神经网络来查找人脸位置
            face_locations = face_recognition.face_locations(rgb_small_frame, model="cnn")
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names.clear()
            detected_faces.clear()
            for face_encoding in face_encodings:
                # 人名、近似度的默认值
                name = "Unknown"
                similarity = 0.0

                # 计算当前脸与已知的脸的欧氏距离，越小越相近
                face_distances = face_recognition.face_distance(person_face_encodings, face_encoding)
                # 将当前人脸编码与已知的所有人脸编码进行比对，确定是否匹配
                matches = face_recognition.compare_faces(person_face_encodings, face_encoding, tolerance=0.35)  # 容忍度

                # 获取第一个匹配的人名
                for index, match in enumerate(matches):
                    if match:
                        name = person_names[index]
                        similarity = face_distances[index]
                        # print("[#] face detected, data:", name)
                        break

                face_names.append((name, similarity))
                detected_faces.append(name)
        # 交替 True, False, True, ...
        # 保证每隔interval帧进行一次识别，而不是每一帧都识别
        # if counter < interval:
        #     process_this_frame = False
        #     counter = counter + 1
        # else:
        #     process_this_frame = True
        #     counter = 0

        # 显示面部的框、人名
        for (top, right, bottom, left), (name, similarity) in zip(face_locations, face_names):
            # 由于前面是从小图的中识别的脸，因此此处要扩大回原来的比例
            scale = 2  # 缩放比例和上面的帧缩放对应
            top *= scale
            right *= scale
            bottom *= scale
            left *= scale

            # 画脸的框
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            # 画文字
            cv2.putText(frame, "%s, %.2f" % (name, 1 - similarity), (left, bottom + 25), cv2.FONT_HERSHEY_DUPLEX, 0.7,
                        (0, 255, 0),
                        1)
        ret, output = cv2.imencode('.jpg', frame)
        out_frame = output.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + out_frame + b'\r\n')  # 逐帧传递(http报文)
        """
        python中还有一种返回值的方法，那就是yield。带有yield的函数是一个迭代器，
        函数返回某个值时，会停留在某个位置，返回函数值后，会在前面停留的位置继续执行，
        直到程序结束。
        """


# 视频流响应
def video_feed(request):
    return StreamingHttpResponse(gen_frames(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


############################################################################################


def index(request):
    # 去app目录下的templates目录寻找对应的html
    return render(request, "index.html")


def login(request):
    if request.method == "GET":
        return render(request, "login.html")

    # 如果是post请求，获取用户提交的数据
    print(request.POST)
    user_name = request.POST.get("user")
    password = request.POST.get("pwd")

    if user_name == 'admin' and password == '123':
        # return HttpResponse("登录成功")
        return redirect("https://www.baidu.com")
    # 登陆失败
    return render(request, "login.html", {"error_msg": "登录失败: 用户名或密码错误"})


def user_regist(request):
    if request.method == "GET":
        print(request)
        # 默认页面
        dataset_handle()  # 预处理
        return render(request, "userRegist.html", {"person_name": detected_faces})

    # 处理POST请求
    print(request.POST)

    username = request.POST.get("name")
    password = request.POST.get("password")

    if username == '' or password == '':
        return render(request, "userRegist.html", {"err_msg": "用户名和密码不符合要求！"})

    ret, save_img = camera.read()
    face_locations = face_recognition.face_locations(save_img, model="cnn")
    # 检测到人脸才可进行保存
    if face_locations:
        # 路径格式："D:/xxx/xxx/"，是以“/”结束
        cv2.imwrite('D:/GraguateProject/Django/app/static/img/faces/' + username + '.jpg', save_img)
        print('Saved succeed: ' + username + ' in dataset')
        dataset_handle()  # 录入后再编码一次数据集
        return render(request, "userRegist.html", {"msg": "录入成功"})
    # 未检测到人脸
    return render(request, "userRegist.html", {"err_msg": "未检测到人脸，请保持您的面部在画面中央，并正视摄像头"})


def send_msg(request):
    receive = request.GET
    print(receive)


def get_msg(request):
    result = {"name": detected_faces}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")


def video(request):
    # 处理GET请求
    if request.method == "GET":
        # camera.grab()
        print(request)
        # 关闭摄像头请求
        if request.GET.get("close") == "shut":
            camera.release()
            # return render(request, "video.html", {"close_msg": "摄像头已关闭"})
            return HttpResponse("摄像头已关闭")

        # if request.GET.get("open") == "active":
        #     camera.open(0)
        #     # return render(request, "video.html", {"msg": "摄像头已开启"})
        #     return HttpResponse("摄像头已开启")

        if request.GET.get("camID") == "local":
            camera.release()  # 释放当前摄像头
            camera.open(0)  # 开启对应设备

        if request.GET.get("camID") == "usb":
            camera.open(1)  # 开启对应设备

        if request.GET.get("camID") == "ip":
            camera.open(video)  # 开启对应设备

        # 默认页面
        dataset_handle()  # 预处理
        return render(request, "video.html", {"person_name": detected_faces,
                                              "cam_list": {
                                                  "cam_1": {"name": "local_0"},
                                                  "cam_2": {"name": "local_1"},
                                                  "cam_3": {"name": "remote_0"}
                                              }
                                              })

        # 处理POST请求
        # print(request.POST)
        #
        # username = request.POST.get("name")
        # password = request.POST.get("password")
        #
        # if username == '' or password == '':
        #     return render(request, "video.html", {"err_msg": "用户名和密码不符合要求！"})
        #
        # ret, save_img = camera.read()
        # face_locations = face_recognition.face_locations(save_img, model="cnn")
        # # 检测到人脸才可进行保存
        # if face_locations:
        #     # 路径格式："D:/xxx/xxx/"，是以“/”结束
        #     cv2.imwrite('D:/GraguateProject/Django/app/static/img/faces/' + username + '.jpg', save_img)
        #     print('Saved succeed: ' + username + ' in dataset')
        #     dataset_handle()  # 录入后再编码一次数据集
        #     return render(request, "video.html", {"msg": "录入成功"})
        # # 未检测到人脸
        # return render(request, "video.html", {"err_msg": "未检测到人脸，请保持您的面部在画面中央，并正视摄像头"})
