from flask import request, render_template, Blueprint
from MushroomClassification.models import resource_model

re_bp = Blueprint('resource', __name__, url_prefix='/resource')
re_service = resource_model.Service()

# 입력 폼
@re_bp.route('/resourceForm')
def resourceForm():
    return render_template('resourceForm.html')

# 버섯도감 목록 검색
@re_bp.route('/searchRequest', methods=['POST'])
def searchRequest():
    # 검색어 구분 (1 : 국명, 2 : 학명, 3 : 국명일치, 4 : 학명일치)
    st = request.form['st']
    # 검색어
    sw = request.form['sw']
    # 한 페이지 결과 수
    numOfRows = request.form['numOfRows']
    # 페이지 번호
    pageNo = request.form['pageNo']

    List = re_service.searchRequest(st, sw, numOfRows, pageNo)
    return render_template('searchRequest.html', List=List)

# 버섯도감 상세정보 조회
@re_bp.route('/infoRequest', methods=['POST'])
def infoRequest():
    # 도감번호
    q1 = request.form['q1']
    print(q1)
    List = re_service.infoRequest(q1)
    return render_template('infoRequest.html', List=List)