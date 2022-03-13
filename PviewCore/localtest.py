from Wrinkle import wrinkleDetect as wd
from SkinTone import skinToneDetect as st
from Pore import poreDetect as pd
from Oilly import oilly as ol
from PIH import PIH_model as ph

PATH = './dataset'
img = 'img.jpg'
img1 = 'img1.jpg'
img2 = 'img2.jpg'

def run_core(img = img):
    WD = wd(PATH, img)
    ST = st(PATH, img)
    PD = pd(PATH, img)
    OL = ol(PATH, img)
    PH = ph(PATH, img)

    return {"DeadSkin": 99, "Wrinkle": WD, "SkinTone": ST, "PoreDetect": PD, "Oilly": OL, "PIL": PH}


if __name__ == "__main__":
    run_core(img1)
    run_core(img2)