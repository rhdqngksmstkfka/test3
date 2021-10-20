from flask import request, render_template, Blueprint
from MushroomClassification.models import img_model

is_bp = Blueprint('img', __name__, url_prefix='/img')
is_service = img_model.Service()

# 입력
@is_bp.route('/imgForm')
def imgForm():
    return render_template('imgForm.html')

# 이미지 포함 검색
@is_bp.route('/imgSearchForm', methods=['POST'])
def imgSearchForm():
    # 한 페이지 결과 수
    numOfRows = request.form['numOfRows']
    # 페이지 수
    pageNo = request.form['pageNo']
    # 검색 구분
    option = request.form['option']
    # 검색어
    searchWord = request.form['searchWord']

    List = is_service.imgSearch(numOfRows, pageNo, option, searchWord)
    return render_template('imgSearchForm.html', List=List)


