import requests
from bs4 import BeautifulSoup


class Resource:
    def __init__(self, imgUrl=None, fngsGnrlNm=None, fngsScnm=None, fngsPilbkNo=None, cont12=None):
        # 이미지URL
        self.imgUrl = imgUrl
        # 국명
        self.fngsGnrlNm = fngsGnrlNm
        # 학명
        self.fngsScnm = fngsScnm
        # 도감번호
        self.fngsPilbkNo = fngsPilbkNo
        # 식용여부
        self.cont12 = cont12


class Service:
    def __init__(self):
        self.base_url = 'http://openapi.nature.go.kr/openapi/service/rest/FungiService'
        self.api_key = 'z87XiFqBjizhP7gRBLRttGzJYgKrESmLrKQNmb1aVULKjUTS9f6TBr2rppZBMSEXbq1ovC5bUdGj2N%2FYD6pKPg%3D%3D'

    # 버섯도감 목록 검색
    def searchRequest(self, st, sw, numOfRows, pageNo):
        url = self.base_url + '/fngsIlstrSearch?ServiceKey=' + self.api_key + '&st='+ st + '&sw=' + sw + '&numOfRows=' + numOfRows + '&pageNo=' + pageNo
        html = requests.get(url).text
        root = BeautifulSoup(html, 'lxml-xml')
        code = root.find('resultCode').text
        resultMsg = root.find('resultMsg').text
        results = []

        if code == '00':
            items = root.select('item')
            for item in items:
                # 이미지URL
                imgUrl = item.find('imgUrl').text
                # 국명
                fngsGnrlNm = item.find('fngsGnrlNm').text
                # 학명
                fngsScnm = item.find('fngsScnm').text
                # 도감번호
                fngsPilbkNo = item.find('fngsPilbkNo').text

                # 맹독여부 확인 위해 버섯도감 상세정보 조회 실시
                url = self.base_url + '/fngsIlstrInfo?ServiceKey=' + self.api_key + '&q1=' + fngsPilbkNo
                html = requests.get(url).text
                root = BeautifulSoup(html, 'lxml-xml')
                code = root.find('resultCode').text

                if code == '00':
                    items = root.select('item')
                    for item in items:
                        # 식용여부
                        cont12 = item.find('cont12').text
                        if cont12 ==' ':
                            cont12 = '불명'

                results.append([imgUrl, fngsGnrlNm, fngsScnm, fngsPilbkNo, cont12])

            return results

        else:
            print('오류발생코드: ', code)
            print('오류 메시지: ', resultMsg)

    # 버섯도감 상세정보 조회
    def infoRequest(self, q1):
        url = self.base_url + '/fngsIlstrInfo?ServiceKey=' + self.api_key + '&q1='+ q1
        html = requests.get(url).text
        root = BeautifulSoup(html, 'lxml-xml')
        code = root.find('resultCode').text
        resultMsg = root.find('resultMsg').text
        results = []

        if code == '00':
            items = root.select('item')
            for item in items:
                # 과국명
                familyKorNm = item.find('familyKorNm').text
                # 과명
                familyNm = item.find('familyNm').text
                # 속국명
                genusKorNm = item.find('genusKorNm').text
                # 속명
                genusNm = item.find('genusNm').text
                # 국명
                fngsGnrlNm = item.find('fngsGnrlNm').text
                # 전체학명
                fngsScnm = item.find('fngsScnm').text
                # 독성여부
                cont12 = item.find('cont12').text
                if cont12 == ' ':
                    cont12 = '불명'
                # 발생 계절
                occrrSsnNm = item.find('occrrSsnNm').text
                if occrrSsnNm == ' ':
                    occrrSsnNm = '사계절'
                # 발생 형태 설명
                occrrFomDscrt = item.find('occrrFomDscrt').text
                if occrrFomDscrt == ' ':
                    occrrFomDscrt = '불명'
                # 발생장소
                cont21 = item.find('cont21').text
                if cont21 == ' ':
                    cont21 = '불명'

                results.append([familyKorNm, familyNm, genusKorNm, genusNm, fngsGnrlNm, fngsScnm, cont12, occrrSsnNm, occrrFomDscrt, cont21])
            print(results)
            return results

        else:
            print('오류발생코드: ', code)
            print('오류 메시지: ', resultMsg)
