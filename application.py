from flask import Flask, render_template, request
import sys
from drawChart import *
from dashboardData import updateDashData
sys.path.append("module/")
application = Flask(__name__)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/index')
def getIndex():
    return render_template('index.html')

@application.route('/mock')
def getMock():
    updateChart()
    updateChart2()
    return render_template('mock.html')

@application.route('/predic')
def getPredic():
    return render_template('predic.html')

@application.route('/analysis')
def getAnalysis():
    return render_template('analysis.html')

@application.route('/dashboard')
def getDashboard():
    updateDashData()
    return render_template('dashboard.html')

@application.route('/search')
def searchResult():
    kosdaqNameList =['카카오게임즈', '펄어비스', '에스티팜', '제넥신', '스튜디오드래곤',
                     '엘앤에프', '솔브레인', '셀트리온헬스케어', '원익IPS', '휴젤',
                     '케이엠더블유', '셀트리온제약', '에코프로비엠', 'SK머티리얼즈',
                     '리노공업', '씨젠', 'CJ ENM', '알테오젠', '티씨케이', '에이치엘비']
    kospiNameList=['SK텔레콤', 'LG생활건강', 'POSCO', 'LG화학', '삼성바이오로직스',
                   'KB금융', 'SK하이닉스', '삼성전자우', '삼성물산', '신한지주', '기아',
                   '삼성전자', '현대차','SK이노베이션', '삼성SDI', 'LG전자',
                   '셀트리온', '현대모비스', 'NAVER', '카카오']
    name=request.args.get("search")
    if name in kosdaqNameList:
        resultChart(name, False)
        return render_template('result.html', name=name)
    elif name in kospiNameList:
        resultChart(name, True)
        return render_template('result.html', name=name)
    else:
        return render_template('error.html')

@application.route('/analysis2')
def getAnalysis2():
    return render_template('analysis2.html')


if __name__ == "__main__":
    application.debug = True
    application.run(host='0.0.0.0', port=int(sys.argv[1]))
