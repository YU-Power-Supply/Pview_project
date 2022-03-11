from PviewCore.Wrinkle import wrinkleDetect as wd  # 주름
from PviewCore.SkinTone import skinToneDetect as st  # 피부톤
from PviewCore.Pore import poreDetect as pd  # 모공
# from DeadSkin import deadSkin as ds  # 각질
from PviewCore.Oilly import oilly as ol  # 유분
from PviewCore.PIH import PIH_model as ph  # 색소침착

PATH = 'PviewCore/dataset'
img = 'img.jpg'
# ds(PATH, img)


def run_core(img=img):
    WD = wd(PATH, img)
    ST = st(PATH, img)
    PD = pd(PATH, img)
    OL = ol(PATH, img)
    PH = ph(PATH, img)

    return {"DeadSkin": 99, "Wrinkle": WD, "SkinTone": ST, "PoreDetect": PD, "Oilly": OL, "PIL": PH}
