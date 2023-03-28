# django_CHJinstagram

취약점진단팀 인스타  asdasd 클론 웹 CHJinstagram 깃 커밋 테스트 성공ㅠㅠ


---

## 실행

python 3.7 이상 버전 설치 후 555

```
# 가상환경 생성 
python -m venv venv

# 가상환경 실행
source ./venv/Scripts/activate

# 필요 package 설치
pip install -r requirements.txt

# migrate 명령어로 DB 생성
python manage.py makemigrations
python manage.py migrate

# 서버 실행
python manage.py runserver

# 브라우져로 접속
http://127.0.0.1:8000/main/
```
