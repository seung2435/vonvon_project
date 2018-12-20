from flask import Flask, render_template, request
from faker import Faker
import random
import csv


app = Flask(__name__)
fake = Faker('ko_KR')

namelist = {}
# fish = []

# '/' : 사용자의 이름 입력받기
@app.route('/js')
def index():
    return render_template('junsaeng.html')
    
# 'pastlife' : 사용자의 (랜덤으로 생성된) 직업/전생 보여주기
@app.route('/pastlife')
def pastlife():
    name = request.args.get('username')

    # 만약에 검색했던 사람이 같은 이름을 입력하면, 동일한 전생을 보여줌
    # 아니라면, 새로운 전생을 보여줌
    if name in namelist :
        pl = namelist[name]
    else :
        pl = fake.job()
        namelist[name] = pl
    return render_template('pl.html', name=name, pl=pl)





@app.route('/')
def landing():
    # 두 사람의 이름을 입력 받음
    return render_template('index.html')
    
@app.route('/match')
def match():
    # 1. fake 궁합을 알려줌
    # 2. 우리만 알 수 있게 저장
    #   - fish 리스트에 append 통해 저장
    # 3. match.html에는 두 사람의 이름과 random으로 생성된 50~100사이 수를 함께 출력
    #   - xxx님과 yyy님의 궁합은 88%입니다
    
    me = request.args.get('me')
    you = request.args.get('you')
    
    # fish.append([me, you])
    
    # csv파일을 통한 데이터 영구저장
    with open('fish.csv','a',encoding="utf-8") as f:
        fish = csv.writer(f)
        fish.writerow([me,you])
    # f.close() #with는 open한 파일을 임시적으로 제어, 제어가 끝나면 자동으로 닫아줌 > close() 할 필요x
    
    matching = random.randrange(50,101)
    
    return render_template('match.html', me=me, you=you, matching=matching)
    
@app.route('/admin')
def admin():
    # 낚인 사람들의 명단
    #   - template에서 반복문을 사용하여 fish 內 데이터 모두 출력
    #   - fish에 들어가 있는 데이터를 모두 보여줌
    
    data = []
    
    with open('fish.csv','r',encoding="utf-8") as f:
        # fish_list = csv.reader(f) #python자체가 csv파일을 읽을 때, 이중배열화해서 읽음 > 해당 코드를 쓰지 않아도 됨
        for fish in f:
            data.append(fish)
                
    return render_template('admin.html', fish=data)
    
    # for x,y in fish:
    #     me = str(x)
    #     you = str(y)
    # return render_template('admin.html', me=me, you=you)