import cv2
import numpy as np

height = 320
width = 320
alpha = 0.8


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
        print(f"유분 : {imgname} is oilly, oilValue : {skinValue*100 : .2f}%")
    elif skinValue > 0.05:
        print(f"유분 : {imgname} is normal, oilValue : {skinValue*100 : .2f}%")
    else:
        print(f"유분 : {imgname} is dry, oilValue : {skinValue*100 : .2f}%")

    return round(skinValue*100, 5)


def contrastControlByHistogram(Img):
    func = (1+alpha) * Img - (alpha * 128)  # 128을 기준으로 명암 맞춰줌
    dst = np.clip(func, 0, 255).astype(np.uint8)
    return dst


def canny(img):
    canny = cv2.Canny(img, 150, 450)  # 2:1 혹은 3:1 의비율을 권함
    return canny


def deleteSkinTexture(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.inRange(img, 110, 255)
    return img


def oilly(PATH, img):
    oilly = cv2.resize(cv2.imread(f"{PATH}/{img}", cv2.IMREAD_COLOR), dsize=(width, height))
    return oilly_normal_dry(f"{img}", canny(contrastControlByHistogram(oilly)))
