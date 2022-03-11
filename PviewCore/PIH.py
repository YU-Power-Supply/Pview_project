import cv2
import numpy as np
import os
from matplotlib import pyplot

height = 320
width = 320
alpha = 0.6

blue1 = np.array([90, 50, 50])
blue2 = np.array([120, 255, 255])
green1 = np.array([45, 50, 50])
green2 = np.array([75, 255, 255])
red1 = np.array([0, 50, 50])
red2 = np.array([15, 255, 255])
red3 = np.array([165, 50, 50])
red4 = np.array([180, 255, 255])
yellow1 = np.array([20, 50, 50])
yellow2 = np.array([35, 255, 255])


def pixelDetector(img):
    cnt = 0
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i][j] == 255:
                cnt += 1
    return cnt


def oilly_normal_dry(imgname, img):
    skinValue = float(pixelDetector(img))/float(height*width)

    if skinValue > 0.1:
        print(f"image: {imgname} is oilly, oilValue : {skinValue*100 : .2f}%")
    elif skinValue > 0.05:
        print(f"image: {imgname} is normal, oilValue : {skinValue*100 : .2f}%")
    else:
        print(f"image {imgname} is dry, oilValue : {skinValue*100 : .2f}%")


def globalThresholding(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh_np = np.zeros_like(img)
    thresh_np[img > 127] = 255


def contrastControlByHistogram(Img, alpha):
    func = (1+alpha) * Img - (alpha * 128)  # 128을 기준으로 명암 맞춰줌
    dst = np.clip(func, 0, 255).astype(np.uint8)
    return dst

# Canny Edge
# cv2.Canny(image, threshold1, threshold2, edge = None, apertureSize = None, L2gradient = None)
# Gausian Blur
# cv2.GaussianBlur(image, ksize, sigmaX, dst=None, sigmaY=None, borderType=None)
# [sigmaX, sigmaY : x, y 편향]
# [ksize : 가우시안 커널 크기, (0, 0)을 지정하면 sigma 값에 의해 자동 결정됨]
# [borderType : 가장자리 픽셀 확장 방식]


def canny(img):
    canny = cv2.Canny(img, 40, 70)  # 2:1 혹은 3:1 의비율을 권함
    return canny


def fillterCustom(img):
    gx_k = np.array([[-3, 0, 3], [-10, 0, 10], [-3, 0, 3]])
    gy_k = np.array([[-3, -10, -3], [0, 0, 0], [3, 10, 3]])
    edge_gx = cv2.filter2D(img, -1, gx_k)
    edge_gy = cv2.filter2D(img, -1, gy_k)
    # scharrx = cv2.Scharr(img, -1, 1, 0)
    # scharry = cv2.Scharr(img, -1, 0, 1)

    # merged1 = np.hstack((img, edge_gx, edge_gy))
    # merged2 = np.hstack((img, scharrx, scharry))
    # merged = np.vstack((merged1, merged2))
    return (edge_gy+edge_gx)/320


def deleteSkinTexture(img):  # 원하는 화소값을 제외하고 삭제
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.inRange(img, 110, 255)
    return img


def oilly_model():
    oilly = []
    dry = []
    for i in range(4):
        oilly.append(cv2.resize(cv2.imread(f"oilly{i+1}.jpg", cv2.IMREAD_COLOR), dsize=(width, height)))
        dry.append(cv2.resize(cv2.imread(f"dry{i+1}.jpg", cv2.IMREAD_COLOR), dsize=(width, height)))

    for i in range(4):
        cv2.imshow(f"oilly{i+1}", oilly[i])
        cv2.imshow(f"canny_oilly{i+1}", canny(contrastControlByHistogram(oilly[i], 0.6)))

        cv2.imshow(f"dry{i+1}", dry[i])
        cv2.imshow(f"canny_dry{i+1}", canny(contrastControlByHistogram(dry[i], 0.6)))

        oilly_normal_dry(f"oilly{i+1}", canny(contrastControlByHistogram(oilly[i], 0.6)))
        oilly_normal_dry(f"dry{i+1}", canny(contrastControlByHistogram(dry[i], 0.6)))

    cv2.waitKey(0)


def deadSkin_model_dataPrepocessing(img):
    image_b, image_g, image_r = cv2.split(img)
    avrColor = (image_b.sum()/(width*height), image_g.sum()/(width*height), image_r.sum()/(width*height))

    # img = cv2.Canny(img, 40, 70)

    image_b = np.clip((1+alpha) * image_b - (alpha * avrColor[0]), 0, 255).astype(np.uint8)
    image_g = np.clip((1+alpha) * image_g - (alpha * avrColor[1]), 0, 255).astype(np.uint8)
    image_r = np.clip((1+alpha) * image_r - (alpha * avrColor[2]), 0, 255).astype(np.uint8)

    img = cv2.merge((image_b, image_g, image_r))
    img = fillterCustom(img)
    image_b, image_g, image_r = cv2.split(img)
    img = (image_r+image_g+image_b)/3
    return img


def deadSkin_model(path):
    for image in os.listdir(f"{path}"):
        img = cv2.resize(cv2.imread(f"{path}/{image}", cv2.IMREAD_COLOR), dsize=(width, height))
        img = deadSkin_model_dataPrepocessing(img)
        pyplot.imsave(f"{path}/{image}", img)

        # pyploy.imsave("",)


def colorMask(img):

    initValue_s = 130
    initValue_alpha = 0.5
    img = contrastControlByHistogram(img, initValue_alpha)

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    img_hsv_h = img_hsv[:, :, 0]
    img_hsv_s = img_hsv[:, :, 1]
    # img_hsv_v = img_hsv[:, :, 2]

    for i in range(len(img_hsv_s)):
        for j in range(len(img_hsv_s[0])):
            if 60 <= img_hsv_h[i][j] < 330:
                img[i][j] = np.array([122, 122, 122])
            if img_hsv_s[i][j] < initValue_s:
                img[i][j] = np.array([122, 122, 122])

    return img
    # np.zeros_like(img, dtype=int)
    # img_mask = cv2.inRange(img, fromColor, toColor)


def PIH(img):

    # 특징점 알고리즘 객체 생성 (KAZE, AKAZE, ORB 등)
    feature = cv2.KAZE_create(threshold=0.0002)  # 방향 성분은 표현이 안됌
    # feature = cv2.AKAZE_create() # 카제를 빠르게, accelateKaze, 방향선분 표현
    # feature = cv2.ORB_create() # 가장 빠르지만 성능이 떨어짐

    # 특징점 검출
    kp1 = feature.detect(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    # kp2 = feature.detect(src2)

    # 검출된 특징점 갯수 파악
    print(f"색소침착 : {len(kp1)}")

    # 검출된 특징점 출력 영상 생성
    img = cv2.drawKeypoints(img, kp1, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    return len(kp1)  # img


def PIH_model(PATH, img):
    pih_img = (cv2.resize(cv2.imread(f"{PATH}/{img}", cv2.IMREAD_COLOR), dsize=(width, height)))
    return PIH(contrastControlByHistogram(pih_img, 0.6))


def imgCropper(path):
    # 이미지 크로핑 후 처리
    for image in os.listdir(f"{path}"):
        # print(f"{path}/{image}"[-4:])

        img = cv2.imread(f"{path}/{image}")
        # crop_img1 = img[0:640, 240:480]
        crop_img2 = img[25:404, 0:240]
        # cv2.imshow("show", crop_img2)
        print(f"{path}/{image[:-4]}.jpg")
        cv2.imwrite(f"{path}/{image[:-4]}.jpg", crop_img2)
        # os.remove(f"{path}/{image}")
        cv2.waitKey(0)
