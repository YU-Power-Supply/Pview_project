import recommend_type1_func as f
import numpy as np

lineA = f.LineA()
lineB = f.LineB()
lineC = f.LineC()
lineD = f.LineD()
lineE = f.LineE()
lineFG = f.LineFG()

#라인별 타입정보 출력함수
def typeDefinition(user):
    userType = [lineA.typeClassification(user1.score_data)+1,
                lineB.typeClassification(user1.score_data)+1,
                lineC.typeClassification(user1.score_data)+1,
                lineD.typeClassification(user1.score_data)+1,
                lineE.typeClassification(user1.score_data)+1,
                lineFG.typeClassification_F(user1.score_data)+1,
                lineFG.typeClassification_G(user1.score_data)+1]

    cosmeticIng = [lineA.typeList[userType[0]],
                    lineB.typeList[userType[1]],
                    lineC.typeList[userType[2]],
                    lineD.typeList[userType[3]],
                    lineE.typeList[userType[4]],
                    lineFG.typeList_F[userType[5]],
                    lineFG.typeList_G[userType[6]]]

    print(userType)
    print(cosmeticIng)


#유저 정보 기입 및 객체 생성
userName = '홍길동'
userAge = 24
#성별 : 남(0) 여(1)
userSex = 0

user1 = f.User(userName, userAge, userSex)

#임의로 점수 생성 (유분/수분(각질)/주름/피부톤/색소침착/모공)
test_score_data = [0.123,0.234,0.345,0.456,0.567,0.678]

#유저 점수 업데이트
user1.score_update(test_score_data)

typeDefinition(user1)

