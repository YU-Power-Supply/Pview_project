
class User:
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex

        self.oil_score = 0
        self.moisture_score = 0
        self.wrinkle_score = 0
        self.skinTone_score = 0
        self.pigmentation_score = 0
        self.pore_score = 0

        self.score_data = []

    def score_update(self, score_data):
        self.score_data = score_data

        self.oil_score = score_data[0]
        self.moisture_score = score_data[1]
        self.wrinkle_score = score_data[2]
        self.skinTone_score = score_data[3]
        self.pigmentation_score = score_data[4]
        self.pore_score = score_data[5]

        print('update complited')

#앰플라인과 스킨라인 구별
class AmpleLine:
    def __init__(self, typeList):
        self.typeList = typeList
        self.type_criteria = [1/len(self.typeList) * (i+1) for i in range(len(self.typeList))]

    def typeClassification(self, score_data):
        return -1

class SkinLine:
    def typeClassification_F(self, score_data):
        return -1

    def typeClassification_G(self, score_data):
        return -1

#타입별 클래스 구별
class LineA(AmpleLine): #진정(여드름)
    def __init__(self):
        #TypeN 변수에는 라인별 성분 비율(%) 들어감.
        self.typeOne = 1.1
        self.typeTwo = 2.2
        self.typeThree = 3.3
        self.typeFour = 4.4
        self.typeList = [self.typeOne, self.typeTwo, self.typeThree, self.typeFour]
        super().__init__(self.typeList)

    #@Overriding
    def typeClassification(self, score_data):
        #모공 + 유분
        pore_score = score_data[5]
        oil_score = score_data[0]

        type_score = pore_score * 0.5 + oil_score * 0.5 #모공점수 50%, 유분점수 50%
        print(type_score, self.type_criteria)
        for criteria in self.type_criteria:
            if type_score <= criteria:
                type_result = self.type_criteria.index(criteria)
                break

        return type_result
    

class LineB(AmpleLine): #진정(자극완화)
    def __init__(self):
        self.typeOne = 1.1
        self.typeTwo = 2.2
        self.typeThree = 3.3
        self.typeList = [self.typeOne, self.typeTwo, self.typeThree]
        super().__init__(self.typeList)

    #@Overriding
    def typeClassification(self, score_data):
        #색소침착
        pih_score = score_data[4]
        
        type_score = pih_score #색소침착 점수 100%
        print(type_score, self.type_criteria)
        for criteria in self.type_criteria:
            if type_score <= criteria:
                type_result = self.type_criteria.index(criteria)
                break

        return type_result

class LineC(AmpleLine): #미백
    def __init__(self):
        self.typeOne = 1.1
        self.typeTwo = 2.2
        self.typeThree = 3.3
        self.typeList = [self.typeOne, self.typeTwo, self.typeThree]
        super().__init__(self.typeList)

    #@Overriding
    def typeClassification(self, score_data):
        #피부톤
        skinTone_score = score_data[3]

        type_score = skinTone_score #피부톤 점수 100%
        print(type_score, self.type_criteria)
        for criteria in self.type_criteria:
            if type_score <= criteria:
                type_result = self.type_criteria.index(criteria)
                break
        
        return type_result

class LineD(AmpleLine): #주름
    def __init__(self):
        self.typeOne = 1.1
        self.typeTwo = 2.2
        self.typeList = [self.typeOne, self.typeTwo]
        super().__init__(self.typeList)

    #@Overriding
    def typeClassification(self, score_data):
        #주름
        wrinkle_score = score_data[2]

        type_score = wrinkle_score #주름 점수 100%
        print(type_score, self.type_criteria)
        for criteria in self.type_criteria:
            if type_score <= criteria:
                type_result = self.type_criteria.index(criteria)
                break
        
        return type_result

class LineE(AmpleLine): #수분
    def __init__(self):
        self.typeOne = 1.1
        self.typeTwo = 2.2
        self.typeList = [self.typeOne, self.typeTwo]
        super().__init__(self.typeList)

    #@Overriding
    def typeClassification(self, score_data):
        #각질
        deadskin_score = score_data[1]

        type_score = deadskin_score #각질 점수 100%
        print(type_score, self.type_criteria)
        for criteria in self.type_criteria:
            if type_score <= criteria:
                type_result = self.type_criteria.index(criteria)
                break
        
        return type_result

class LineFG(SkinLine): #F:보습 G:유분
    def __init__(self):
        #F라인 타입별 성분용량
        self.typeOne_F = 1.1
        self.typeTwo_F = 2.2
        self.typeThree_F = 3.3
        self.typeFour_F = 4.4
        self.typeFive_F = 5.5
        #G라인 타입별 성분용량
        self.typeOne_G = 1.01
        self.typeTwo_G = 2.02
        self.typeThree_G = 3.03
        self.typeFour_G = 4.04
        self.typeFive_G = 5.05

        self.typeList_F = [self.typeOne_F, self.typeTwo_F, self.typeThree_F, self.typeFour_F, self.typeFive_F]
        self.typeList_G = [self.typeOne_G, self.typeTwo_G, self.typeThree_G, self.typeFour_G, self.typeFive_G]
        
        self.type_criteria = [1/len(self.typeList_F) * (i+1) for i in range(len(self.typeList_F))]

    #@Overriding
    def typeClassification_F(self, score_data):
        #유분 + 수분
        oil_score = score_data[0]
        deadskin_score = score_data[1]

        type_score = oil_score*0.5 + deadskin_score*0.5 #피부톤 점수 100%
        print(type_score, self.type_criteria)
        for criteria in self.type_criteria:
            if type_score <= criteria:
                type_result = self.type_criteria.index(criteria)
                break
        
        return type_result

    #@Overriding
    def typeClassification_G(self, score_data):
        #유분
        oil_score = score_data[0]

        type_score = oil_score #유분 점수 100%
        print(type_score, self.type_criteria)
        for criteria in self.type_criteria:
            if type_score <= criteria:
                type_result = self.type_criteria.index(criteria)
                break
        
        return type_result
