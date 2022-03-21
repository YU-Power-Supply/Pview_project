import recommend_type1_func as f
import numpy as np

s_acne = f.LineA()
s_stimulus = f.LineB()
s_whitening = f.LineC()
s_wrinkle = f.LineD()
s_moisture = f.LineE()
a_moisturizing = f.LineF()
a_oil = f.LineG()


#라인별 타입정보 출력함수
def typeDefinition(user):
    userType = [s_acne.typeClassification(user1.score_data)+1,
                s_stimulus.typeClassification(user1.score_data)+1,
                s_whitening.typeClassification(user1.score_data)+1,
                s_wrinkle.typeClassification(user1.score_data)+1,
                s_moisture.typeClassification(user1.score_data)+1,
                a_moisturizing.typeClassification(user1.score_data)+1,
                a_oil.typeClassification(user1.score_data)+1]

    cosmeticIng = [s_acne.typeList[userType[0]-1],
                    s_stimulus.typeList[userType[1]-1],
                    s_whitening.typeList[userType[2]-1],
                    s_wrinkle.typeList[userType[3]-1],
                    s_moisture.typeList[userType[4]-1],
                    a_moisturizing.typeList[userType[5]-1],
                    a_oil.typeList[userType[6]-1]]

    print(userType)
    print(cosmeticIng)


user1 = f.User()

#임의로 점수 생성 (유분/수분(각질)/주름/피부톤/색소침착/모공)
test_score_data = [0.123,0.234,0.345,0.456,0.567,0.678]


if __name__ == "__main__":
    #유저 점수 업데이트
    user1.score_update(test_score_data)
    typeDefinition(user1)

