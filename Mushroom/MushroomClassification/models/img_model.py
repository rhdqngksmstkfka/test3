import requests
from bs4 import BeautifulSoup

class ImageList:
    def __init__(self, numOfRows=None, pageNo=None, option=None, searchWord=None, pageIndex=None, pageUnit=None):
        # 한 페이지 결과 수
        self.numOfRows = numOfRows
        # 페이지 수
        self.pageNo = pageNo
        # 검색 구분
        self.option = option
        # 검색어
        self.searchWord = searchWord
        # 선택페이지
        self.pageIndex = pageIndex
        # 페이지 사이즈
        self.pageUnit = pageUnit


class Service:
    def __init__(self):
        self.base_url ='http://apis.data.go.kr/1390804/NihhsMushroomImageInfo/'
        self.api_key = ''

    # 이미지 포함 검색
    def imgSearch(self, numOfRows, pageNo, searchWord):
        cmd = 'selectMushroomImageList?'
        url = self.base_url + cmd + '&serviceKey=' + self.api_key + '&searchWord=' + searchWord + '&numOfRows=' + numOfRows + '&pageNo=' + pageNo
        html = requests.get(url).text
        root = BeautifulSoup(html, 'lxml-xml')
        code = root.find('resultCode').get_text()
        resultMsg = root.find('resultMsg').text
        results = []

        if code == '1': # 출력부에서 받아오는 부분(응답메세지에서 가져오는)
            items = root.select('result')
            for item in items:
                scNameKr = item.find('scNameKr').get_text()
                scName = item.find('scName').get_text()
                imgFileUrl = item.find('imgFileUrl').get_text()
                publishOrg = item.find('publishOrg').get_text()

                results.append([scNameKr, scName, imgFileUrl, publishOrg])
            return results

        else:
            print('오류발생 code:', code)
            print('오류 메시지: ', resultMsg)
